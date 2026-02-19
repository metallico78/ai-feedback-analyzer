# Android Build Guide - AI Feedback Analyzer

## Overview
This guide provides step-by-step instructions for building, signing, and publishing the AI Feedback Analyzer Android app to Google Play Store.

## Prerequisites

1. **Android Studio** (Latest version)
   - Download from: https://developer.android.com/studio
   - Install with Android SDK 34+
   - Minimum API Level: 21 (Android 5.0)

2. **Java Development Kit (JDK)**
   - JDK 17 or higher

3. **Node.js & npm**
   - For web assets bundling

4. **Android Keystore**
   - For app signing (see Signing section)

## Method 1: Using React Native / Expo (Recommended)

### Setup

```bash
# Install Expo CLI
npm install -g expo-cli eas-cli

# Create new Expo project
npx create-expo-app ai-feedback-analyzer-android
cd ai-feedback-analyzer-android

# Install dependencies
npm install
npm install @react-navigation/native @react-native-community/masked-view
```

### Create App.js

```javascript
import React from 'react';
import { WebView } from 'react-native-webview';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function App() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <WebView
        source={{ uri: 'https://ai-feedback-analyzer-production.up.railway.app' }}
        startInLoadingState={true}
        scalePageToFit={true}
      />
    </SafeAreaView>
  );
}
```

### Build for Android

```bash
# Create build configuration
eas build --platform android --token YOUR_EAS_TOKEN

# Or build locally
npm run android
```

## Method 2: Using Cordova

### Setup

```bash
# Install Cordova
npm install -g cordova

# Create Cordova project
cordova create ai-feedback-analyzer
cd ai-feedback-analyzer

# Add Android platform
cordova platform add android

# Add plugins
cordova plugin add cordova-plugin-inappbrowser
cordova plugin add cordova-plugin-statusbar
```

### Build

```bash
# Debug build
cordova build android

# Release build
cordova build android --release
```

## Method 3: Native Android Studio Project

### Setup

1. Open Android Studio
2. Create a new "Empty Views Activity" project
3. Set:
   - Package name: `com.aiinnovationlab.feedbackanalyzer`
   - Minimum SDK: API 21
   - Target SDK: API 34

### Create WebView Activity

```java
package com.aiinnovationlab.feedbackanalyzer;

import androidx.appcompat.app.AppCompatActivity;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {
    private WebView myWebView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        myWebView = findViewById(R.id.webview);
        myWebView.setWebViewClient(new WebViewClient());
        
        // Enable JavaScript
        myWebView.getSettings().setJavaScriptEnabled(true);
        
        // Load the web app
        myWebView.loadUrl("https://ai-feedback-analyzer-production.up.railway.app");
    }
}
```

### Update AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:theme="@style/Theme.AppCompat.Light">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

## Signing the APK

### Create a Keystore

```bash
keytool -genkey -v -keystore ai-feedback-analyzer-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias ai-feedback-key
```

### Sign the Release Build

In Android Studio:
1. Go to **Build** > **Generate Signed Bundle / APK**
2. Select **APK** (not Bundle)
3. Choose your keystore
4. Fill in password and key information
5. Select **Release** build variant
6. Finish the signing process

The signed APK will be in: `app/release/app-release.apk`

## Publishing to Google Play

### Step 1: Upload to Google Play Console

