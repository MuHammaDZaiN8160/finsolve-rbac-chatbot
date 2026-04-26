from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "finsolve-secret-key-123")
ALGORITHM = "HS256"

ROLE_PERMISSIONS = {
    "finance":     ["finance", "general"],
    "marketing":   ["marketing", "general"],
    "hr":          ["hr", "general"],
    "engineering": ["engineering", "general"],
    "c_level":     ["finance", "marketing", "hr", "engineering", "general"],
    "employee":    ["general"],
}