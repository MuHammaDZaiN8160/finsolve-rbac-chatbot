from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.auth.auth_handler import decode_token
from backend.rag.retriever import retrieve_docs
from backend.rag.generator import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    token: str

@router.post("/chat")
def chat(request: ChatRequest):
    # Validate token
    payload = decode_token(request.token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    role = payload["role"]
    username = payload["sub"]
    
    print(f"User: {username} | Role: {role} | Query: {request.query}")
    
    # Retrieve relevant docs based on role
    docs = retrieve_docs(request.query, role)
    
    # Generate response
    answer = generate_response(request.query, docs, role)
    
    # Extract source names
    sources = list(set([
        d.metadata.get("source", "Unknown") for d in docs
    ]))
    
    return {
        "answer": answer,
        "sources": sources,
        "role": role,
        "username": username
    }