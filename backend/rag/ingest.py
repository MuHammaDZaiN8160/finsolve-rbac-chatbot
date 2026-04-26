from dotenv import load_dotenv
import os
load_dotenv()

from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DEPARTMENTS = ["finance", "marketing", "hr", "engineering", "general"]

def load_file(file_path, dept):
    ext = os.path.splitext(file_path)[1].lower()
    docs = []
    try:
        if ext in [".md", ".txt"]:
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
        elif ext == ".csv":
            loader = CSVLoader(file_path, encoding="utf-8")
            docs = loader.load()
        else:
            print(f"Skipping unsupported file: {file_path}")
            return []
        for doc in docs:
            doc.metadata["department"] = dept
            doc.metadata["source"] = os.path.basename(file_path)
        return docs
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def ingest():
    all_docs = []
    for dept in DEPARTMENTS:
        path = f"data/{dept}"
        if not os.path.exists(path):
            print(f"Folder not found: {path}, skipping...")
            continue
        files = os.listdir(path)
        if not files:
            print(f"No files in {path}, skipping...")
            continue
        for file in files:
            file_path = os.path.join(path, file)
            print(f"Loading: {file_path}")
            docs = load_file(file_path, dept)
            all_docs.extend(docs)

    if not all_docs:
        print("No documents found.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)
    print(f"Creating embeddings for {len(chunks)} chunks...")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("./faiss_db")
    print(f"✅ Done! Ingested {len(chunks)} chunks into FAISS.")

if __name__ == "__main__":
    ingest()