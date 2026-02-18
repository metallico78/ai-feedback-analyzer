from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
import uuid
import hashlib
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base, Session, sessionmaker
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./feedback.db")

app = FastAPI(title="AI Feedback Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

openai.api_key = OPENAI_API_KEY

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

def verify_api_key(x_api_key: str = Header(None), db: Session = Depends(get_db)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key requerida")
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="API Key inválida")
    if user.requests_used >= user.requests_limit:
        raise HTTPException(status_code=429, detail="Límite alcanzado")
    return user

def analyze_with_openai(text: str):
    """Analiza feedback con GPT"""
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
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return '{"sentiment": "neutral", "score": 5, "suggestions": ["Error"], "summary": "Error procesando"}'

# RUTAS
@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/api/status")
def status():
    return {"status": "ok", "message": "🤖 AI Feedback Analyzer API v1.0"}

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
        raise HTTPException(status_code=400, detail="Texto muy corto")
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
