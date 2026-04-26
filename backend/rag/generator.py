from dotenv import load_dotenv
import os
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

PROMPT = ChatPromptTemplate.from_template("""
You are FinSolve's internal AI assistant helping employees get information.
Answer using ONLY the context provided below.
If the answer is not in the context, say: "I don't have access to that information."
Do NOT make up any information.

User Role: {role}

Context:
{context}

Question: {question}

Provide a clear, helpful answer and always mention the source document names at the end.
""")

def generate_response(query: str, docs: list, role: str) -> str:
    if not docs:
        return "I could not find any relevant information for your query in the documents you have access to."
    
    context = "\n\n".join([
        f"[Source: {d.metadata.get('source', 'Unknown')} | Department: {d.metadata.get('department', 'Unknown')}]\n{d.page_content}"
        for d in docs
    ])
    
    chain = PROMPT | llm
    result = chain.invoke({
        "role": role,
        "context": context,
        "question": query
    })
    
    return result.content