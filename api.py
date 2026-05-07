from fastapi import FastAPI
from pydantic import BaseModel

from app import agent, summarize, explain, generate_questions

app_api = FastAPI()


class TextRequest(BaseModel):
    text: str


@app_api.get("/")
def home():
    return {"message": "AI Agent API is running 🚀"}


@app_api.post("/summarize")
def summarize_api(request: TextRequest):
    return {
        "success": True,
        "tool": "summarize",
        "result": summarize(request.text),
        "input_length": len(request.text)
    }


@app_api.post("/explain")
def explain_api(request: TextRequest):
    return {
        "success": True,
        "tool": "explain",
        "result": explain(request.text),
        "input_length": len(request.text)
    }


@app_api.post("/questions")
def questions_api(request: TextRequest):
    return {
        "success": True,
        "tool": "questions",
        "result": generate_questions(request.text),
        "input_length": len(request.text)
    }


@app_api.post("/agent")
def agent_api(request: TextRequest):
    return agent(request.text)
