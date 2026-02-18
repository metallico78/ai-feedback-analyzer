# AI Feedback Analyzer - API Documentation

## Overview
AI Feedback Analyzer es una API REST potente que analiza feedback con inteligencia artificial usando OpenAI GPT-3.5-turbo. Proporciona análisis de sentimiento, puntuación de calidad y sugerencias de mejora automatizadas.

## Base URL
```
https://ai-feedback-analyzer-production.up.railway.app
```

## Autenticación
Todas las solicitudes requieren una API Key en el header `X-API-Key`.

```bash
curl -H "X-API-Key: sk_YOUR_API_KEY" https://api.example.com/api/endpoint
```

## Rate Limiting
- Límite: 30 requests por minuto por API Key
- Headers de respuesta: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Endpoints

### 1. Registro de Usuario
**POST** `/api/auth/register`

Crea una nueva cuenta y genera una API Key.

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "id": "uuid",
  "email": "usuario@example.com",
  "api_key": "sk_...",
  "plan": "free",
  "requests_limit": 100
}
```

### 2. Login
**POST** `/api/auth/login`

Inicia sesión y obtiene credenciales.

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "id": "uuid",
  "email": "usuario@example.com",
  "api_key": "sk_...",
  "plan": "free",
  "requests_used": 5,
  "requests_limit": 100
}
```

### 3. Analizar Feedback
**POST** `/api/analyze`

Analiza un texto de feedback usando IA.

**Headers:**
```
X-API-Key: sk_YOUR_API_KEY
```

**Request Body:**
```json
{
  "text": "La aplicación funciona muy bien pero la interfaz podría ser más intuitiva."
}
```

**Response:**
```json
{
  "success": true,
  "id": "uuid",
  "sentiment": "positivo",
  "score": 7,
  "suggestions": [
    "Mejorar la navegación principal",
    "Simplificar el flujo de registro"
  ],
  "summary": "Feedback positivo con sugerencias de mejora en UX"
}
```

### 4. Obtener Analíticos
**GET** `/api/analytics`

Obtiene estadísticas de análisis del usuario.

**Headers:**
```
X-API-Key: sk_YOUR_API_KEY
```

**Response:**
```json
{
  "total": 50,
  "positive": 35,
  "negative": 8,
  "neutral": 7,
  "average": 7.2,
  "requests_used": 45,
  "requests_limit": 100
}
```

### 5. Perfil de Usuario
**GET** `/api/user/profile`

Obtiene información del perfil.

**Headers:**
```
X-API-Key: sk_YOUR_API_KEY
```

**Response:**
```json
{
  "id": "uuid",
  "email": "usuario@example.com",
  "api_key": "sk_...",
  "plan": "free",
  "requests_used": 45,
  "requests_limit": 100
}
```

### 6. Health Check
**GET** `/api/health`

Verifica el estado del servidor.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-18T17:00:00"
}
```

### 7. Crear Intención de Pago
**POST** `/api/payment/create-intent`

Crea una intención de pago con Stripe.

**Request Body:**
```json
{
  "amount": 9900,
  "email": "usuario@example.com",
  "description": "Upgrade a plan Pro"
}
```

**Response:**
```json
{
  "clientSecret": "pi_...",
  "paymentIntentId": "pi_..."
}
```

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Validación fallida |
| 401 | Unauthorized - API Key inválida |
| 429 | Too Many Requests - Rate limit excedido |
| 500 | Internal Server Error |

## Ejemplos de Uso

### cURL
```bash
curl -X POST https://ai-feedback-analyzer-production.up.railway.app/api/analyze \
  -H "X-API-Key: sk_YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Gran servicio pero necesita mejoras en latencia"}'
```

### Python
```python
import requests

headers = {"X-API-Key": "sk_YOUR_API_KEY"}
data = {"text": "El producto es excelente"}
response = requests.post(
    "https://ai-feedback-analyzer-production.up.railway.app/api/analyze",
    headers=headers,
    json=data
)
print(response.json())
```

### JavaScript
```javascript
const response = await fetch(
  'https://ai-feedback-analyzer-production.up.railway.app/api/analyze',
  {
    method: 'POST',
    headers: {
      'X-API-Key': 'sk_YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: 'Excelente producto con buen soporte'
    })
  }
);
const data = await response.json();
console.log(data);
```

## Características

- ✨ **Análisis IA Avanzado**: Usa GPT-3.5-turbo para análisis precisos
- 🚀 **Alto Rendimiento**: Caché inteligente y 4 workers Uvicorn
- 🔒 **Seguro**: Autenticación con API Keys
- ⚡ **Rate Limiting**: Protección contra abuso
- 💳 **Pagos Integrados**: Soporte de Stripe
- 📊 **Analíticos**: Estadísticas en tiempo real
- 🌐 **Multiplataforma**: Disponible como API REST

## Planes

| Plan | Requests/Mes | Precio | Características |
|------|--------------|--------|------------------|
| Free | 100 | $0 | Básico |
| Pro | 10,000 | $29 | Avanzado + Analíticos |
| Enterprise | Ilimitado | Custom | Soporte + API dedicada |

## Soporte

- **Email**: support@aifeedback.com
- **Docs**: https://github.com/metallico78/ai-feedback-analyzer
- **Issues**: https://github.com/metallico78/ai-feedback-analyzer/issues

## Licencia

MIT License - Ver LICENSE file para detalles.
