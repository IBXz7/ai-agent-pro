from fastapi import FastAPI
from pydantic import BaseModel
from app import summarize, explain, generate_questions, agent

app_api = FastAPI()

# --- Request Model ---
class TextRequest(BaseModel):
    text: str

# --- Endpoints ---

@app_api.get("/")
def home():
    return {"message": "AI Agent API is running 🚀"}

@app_api.post("/summarize")
def summarize_api(request: TextRequest):
    result = summarize(request.text)
    return {
    "success": True,
    "tool": "summarize",
    "input_length": len(request.text),
    "output": result,
    "message": "Summarization completed"
}

@app_api.post("/explain")
def explain_api(request: TextRequest):
    result = explain(request.text)
    return {
    "success": True,
    "tool": "explain",
    "input_length": len(request.text),
    "output": result,
    "message": "Explanation generated"
}

@app_api.post("/questions")
def questions_api(request: TextRequest):
    result = generate_questions(request.text)
    return {
    "success": True,
    "tool": "questions",
    "input_length": len(request.text),
    "output": result,
    "message": "Questions generated"
}

@app_api.post("/agent")
def agent_api(request: TextRequest):
    result = agent(request.text)
    return {
    "success": True,
    "tool": "agent",
    "input_length": len(request.text),
    "output": result,
    "message": "Agent response generated"
}