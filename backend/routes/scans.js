const express = require('express');
const router = express.Router();
const authenticateToken = require('../middleware/auth');
const prisma = require('../prisma');
const axios = require('axios');

const WASTE_BIN_MAP = {
  Plastic: 'Blue Bin',
  plastic: 'Blue Bin',
  Glass: 'Green Bin',
  glass: 'Green Bin',
  Paper: 'Paper Bin',
  paper: 'Paper Bin',
  Metal: 'Metal Bin',
  metal: 'Metal Bin',
  Compost: 'Compost',
  compost: 'Compost',
  Electronics: 'E-Waste',
  electronics: 'E-Waste',
  'e-waste': 'E-Waste',
  Organic: 'Compost',
  organic: 'Compost',
  Hazardous: 'Hazardous Waste',
  hazardous: 'Hazardous Waste',
  Default: 'General Waste'
};

const MATERIAL_MATCHERS = [
  { category: 'Plastic', keywords: ['plastic', 'bottle', 'pet'] },
  { category: 'Glass', keywords: ['glass', 'jar'] },
  { category: 'Paper', keywords: ['paper', 'cardboard', 'carton', 'book', 'newspaper'] },
  { category: 'Metal', keywords: ['metal', 'aluminium', 'aluminum', 'steel', 'can', 'copper', 'wire'] },
  { category: 'Electronics', keywords: ['electronic', 'e-waste', 'battery', 'phone', 'keyboard', 'cable'] },
  { category: 'Compost', keywords: ['compost', 'organic', 'food', 'leaf', 'leaves'] },
  { category: 'Hazardous', keywords: ['hazard', 'chemical', 'paint', 'medical'] }
];

function getMaterialCategory(label) {
  const normalized = String(label).toLowerCase();
  const match = MATERIAL_MATCHERS.find((item) => item.keywords.some((keyword) => normalized.includes(keyword)));
  return match?.category || 'Other';
}

function getBinCategory(label) {
  const materialCategory = getMaterialCategory(label);
  return WASTE_BIN_MAP[label] || WASTE_BIN_MAP[String(label).toLowerCase()] || WASTE_BIN_MAP[materialCategory] || WASTE_BIN_MAP.Default;
}

function normalizePrediction(predictions) {
  if (!Array.isArray(predictions) || predictions.length === 0) {
    return null;
  }

  const topPrediction = [...predictions].sort((a, b) => {
    const aScore = a.confidence || a.score || 0;
    const bScore = b.confidence || b.score || 0;
    return bScore - aScore;
  })[0];
  const label = topPrediction.class || topPrediction.label || topPrediction.predicted_class || 'Unknown Item';
  const confidence = topPrediction.confidence || topPrediction.score || 0;

  return {
    label,
    confidence: Number(confidence.toFixed(2)),
    materialCategory: getMaterialCategory(label),
    binCategory: getBinCategory(label)
  };
}

