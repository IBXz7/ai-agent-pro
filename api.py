from fastapi import FastAPI
from pydantic import BaseModel
from app import chat

app_api = FastAPI()


# --- Request Model ---
class ChatRequest(BaseModel):
    message: str
    history: list = []


# --- Root ---
@app_api.get("/")
def home():
    return {"message": "AI Chat API is running 🚀"}


# --- Chat Endpoint ---
@app_api.post("/chat")
def chat_api(request: ChatRequest):

    result = chat(request.message, request.history)

    return {
        "success": True,
        "response": result
    }
