# # main.py
# from fastapi import FastAPI, Depends, HTTPException, Header
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from database import SessionLocal, engine
# from models import Base, User
# from dotenv import load_dotenv
# import secrets, os, requests

# # Load .env variables
# load_dotenv()

# # Create database tables (if not exist)
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="FastAPI Gemini + HuggingFace Project")

# # --------------------------
# # Database Dependency
# # --------------------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # --------------------------
# # Pydantic Schemas
# # --------------------------
# class RegisterModel(BaseModel):
#     username: str
#     password: str

# class LoginModel(BaseModel):
#     username: str
#     password: str

# class ChatRequest(BaseModel):
#     prompt: str

# class HuggingFaceInput(BaseModel):
#     text: str

# # --------------------------
# # Register User
# # --------------------------
# @app.post("/register")
# def register(user: RegisterModel, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.username == user.username).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")

#     new_user = User(username=user.username, password=user.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User registered successfully"}

# # --------------------------
# # Login User + Generate Token
# # --------------------------
# @app.post("/login")
# def login(user: LoginModel, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or db_user.password != user.password:
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     # Generate token
#     token = secrets.token_hex(16)
#     db_user.token = token
#     db.commit()
#     db.refresh(db_user)
#     return {"message": "Login successful", "token": token}

# # --------------------------
# # Authenticate User (via Token)
# # --------------------------
# def authenticate_user(token: str = Header(None), db: Session = Depends(get_db)):
#     """
#     Expect header: token: <user-token>
#     Returns the DB user object if token valid, otherwise raises 401.
#     """
#     if not token:
#         raise HTTPException(status_code=401, detail="Token missing")
#     db_user = db.query(User).filter(User.token == token).first()
#     if not db_user:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return db_user

# # --------------------------
# # Gemini API Chat Route
# # --------------------------
# @app.post("/chat")
# def chat_with_gemini(request: ChatRequest, db_user: User = Depends(authenticate_user)):
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise HTTPException(status_code=500, detail="Gemini API key missing in .env")

#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
#     headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
#     body = {
#         "contents": [
#             {
#                 "parts": [{"text": request.prompt}]
#             }
#         ]
#     }

#     resp = requests.post(url, headers=headers, json=body, timeout=30)
#     if resp.status_code != 200:
#         raise HTTPException(status_code=500, detail=f"Gemini API error: {resp.text}")

#     return {
#         "username": db_user.username,
#         "prompt": request.prompt,
#         "reply": resp.json()
#     }

# # --------------------------
# # Hugging Face Endpoint
# # --------------------------
# @app.post("/huggingface")
# def query_huggingface(data: HuggingFaceInput, db_user: User = Depends(authenticate_user)):
#     hf_key = os.getenv("HUGGINGFACE_API_KEY")
#     if not hf_key:
#         raise HTTPException(status_code=500, detail="HuggingFace API key missing in .env")

#     # Choose model endpoint (example: gpt2 - you can change to any inference model)
#     url = "https://api-inference.huggingface.co/models/gpt2"
#     headers = {"Authorization": f"Bearer {hf_key}"}
#     payload = {"inputs": data.text}

#     resp = requests.post(url, headers=headers, json=payload, timeout=30)
#     if resp.status_code != 200:
#         # return HF full message for debugging
#         raise HTTPException(status_code=500, detail=f"Hugging Face API error: {resp.text}")

#     return {
#         "username": db_user.username,
#         "input": data.text,
#         "reply": resp.json()
#     }

# # --------------------------
# # Root Route
# # --------------------------
# @app.get("/")
# def home():
#     return {"message": "Welcome — FastAPI Gemini + HuggingFace Project by Junaid!"}
# from fastapi import FastAPI, Depends, HTTPException, Header
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from database import SessionLocal, engine
# from models import Base, User
# from dotenv import load_dotenv
# import secrets, os, requests

# # --------------------------
# # Load environment variables
# # --------------------------
# load_dotenv()

# # Create DB tables if not exist
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="FastAPI Gemini + HuggingFace Project")

# # --------------------------
# # Database Dependency
# # --------------------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # --------------------------
# # Schemas
# # --------------------------
# class RegisterModel(BaseModel):
#     username: str
#     password: str

# class LoginModel(BaseModel):
#     username: str
#     password: str

# class ChatRequest(BaseModel):
#     prompt: str

# class HuggingFaceInput(BaseModel):
#     text: str

# # --------------------------
# # Helper: Uniform Response
# # --------------------------
# def success_response(message: str, data: dict = None):
#     return {"status": "success", "message": message, "data": data or {}}

# def error_response(message: str):
#     return {"status": "error", "message": message}

# # --------------------------
# # Register User
# # --------------------------
# @app.post("/register")
# def register(user: RegisterModel, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.username == user.username).first()
#     if existing_user:
#         return error_response("Username already exists")

#     new_user = User(username=user.username, password=user.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return success_response("User registered successfully")

# # --------------------------
# # Login User + Generate Token
# # --------------------------
# @app.post("/login")
# def login(user: LoginModel, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or db_user.password != user.password:
#         return error_response("Invalid username or password")

#     token = secrets.token_hex(16)
#     db_user.token = token
#     db.commit()
#     db.refresh(db_user)

#     return success_response("Login successful", {"token": token})

# # --------------------------
# # Authenticate User
# # --------------------------
# def authenticate_user(token: str = Header(None), db: Session = Depends(get_db)):
#     if not token:
#         raise HTTPException(status_code=401, detail="Token missing")

#     db_user = db.query(User).filter(User.token == token).first()
#     if not db_user:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     return db_user

