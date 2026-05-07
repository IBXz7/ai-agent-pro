# 🤖 AI Agent Pro

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter-orange)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen)

---

## 🚀 Overview

**AI Agent Pro** is a lightweight AI-powered chat system that connects a modern web UI with a FastAPI backend and OpenRouter LLMs.

It simulates a simplified ChatGPT-style experience with:
- Tool-based reasoning
- Context-aware responses
- Cloud deployment

---

## 💬 Live Demo

- 🌐 UI: https://ai-agent-pro-ui.onrender.com
- ⚙️ API: https://ai-agent-pro.onrender.com/docs

---

## 🧠 Key Features

- 💬 Chat-based AI assistant
- 🧠 Context-aware responses (history support)
- ✍️ Text summarization
- 📘 Explanation generation
- ❓ Question generation
- ⚡ OpenRouter LLM integration
- 🌐 REST API with FastAPI
- ☁️ Fully deployed on Render

---

## 🏗️ System Architecture

text id="arch_pro"
User
 ↓
Streamlit UI
 ↓
FastAPI Backend
 ↓
OpenRouter LLM
 ↓
AI Response

--- 

##📡 API Reference
POST /chat

Send a message to the AI agent.

Request
{
  "message": "Explain machine learning",
  "history": []
}
Response
{
  "success": true,
  "response": "Machine learning is a subset of AI that allows systems to learn from data..."
}

---

##⚙️ Tech Stack
Python 🐍
FastAPI ⚡
Streamlit 🎨
OpenRouter LLM 🧠
Render ☁️
Requests HTTP Client

---

##🔐 Environment Variables

Required for deployment:

OPENROUTER_API_KEY=your_api_key_here

---

##▶️ Local Setup for macOS
1. Clone repository
git clone https://github.com/IBXz7/ai-agent-pro.git
cd ai-agent-pro
2. Install dependencies
pip install -r requirements.txt
3. Run backend
uvicorn api:app_api --reload
4. Run frontend
streamlit run ui.py

---

##☁️ Deployment

This project is deployed on Render with:

🔵 Backend service (FastAPI)
- Runs FastAPI
- Handles /chat endpoint
- Connects to OpenRouter API
🟢 Frontend service (Streamlit)
- Runs Streamlit UI
- Sends requests to backend API
- Displays chat interface

Environment variables for API keys
 Roadmap

---

## 🚀 Future improvements planned:

🧠 Smarter tool routing (LLM-based decision making)
💾 Persistent chat memory (database integration)
⚡ Streaming responses (real-time typing effect)
🔐 User authentication system
🎨 Improved UI/UX (chat bubbles + dark mode)
👨‍💻 Author

Developed by Omar Almutairi

📄 License

This project is for educational and learning purposes.
