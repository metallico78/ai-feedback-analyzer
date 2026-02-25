# Guía de Publicación en Google Play Store y Apple App Store

## 🚀 Prerequisitos

Para publicar tu app en ambas tiendas, necesitarás:

### Hardware y Software
- Node.js v14+
- React Native CLI
- Android Studio (para Android)
- Xcode (para iOS - solo en macOS)
- Git

### Cuentas Requeridas
1. **Google Play Developer Account** - $25 USD (una sola vez)
2. **Apple Developer Program** - $99 USD/año
3. Cuenta de GitHub (ya tienes)
4. Cuenta de Firebase (recomendado para analytics)

---

## 📱 Paso 1: Configurar Proyecto React Native

### Crear el proyecto
```bash
npx react-native init AIFeedbackAnalyzer
cd AIFeedbackAnalyzer
```

### Instalar dependencias necesarias
```bash
npm install axios react-native-dotenv react-native-gesture-handler react-native-reanimated
npm install --save-dev @react-native-community/eslint-config
```

### Estructura del proyecto
```
AIFeedbackAnalyzer/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.js
│   │   ├── AnalysisScreen.js
│   │   └── ResultsScreen.js
│   ├── services/
│   │   ├── api.js
│   │   └── config.js
│   ├── components/
│   │   ├── FeedbackForm.js
│   │   └── ResultCard.js
│   └── App.js
├── android/
├── ios/
├── package.json
└── app.json
```

---

## 🤖 Paso 2: Publicar en Google Play Store

### 2.1 Crear Google Play Developer Account
1. Ir a https://play.google.com/console
2. Crear nueva cuenta de desarrollador
3. Pagar $25 USD
4. Completar información del perfil

### 2.2 Generar APK Firmado

#### A. Crear Keystore
```bash
keytool -genkey -v -keystore my-release-key.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias my-key-alias
```

#### B. Configurar gradle.properties
```properties
FLAVOR=release
ORG_GRADLE_PROJECT_MY_RELEASE_STORE_FILE=my-release-key.keystore
ORG_GRADLE_PROJECT_MY_RELEASE_KEY_ALIAS=my-key-alias
ORG_GRADLE_PROJECT_MY_RELEASE_STORE_PASSWORD=<password>
ORG_GRADLE_PROJECT_MY_RELEASE_KEY_PASSWORD=<password>
```

#### C. Build APK
```bash
cd android
./gradlew clean bundleRelease
cd ..
```

El archivo generado estará en:
`android/app/build/outputs/bundle/release/app-release.aab`

### 2.3 Subir a Google Play Console
1. Ve a Google Play Console
2. Crea nueva app
3. Completa:
   - Nombre: "AI Feedback Analyzer"
   - Categoría: "Productivity" o "Tools"
   - Tipo de contenido: "Aplicación"
4. En "Versión": sube el `.aab`
5. Completa toda la información de listings
6. Somete para revisión

### 2.4 Información Requerida para Google Play
- **Título**: "AI Feedback Analyzer - IA Inteligente"
- **Descripción breve**: "Analiza feedback con IA avanzada (max 80 caracteres)"
- **Descripción completa**: Descripción detallada (max 4000 caracteres)
- **Categoría**: Productividad
- **Privacidad**: URL de política de privacidad
- **Email de contacto**: tu@email.com
- **Website**: URL de tu sitio
- **Screenshots**: 2-8 screenshots (1080x1920px)
- **Ícono de app**: 512x512px
- **Feature gráfico**: 1024x500px

---

## 🍎 Paso 3: Publicar en Apple App Store

### 3.1 Crear Apple Developer Account
1. Ir a https://developer.apple.com
2. Crear Apple ID si no tienes
3. Enroll en Apple Developer Program ($99/año)
4. Completar perfil de desarrollador

### 3.2 Configurar Xcode
```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcode-select --reset
```

### 3.3 Crear Certificate y Provisioning Profile
1. En Apple Developer Portal:
   - Certificates, Identifiers & Profiles
   - Create App ID
   - Create iOS Distribution Certificate
   - Create App Store Provisioning Profile

### 3.4 Build IPA para iOS

#### A. Configurar Xcode Project
```bash
cd ios
pod install
cd ..
```

