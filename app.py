import requests
import os

# --- OpenRouter Config ---

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


# --- LLM Request ---
def ask_llm(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        data = response.json()

        
        if "error" in data:
            return f"OpenRouter Error: {data['error']}"

        
        if "choices" not in data:
            return f"Unexpected response: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"LLM Error: {str(e)}"


# --- Tools ---

def summarize(text):
    prompt = f"Summarize this text clearly:\n\n{text}"
    return ask_llm(prompt)


def explain(text):
    prompt = f"Explain this clearly and simply:\n\n{text}"
    return ask_llm(prompt)


def generate_questions(text):
    prompt = f"Generate 3 study questions from this text:\n\n{text}"
    return ask_llm(prompt)


# --- Tool Registry ---
TOOLS = {
    "summarize": summarize,
    "explain": explain,
    "questions": generate_questions
}


# --- Tool Decision ---
def decide_tool(user_input):
    text = user_input.lower()

    if "summary" in text or "summarize" in text:
        return "summarize"

    if "explain" in text:
        return "explain"

    if "question" in text:
        return "questions"

    return "summarize"


# --- Agent ---
def agent(user_input):
    try:
        tool = decide_tool(user_input)

        if tool not in TOOLS:
            return {
                "success": False,
                "tool": "unknown",
                "result": "Unknown tool",
                "input_length": len(user_input)
            }

        result = TOOLS[tool](user_input)

        return {
            "success": True,
            "tool": tool,
            "result": result,
            "input_length": len(user_input)
        }

    except Exception as e:
        return {
            "success": False,
            "tool": "error",
            "result": str(e),
            "input_length": len(user_input)
        }
