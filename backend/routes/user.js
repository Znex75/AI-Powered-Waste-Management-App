const express = require('express');
const router = express.Router();
const authenticateToken = require('../middleware/auth');
const prisma = require('../prisma');

// Create user profile (after Supabase signup)
router.post('/profile', authenticateToken, async (req, res) => {
  const { name, email } = req.body;
  
  try {
    // Check if user already exists
    let user = await prisma.user.findUnique({
      where: { id: req.user.id }
    });

    if (!user) {
      user = await prisma.user.create({
        data: {
          id: req.user.id,
          name: name || 'Eco Warrior',
          email: email || req.user.email,
        }
      });
    }
    
    res.json({ message: 'Profile created/verified successfully', user });
  } catch (error) {
    console.error('Error creating profile:', error);
    res.status(500).json({ error: 'Failed to create profile' });
  }
});

// Get User Profile (Protected Route)
router.get('/profile', authenticateToken, async (req, res) => {
  try {
    let user = await prisma.user.findUnique({
      where: { id: req.user.id },
      include: {
        scans: true,
        listings: true
      }
    });

    if (!user) {
      // Auto-create local profile if it doesn't exist yet!
      user = await prisma.user.create({
        data: {
          id: req.user.id,
          name: req.user.user_metadata?.name || req.user.email.split('@')[0],
          email: req.user.email,
        },
        include: { scans: true, listings: true }
      });
    }

    res.json({
      message: 'Profile retrieved successfully',
      user
    });
  } catch (error) {
    console.error('Error fetching profile:', error);
    res.status(500).json({ error: 'Failed to fetch profile' });
  }
});

// Purchase credits placeholder endpoint
router.post('/purchase', authenticateToken, async (req, res) => {
  const { type, quantity } = req.body;
  const qty = Number(quantity) || 5;

  if (!['scan', 'market'].includes(type)) {
    return res.status(400).json({ error: 'Invalid purchase type. Use scan or market.' });
  }

  const paymentUrl = process.env.PAYMENT_BASE_URL
    ? `${process.env.PAYMENT_BASE_URL}/checkout?type=${type}&qty=${qty}`
    : `https://example.com/pay?type=${type}&qty=${qty}`;

  res.json({
    message: 'Payment required to purchase credits.',
    paymentUrl,
    amountDue: type === 'scan' ? qty * 0.99 : qty * 1.49,
    credits: qty
  });
});

module.exports = router;