# # --------------------------
# # Gemini API Chat Route (timeout fixed: 120s)
# # --------------------------
# @app.post("/chat")
# def chat_with_gemini(request: ChatRequest, db_user: User = Depends(authenticate_user)):
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         return error_response("Gemini API key missing in .env")

#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
#     headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
#     body = {"contents": [{"parts": [{"text": request.prompt}]}]}

#     try:
#         resp = requests.post(url, headers=headers, json=body, timeout=120)
#     except requests.exceptions.Timeout:
#         return error_response("Request to Gemini API timed out (waited 120 seconds). Try again.")

#     if resp.status_code != 200:
#         return error_response(f"Gemini API error: {resp.text}")

#     return success_response(
#         "Gemini response generated successfully",
#         {
#             "username": db_user.username,
#             "prompt": request.prompt,
#             "reply": resp.json()
#         }
#     )

# # --------------------------
# # Hugging Face — LLaMA 3.3 Model
# # --------------------------
# @app.post("/huggingface")
# def query_huggingface(data: HuggingFaceInput, db_user: User = Depends(authenticate_user)):
#     hf_key = os.getenv("HF_TOKEN")
#     if not hf_key:
#         return error_response("HuggingFace API key missing in .env")

#     model_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"
#     headers = {"Authorization": f"Bearer {hf_key}", "Content-Type": "application/json"}
#     payload = {"inputs": data.text}

#     try:
#         resp = requests.post(model_url, headers=headers, json=payload, timeout=120)
#     except requests.exceptions.Timeout:
#         return error_response("Request to Hugging Face API timed out (120 seconds).")

#     if resp.status_code == 503:
#         return error_response("Model is loading on Hugging Face. Please retry after a few seconds.")

#     if resp.status_code != 200:
#         return error_response(f"Hugging Face API error: {resp.text}")

#     result = resp.json()
#     output = ""

#     if isinstance(result, list) and len(result) > 0:
#         output = result[0].get("generated_text", str(result))
#     else:
#         output = str(result)

#     return success_response(
#         "Hugging Face response generated successfully",
#         {
#             "username": db_user.username,
#             "model_used": "meta-llama/Llama-3.3-70B-Instruct",
#             "input": data.text,
#             "reply": output
#         }
#     )

# # --------------------------
# # Root Route
# # --------------------------
# @app.get("/")
# def home():
#     return success_response("Welcom — FastAPI Gemini + HuggingFace Project by Junaid!")

from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from dotenv import load_dotenv
import secrets, os, requests

# =====================================================
# Load environment variables
# =====================================================
load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Gemini + Hugging Face Router Project")

# =====================================================
# Database Dependency
# =====================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# Schemas
# =====================================================
class RegisterModel(BaseModel):
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    prompt: str

class HuggingFaceRouterRequest(BaseModel):
    prompt: str
    max_tokens: int = 500  # optional default

# =====================================================
# Helper Responses
# =====================================================
def success_response(message: str, data: dict = None):
    return {"status": "success", "message": message, "data": data or {}}

def error_response(message: str):
    return {"status": "error", "message": message, "data": {}}

# =====================================================
# User Register / Login
# =====================================================
@app.post("/register")
def register(user: RegisterModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return error_response("Username already exists")

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return success_response("User registered successfully")

@app.post("/login")
def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.password != user.password:
        return error_response("Invalid username or password")

    token = secrets.token_hex(16)
    db_user.token = token
    db.commit()
    return success_response("Login successful", {"token": token})

# =====================================================
# Token Authentication
# =====================================================
def authenticate_user(token: str = Header(None), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    db_user = db.query(User).filter(User.token == token).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return db_user

# =====================================================
# Gemini Endpoint (120 s timeout)
# =====================================================
@app.post("/chat/gemini")
def chat_with_gemini(request: ChatRequest, db_user: User = Depends(authenticate_user)):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return error_response("Gemini API key missing in .env")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    body = {"contents": [{"parts": [{"text": request.prompt}]}]}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=120)
    except requests.exceptions.Timeout:
        return error_response("Request to Gemini API timed out (120 s).")

    if resp.status_code != 200:
        return error_response(f"Gemini API error: {resp.text}")

    return success_response(
        "Gemini response generated successfully",
        {
            "username": db_user.username,
            "prompt": request.prompt,
            "reply": resp.json()
        }
    )

# =====================================================
# Hugging Face Router Endpoint (Llama-3.3-70B)
# =====================================================
@app.post("/chat/huggingface")
def chat_with_huggingface(request: HuggingFaceRouterRequest, db_user: User = Depends(authenticate_user)):
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        return error_response("Hugging Face API key missing in .env")

    MODEL_ID = "meta-llama/Llama-3.3-70B-Instruct"
    ENDPOINT = "https://router.huggingface.co/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": request.prompt}],
        "max_tokens": request.max_tokens
    }

    try:
        response = requests.post(ENDPOINT, headers=HEADERS, json=payload, timeout=120)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return error_response("Request to Hugging Face API timed out (120 s).")
    except requests.exceptions.RequestException as e:
        return error_response(f"Error calling Hugging Face API: {e}")

    data = response.json()
    try:
        generated_text = data["choices"][0]["message"]["content"]
    except Exception:
        return error_response(f"Unexpected response format: {data}")

    return success_response(
        "Hugging Face response generated successfully",
        {
            "username": db_user.username,
            "model_used": MODEL_ID,
            "prompt": request.prompt,
            "reply": generated_text
        }
    )

# =====================================================
# Root Route
# =====================================================
@app.get("/")
def home():
    return success_response("Welcome — FastAPI Gemini + Hugging Face Router Project by Junaid!")
