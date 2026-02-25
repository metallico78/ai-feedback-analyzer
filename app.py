from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
import openai
from dotenv import load_dotenv
import uuid
import hashlib
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base, Session, sessionmaker
import json
from functools import lru_cache
from typing import Dict, Optional
import time
import stripe

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./feedback.db")
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY', 'sk_test_PLACEHOLDER')

app = FastAPI(title="AI Feedback Analyzer v2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caché de resultados para optimizar
analysis_cache: Dict[str, tuple] = {}
CACHE_EXPIRY = 3600  # 1 hora

# Rate limiting
rate_limit_tracker: Dict[str, list] = {}
REQUESTS_PER_MINUTE = 30

# Base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

openai.api_key = OPENAI_API_KEY
stripe.api_key = STRIPE_API_KEY

# MODELOS BD
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    api_key = Column(String, unique=True)
    plan = Column(String, default="free")
    requests_used = Column(Integer, default=0)
    requests_limit = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    text = Column(String)
    sentiment = Column(String)
    score = Column(Integer)
    suggestions = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ESQUEMAS
class FeedbackRequest(BaseModel):
    text: str

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PaymentRequest(BaseModel):
    amount: int
    email: str
    description: str = "AI Feedback Analysis"

# FUNCIONES
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_pwd(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def gen_api_key():
    return "sk_" + hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:40]

def check_rate_limit(api_key: str) -> bool:
    """Implementa rate limiting"""
    current_time = time.time()
    if api_key not in rate_limit_tracker:
        rate_limit_tracker[api_key] = []
    
    # Limpiar timestamps antiguos (> 1 minuto)
    rate_limit_tracker[api_key] = [
        ts for ts in rate_limit_tracker[api_key] 
        if current_time - ts < 60
    ]
    
    if len(rate_limit_tracker[api_key]) >= REQUESTS_PER_MINUTE:
        return False
    
    rate_limit_tracker[api_key].append(current_time)
    return True

def get_cache_key(text: str) -> str:
    """Genera clave de caché"""
    return hashlib.md5(text.encode()).hexdigest()

def verify_api_key(x_api_key: str = Header(None), db: Session = Depends(get_db)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key requerida")
    
    if not check_rate_limit(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Máximo 30 requests/minuto")
    
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="API Key inválida")
    if user.requests_used >= user.requests_limit:
        raise HTTPException(status_code=429, detail="Límite de requests alcanzado")
    return user

def analyze_with_openai(text: str):
    """Analiza feedback con GPT - Optimizado"""
    # Verificar caché primero
    cache_key = get_cache_key(text)
    if cache_key in analysis_cache:
        cached_result, expiry_time = analysis_cache[cache_key]
        if time.time() < expiry_time:
            return cached_result
    
    prompt = f"""Analiza este feedback:
"{text}"
Responde en JSON válido:
{{
 "sentiment": "positivo" o "negativo" o "neutral",
 "score": 1-10,
 "suggestions": ["sugerencia 1", "sugerencia 2"],
 "summary": "resumen corto"
}}
Solo JSON."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
            timeout=30
        )
        result = response.choices[0].message.content
        # Guardar en caché
        analysis_cache[cache_key] = (result, time.time() + CACHE_EXPIRY)
        return result
    except Exception as e:
        return '{"sentiment": "neutral", "score": 5, "suggestions": ["Error"], "summary": "Error procesando"}'

# RUTAS
@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/api/status")
def status():
    return {"status": "ok", "message": "🤖 AI Feedback Analyzer API v2.0", "version": "2.0"}

@app.post("/api/auth/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email existe")
    
    user_id = str(uuid.uuid4())
    api_key = gen_api_key()
    
    new_user = User(
        id=user_id,
        email=user.email,
        password_hash=hash_pwd(user.password),
        api_key=api_key,
        plan="free"
    )
    db.add(new_user)
    db.commit()
    
    return {
        "success": True,
        "id": user_id,
        "email": user.email,
        "api_key": api_key,
        "plan": "free",
        "requests_limit": 100
    }

@app.post("/api/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or db_user.password_hash != hash_pwd(user.password):
        raise HTTPException(status_code=401, detail="Email o contraseña inválidos")
    
    return {
        "success": True,
        "id": db_user.id,
        "email": db_user.email,
        "api_key": db_user.api_key,
        "plan": db_user.plan,
        "requests_used": db_user.requests_used,
        "requests_limit": db_user.requests_limit
    }

@app.post("/api/analyze")
def analyze(req: FeedbackRequest, user: User = Depends(verify_api_key), db: Session = Depends(get_db)):
    if not req.text or len(req.text) < 5:
        raise HTTPException(status_code=400, detail="Texto muy corto (mínimo 5 caracteres)")
    
    if len(req.text) > 5000:
        raise HTTPException(status_code=400, detail="Texto muy largo (máximo 5000 caracteres)")
    
    result_str = analyze_with_openai(req.text)
    
    try:
        result = json.loads(result_str)
    except:
        result = {"sentiment": "neutral", "score": 5, "suggestions": [], "summary": "Error"}
    
    analysis_id = str(uuid.uuid4())
    analysis = Analysis(
        id=analysis_id,
        user_id=user.id,
        text=req.text,
        sentiment=result.get("sentiment", "neutral"),
        score=result.get("score", 5),
        suggestions=str(result.get("suggestions", []))
    )
    db.add(analysis)
    user.requests_used += 1
    db.commit()
    
    return {
        "success": True,
        "id": analysis_id,
        "sentiment": result.get("sentiment"),
        "score": result.get("score"),
        "suggestions": result.get("suggestions"),
        "summary": result.get("summary")
    }

@app.get("/api/analytics")
def analytics(user: User = Depends(verify_api_key), db: Session = Depends(get_db)):
    analyses = db.query(Analysis).filter(Analysis.user_id == user.id).all()
    
    total = len(analyses)
    if total == 0:
        return {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "average": 0,
            "requests_used": user.requests_used,
            "requests_limit": user.requests_limit
        }
    
    positive = len([a for a in analyses if "positiv" in a.sentiment.lower()])
    negative = len([a for a in analyses if "negativ" in a.sentiment.lower()])
    neutral = len([a for a in analyses if "neutral" in a.sentiment.lower()])
    avg = sum([a.score for a in analyses]) / total
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "average": round(avg, 2),
        "requests_used": user.requests_used,
        "requests_limit": user.requests_limit
    }

@app.get("/api/user/profile")
def profile(user: User = Depends(verify_api_key)):
    return {
        "id": user.id,
        "email": user.email,
        "api_key": user.api_key,
        "plan": user.plan,
        "requests_used": user.requests_used,
        "requests_limit": user.requests_limit
    }

@app.post('/api/payment/create-intent')
def create_payment_intent(payment: PaymentRequest):
    try:
        intent = stripe.PaymentIntent.create(
            amount=payment.amount,
            currency='usd',
            receipt_email=payment.email,
            metadata={'description': payment.description}
        )
        return {
            'clientSecret': intent.client_secret,
            'paymentIntentId': intent.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/api/payment/status/{payment_intent_id}')
def check_payment_status(payment_intent_id: str):
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            'status': intent.status,
            'amount': intent.amount,
            'amount_received': intent.amount_received
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
<<<<<<< HEAD
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hola desde ai-feedback-analyzer!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
=======

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
>>>>>>> 15018256b5eac04f96868a9d266c3091629a84a8
