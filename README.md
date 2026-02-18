# 🤖 AI Feedback Analyzer

## Descripción

AI Feedback Analyzer es una aplicación web que utiliza inteligencia artificial (OpenAI GPT) para analizar feedback de usuarios e integra procesamiento de pagos con Stripe.

## 🚀 Características

- ✅ **Análisis de Feedback con IA** - Usa OpenAI GPT para análisis inteligente
- 💳 **Procesamiento de Pagos** - Integración completa con Stripe
- 🎨 **Interfaz Moderna** - UI profesional y responsive
- 📊 **Base de Datos** - SQLAlchemy con SQLite
- 🔒 **Seguro** - Validaciones y manejo de errores
- 🌐 **API REST** - Endpoints para frontend/mobile

## 📦 Tecnologías

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **IA**: OpenAI GPT API
- **Pagos**: Stripe API
- **Base de Datos**: SQLite + SQLAlchemy
- **Deployment**: Railway
- **Repositorio**: GitHub

## 🛠️ Instalación Local

### Prerrequisitos

- Python 3.8+
- Cuenta de OpenAI con API Key
- Cuenta de Stripe con API Key

### Pasos

1. **Clonar repositorio**
```bash
git clone https://github.com/metallico78/ai-feedback-analyzer.git
cd ai-feedback-analyzer
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
Crea un archivo `.env` con:
```
OPENAI_API_KEY=tu_api_key_de_openai
STRIPE_API_KEY=tu_api_key_de_stripe
DATABASE_URL=sqlite:///./feedback.db
```

4. **Ejecutar aplicación**
```bash
python app.py
```

5. **Abrir en navegador**
```
http://localhost:8000
```

## 📡 API Endpoints

### Análisis de Feedback
```http
POST /api/analyze
Content-Type: application/json

{
  "feedback": "El producto es excelente",
  "api_key": "tu_api_key"
}
```

**Respuesta**:
```json
{
  "analysis": "Análisis del feedback...",
  "sentiment": "positive"
}
```

### Crear Intención de Pago
```http
POST /api/payment/create-intent
Content-Type: application/json

{
  "amount": 999,
  "email": "usuario@email.com",
  "description": "AI Feedback Analysis"
}
```

**Respuesta**:
```json
{
  "clientSecret": "pi_xxx_secret_xxx",
  "paymentIntentId": "pi_xxx"
}
```

### Verificar Estado de Pago
```http
GET /api/payment/status/{payment_intent_id}
```

**Respuesta**:
```json
{
  "status": "succeeded",
  "amount": 999,
  "amount_received": 999
}
```

## 🔧 Configuración en Producción

### Railway Deployment

1. **Conectar repositorio GitHub**
2. **Configurar variables de entorno**:
   - `OPENAI_API_KEY`
   - `STRIPE_API_KEY`
3. **Deploy automático** activado

### Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|----------|
| `OPENAI_API_KEY` | API Key de OpenAI | `sk-proj-...` |
| `STRIPE_API_KEY` | API Key de Stripe | `sk_live_...` o `sk_test_...` |
| `DATABASE_URL` | URL base de datos | `sqlite:///./feedback.db` |

## 📝 Uso

1. **Ingresar feedback** en el formulario
2. **Click en "Analizar con IA"**
3. **Ver resultados** del análisis
4. **(Opcional)** **Procesar pago** con tarjeta de crédito

## 🔐 Seguridad

- ❌ **No subir API Keys** al repositorio
- ✅ Usar **variables de entorno**
- ✅ **HTTPS** en producción
- ✅ **Validaciones** en frontend y backend
- ✅ **Sanitización** de inputs

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - Ver archivo `LICENSE` para más detalles

## 👤 Autor

**metallico78**
- GitHub: [@metallico78](https://github.com/metallico78)

## 🙏 Agradecimientos

- OpenAI por su API de GPT
- Stripe por su sistema de pagos
- Railway por el hosting

## 📞 Soporte

Para soporte, crear un [Issue en GitHub](https://github.com/metallico78/ai-feedback-analyzer/issues)

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!
