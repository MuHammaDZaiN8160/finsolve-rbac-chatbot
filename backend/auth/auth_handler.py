from jose import jwt, JWTError
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.config import SECRET_KEY, ALGORITHM
from backend.auth.users import USERS_DB

def authenticate_user(username: str, password: str):
    user = USERS_DB.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None

def create_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None