#### B. Build Release
```bash
xcodebuild -workspace ios/AIFeedbackAnalyzer.xcworkspace \
  -scheme AIFeedbackAnalyzer \
  -configuration Release \
  -derivedDataPath build \
  -archivePath build/AIFeedbackAnalyzer.xcarchive \
  archive
```

#### C. Exportar IPA
```bash
xcodebuild -exportArchive \
  -archivePath build/AIFeedbackAnalyzer.xcarchive \
  -exportOptionsPlist ios/ExportOptions.plist \
  -exportPath build/
```

### 3.5 Subir a App Store Connect
1. Ve a https://appstoreconnect.apple.com
2. Create New App
3. Completa información:
   - Nombre: "AI Feedback Analyzer"
   - SKU: "com.tuempresa.aifeedback"
   - Bundle ID: selecciona el que creaste
4. Completa App Information
5. Sube IPA usando Transporter o Xcode

### 3.6 Información Requerida para App Store
- **Nombre**: "AI Feedback Analyzer"
- **Subtitle**: "Análisis IA Inteligente"
- **Descripción**: Descripción completa
- **Palabras clave**: "AI, feedback, analysis, IA"
- **Categoría**: "Productivity"
- **Privacidad**: URL de política de privacidad
- **Soporte**: Email de soporte
- **Website**: URL del sitio
- **Screenshots**: 2-5 screenshots (para cada device)
- **App Icon**: 1024x1024px
- **Preview Video**: (opcional) video de demostración

---

## 📋 Checklist de Publicación

### Antes de Publicar
- [ ] App funciona en Android e iOS
- [ ] Política de privacidad publicada
- [ ] Términos de servicio completados
- [ ] Todas las APIs funcionan correctamente
- [ ] Testing en dispositivos reales
- [ ] Screenshots de alta calidad
- [ ] Descripción clara y atractiva
- [ ] Logo y assets de branding
- [ ] Email de soporte funcional

### Google Play Store
- [ ] Generar keystore firmado
- [ ] Build AAB release
- [ ] Completar app listing
- [ ] Definir precio y distribución
- [ ] Cumplimiento de políticas
- [ ] Enviar para revisión
- [ ] Esperar aprobación (48-72 horas)

### Apple App Store
- [ ] Crear desarrollo certificates
- [ ] Crear provisioning profiles
- [ ] Build IPA signed
- [ ] Completar app information
- [ ] Completar app preview
- [ ] Build and Release version
- [ ] Enviar para revisión
- [ ] Esperar aprobación (24-48 horas)

---

## 🔗 Links Útiles

### Google Play
- https://play.google.com/console
- https://developer.android.com/distribute
- https://support.google.com/googleplay/android-developer

### Apple App Store
- https://appstoreconnect.apple.com
- https://developer.apple.com
- https://help.apple.com/app-store-connect

### React Native
- https://reactnative.dev/docs/signed-apk-android
- https://reactnative.dev/docs/publishing-to-app-store
- https://reactnative.dev/docs/running-on-device

---

## 💡 Tips y Mejores Prácticas

1. **Versioning**: Mantén consistencia entre versión de código y tienda
2. **Release Notes**: Escribe notas de lanzamiento descriptivas
3. **Testing**: Usa TestFlight (iOS) y Play Console internal testing (Android)
4. **Monetización**: Planifica estrategia de ingresos antes de publicar
5. **Analytics**: Integra Firebase o Mixpanel para tracking
6. **Updates**: Planifica actualizaciones regulares
7. **Ratings**: Implementa solicitud de ratings en app
8. **Deep Linking**: Configura deep links para marketing

---

## 🆘 Troubleshooting

### Android
- **Signature error**: Verifica gradle.properties
- **Gradle sync failed**: Actualiza gradle en android/gradle/wrapper
- **Build fails**: Limpia con `./gradlew clean`

### iOS
- **Code signing error**: Verifica provisioning profiles en Xcode
- **Pod install error**: `rm -rf ios/Pods && pod install`
- **Build error**: Limpiar con `xcodebuild clean`

---

## 📞 Soporte

Para ayuda adicional:
- GitHub Issues: https://github.com/metallico78/ai-feedback-analyzer/issues
- React Native Community: https://reactnativecommunity.org
- Stack Overflow: etiqueta con `react-native`