async function queryRoboflow(imageBase64, imageUrl) {
  const apiKey = process.env.ROBOFLOW_API_KEY;

  if (!apiKey) {
    throw new Error('Roboflow API configuration missing');
  }

  const endpoint = `https://serverless.roboflow.com/znexs-workspace/workflows/detect-and-classify-5`;
  const payload = {
    api_key: apiKey,
    inputs: {
      image: imageUrl 
        ? { type: "url", value: imageUrl } 
        : { type: "base64", value: imageBase64 }
    }
  };

  try {
    const response = await axios.post(endpoint, payload, {
      timeout: 30000,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    const detail = error.response?.data?.error || error.response?.data?.message || error.message;
    throw new Error(`Roboflow call failed: ${error.response?.status || 'network'} ${detail}`);
  }
}

router.post('/identify', authenticateToken, async (req, res) => {
  const { imageBase64, imageUrl } = req.body;

  if (!imageBase64 && !imageUrl) {
    return res.status(400).json({ error: 'Missing imageBase64 or imageUrl' });
  }

  try {
    const user = await prisma.user.findUnique({ where: { id: req.user.id } });

    if (!user) {
      return res.status(404).json({ error: 'User profile not found' });
    }

    if (user.scanCredits <= 0) {
      return res.status(402).json({
        error: 'No scan credits left',
        paymentRequired: true,
        message: 'Buy more scan credits to continue identifying waste items.',
        paymentUrl: process.env.PAYMENT_BASE_URL
          ? `${process.env.PAYMENT_BASE_URL}/checkout?type=scan&qty=5`
          : 'https://example.com/pay?type=scan&qty=5'
      });
    }

   const roboflowResult = await queryRoboflow(imageBase64, imageUrl);
console.log("Raw Roboflow response:", JSON.stringify(roboflowResult, null, 2));

// ── Flexible output extraction ──────────────────────────────
let predictions = [];

const extractFromOutput = (output) => {
  if (!output) return [];
  // Standard predictions array
  if (Array.isArray(output.predictions)) return output.predictions;
  // Classification output (object keyed by class name)
  if (output.predictions && typeof output.predictions === 'object') {
    return Object.entries(output.predictions).map(([cls, val]) => ({
      class: cls,
      confidence: typeof val === 'object' ? val.confidence : val
    }));
  }
  // Classes array (some workflow versions)
  if (Array.isArray(output.classes)) return output.classes;
  // top_class shorthand
  if (output.top_class) {
    return [{ class: output.top_class, confidence: output.top_class_confidence || 0.8 }];
  }
  return [];
};

if (Array.isArray(roboflowResult.predictions)) {
  predictions = roboflowResult.predictions;
} else if (Array.isArray(roboflowResult.outputs)) {
  for (const output of roboflowResult.outputs) {
    predictions = extractFromOutput(output);
    if (predictions.length > 0) break;
  }
} else if (roboflowResult.outputs && typeof roboflowResult.outputs === 'object') {
  for (const key of Object.keys(roboflowResult.outputs)) {
    predictions = extractFromOutput(roboflowResult.outputs[key]);
    if (predictions.length > 0) break;
  }
}
// ────────────────────────────────────────────────────────────
     
    const prediction = normalizePrediction(predictions);

    if (!prediction) {
      return res.status(200).json({
        result: {
          label: 'Could not identify waste',
          binCategory: 'General Waste',
          confidence: 0,
          sellable: false,
          xpReward: 0,
          co2Saved: 0
        }
      });
    }

    const xpReward = Math.max(5, Math.min(30, Math.round(prediction.confidence * 25)));
    const co2Saved = Number((xpReward * 0.35).toFixed(2));

    res.json({
      result: {
        label: prediction.label,
        materialCategory: prediction.materialCategory,
        binCategory: prediction.binCategory,
        confidence: prediction.confidence,
        sellable: prediction.confidence > 0,
        xpReward,
        co2Saved,
        recommendation: `Place this item in the ${prediction.binCategory}.`,
        priceEstimate: `(estimate ${Math.max(1, Math.round(prediction.confidence * 10))} EcoCoins)`
      }
    });
  } catch (error) {
    console.error('Roboflow identify error:', error);
    res.status(500).json({ error: 'Failed to identify image', detail: error.message });
  }
});

// Log a scan
router.post('/', authenticateToken, async (req, res) => {
  const { type, binCategory, xpReward, co2Saved } = req.body;

  if (!type || !binCategory) {
    return res.status(400).json({ error: 'type and binCategory are required' });
  }

  try {
    const user = await prisma.user.findUnique({ where: { id: req.user.id } });

    if (!user) {
      return res.status(404).json({ error: 'User profile not found' });
    }

    if (user.scanCredits <= 0) {
      return res.status(402).json({
        error: 'No scan credits left',
        paymentRequired: true,
        paymentUrl: process.env.PAYMENT_BASE_URL
          ? `${process.env.PAYMENT_BASE_URL}/checkout?type=scan&qty=5`
          : 'https://example.com/pay?type=scan&qty=5'
      });
    }

    const scan = await prisma.scan.create({
      data: {
        type,
        binCategory,
        xpReward: xpReward || 10,
        co2Saved: co2Saved || 0.5,
        userId: req.user.id
      }
    });

    const updatedUser = await prisma.user.update({
      where: { id: req.user.id },
      data: {
        xpPoints: { increment: scan.xpReward },
        co2Saved: { increment: scan.co2Saved },
        scanCredits: { decrement: 1 }
      }
    });

    res.json({ message: 'Scan logged successfully', scan, updatedUser });
  } catch (error) {
    console.error('Error logging scan:', error);
    res.status(500).json({ error: 'Failed to log scan' });
  }
});

module.exports = router;
