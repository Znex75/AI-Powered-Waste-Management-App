# EcoCycle Android App

This Android project wraps the existing HTML screens in a native WebView.

## Open in Android Studio

1. Open Android Studio.
2. Choose **Open** and select the `android` folder.
3. Let Gradle sync.
4. Run the `app` configuration on an emulator or Android phone.

## Backend URL

`Authentication/user.html` now uses `http://10.0.2.2:3000` by default, which reaches your computer's `localhost:3000` from the Android emulator.

For a real phone, replace `10.0.2.2` with your computer's LAN IP address, or deploy the backend and use the deployed API URL.
