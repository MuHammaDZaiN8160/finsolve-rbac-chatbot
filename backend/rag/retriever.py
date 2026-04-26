from dotenv import load_dotenv
import os
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.config import ROLE_PERMISSIONS

def retrieve_docs(query: str, role: str, k: int = 5):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        "./faiss_db",
        embeddings,
        allow_dangerous_deserialization=True
    )
    allowed = ROLE_PERMISSIONS.get(role, ["general"])
    print(f"Role: {role} | Allowed departments: {allowed}")
    results = vectorstore.similarity_search(query, k=5)
    filtered = [doc for doc in results if doc.metadata.get("department") in allowed]
    return filtered[:3]