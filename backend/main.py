from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.auth.auth_handler import authenticate_user, create_token
from backend.routers.chat import router as chat_router

app = FastAPI(
    title="FinSolve RBAC Chatbot API",
    description="Role-Based Access Control Chatbot for FinSolve Technologies",
    version="1.0.0"
)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/auth/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_token(user["username"], user["role"])
    
    return {
        "token": token,
        "role": user["role"],
        "username": user["username"],
        "message": f"Welcome {user['username']}! You are logged in as {user['role']}."
    }

app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "FinSolve Chatbot API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}