1. Go to [Google Play Console](https://play.google.com/console)
2. Select your app "AI Feedback Analyzer"
3. Go to **Test & Release** > **Releases** > **Production**
4. Click "Create New Release"
5. Upload the signed APK
6. Add release notes in Spanish and English
7. Review and confirm

### Step 2: Fill in App Details

1. **App Details**
   - Target Audience: Adults
   - Category: Productivity
   - Content rating: Complete the questionnaire

2. **Pricing**
   - Already set to Free
   - Enable in-app purchases if needed

3. **Monetization**
   - Set up Stripe integration
   - Add in-app purchase items
   - Enable billing for premium features

### Step 3: Compliance

- Review privacy policy
- Confirm compliance with Google Play policies
- Complete content rating questionnaire

### Step 4: Submit for Review

1. Click "Submit" button
2. App will undergo automatic review (usually 2-3 hours)
3. Monitor **Policy Status** page for approval

## App Store Configuration (iOS)

### Using Expo

```bash
# Build for iOS
eas build --platform ios --token YOUR_EAS_TOKEN

# Or submit directly
eas submit --platform ios
```

### Using Xcode

1. Open Xcode
2. Create new iOS project
3. Add WebView for the web app
4. Sign with Apple Developer certificate
5. Submit via Xcode (Organizer tab)

## Testing Before Release

### Device Testing

```bash
# Android
adb install app/debug/app-debug.apk
adb logcat  # View logs

# iOS
xcode build and run on simulator
```

### Test Tracks

1. **Internal Testing**: 50+ testers (max)
2. **Closed Testing**: 1,000+ testers
3. **Open Testing**: Public beta
4. **Production**: Final release

### Quality Checklist

- [ ] App loads web view correctly
- [ ] API calls work (feedback analysis)
- [ ] Payment processing works (Stripe integration)
- [ ] UI is responsive on different screen sizes
- [ ] No crashes on normal usage
- [ ] App permissions are properly requested
- [ ] Privacy policy is accessible
- [ ] Terms of service are displayed

## Troubleshooting

### Common Issues

1. **WebView not loading**
   - Check internet permission in manifest
   - Verify Railway app is running
   - Check CORS settings

2. **SSL Certificate Error**
   - Railway provides automatic SSL
   - Add domain to trusted hosts if needed

3. **Build fails**
   - Clear gradle cache: `./gradlew clean`
   - Update SDK: `sdkmanager --update`
   - Check Java version: `java -version`

4. **Play Store rejection**
   - Review rejection reason in Play Console
   - Most common: Privacy policy, permissions
   - Fix and resubmit

## Monetization Strategy

### In-App Purchases

1. **Premium Analysis**: $2.99/month
2. **Export Reports**: $1.99 per export
3. **Batch Processing**: $4.99/month

### Stripe Integration

```python
# In your Flask app
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    intent = stripe.PaymentIntent.create(
        amount=299,  # $2.99 in cents
        currency='usd',
        metadata={'app': 'ai-feedback-analyzer'}
    )
    return {'client_secret': intent.client_secret}
```

## App Marketing

1. **Google Play Listing**
   - Professional screenshots
   - Compelling description
   - Video preview (optional)
   - Keywords for discovery

2. **Social Media**
   - Share on Twitter/X
   - Post on LinkedIn
   - Create TikTok demos
   - Instagram highlights

3. **Community**
   - Reddit threads
   - Product Hunt
   - Hacker News
   - Tech forums

## Maintenance & Updates

### Regular Updates

1. Monitor crash reports in Play Console
2. Review user feedback and ratings
3. Implement bug fixes
4. Add new features based on requests
5. Update dependencies for security

### Performance Optimization

- Monitor app size (target < 20MB)
- Optimize images and assets
- Minimize API calls
- Implement caching strategies
- Use code obfuscation for release builds

## Support Resources

- [Android Developer Guide](https://developer.android.com/guide)
- [Google Play Console Help](https://support.google.com/googleplay/android-developer)
- [Expo Documentation](https://docs.expo.dev)
- [React Native WebView](https://github.com/react-native-webview/react-native-webview)
- [Cordova Documentation](https://cordova.apache.org)

## Next Steps

1. ✅ Create app entry in Google Play Console
2. ⏳ Build APK using chosen method
3. ⏳ Test on multiple devices
4. ⏳ Upload to Google Play
5. ⏳ Submit for review
6. ⏳ Wait for approval (2-3 hours)
7. ⏳ Launch to production
8. ⏳ Monitor analytics and user feedback
9. ⏳ Plan future updates

---

**Last Updated**: February 2026
**Current Status**: App registered on Google Play Console
**App ID**: 4976304436219890258
**Package Name**: Ready for assignment
