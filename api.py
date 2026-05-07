from fastapi import FastAPI
from pydantic import BaseModel

from app import agent, summarize, explain, generate_questions

app_api = FastAPI()


# --- Request Model ---
class TextRequest(BaseModel):
    text: str


# --- Health Check ---
@app_api.get("/")
def home():
    return {
        "message": "AI Agent API is running 🚀"
    }


# --- Summarize Endpoint ---
@app_api.post("/summarize")
def summarize_api(request: TextRequest):
    result = summarize(request.text)

    return {
        "success": True,
        "tool": "summarize",
        "result": result,
        "input_length": len(request.text)
    }


# --- Explain Endpoint ---
@app_api.post("/explain")
def explain_api(request: TextRequest):
    result = explain(request.text)

    return {
        "success": True,
        "tool": "explain",
        "result": result,
        "input_length": len(request.text)
    }


# --- Questions Endpoint ---
@app_api.post("/questions")
def questions_api(request: TextRequest):
    result = generate_questions(request.text)

    return {
        "success": True,
        "tool": "questions",
        "result": result,
        "input_length": len(request.text)
    }


# --- Main Agent Endpoint ---
@app_api.post("/agent")
def agent_api(request: TextRequest):

    result = agent(request.text)

    # 🧠 مهم: نرجّع نفس JSON بدون تعديل
    return result
