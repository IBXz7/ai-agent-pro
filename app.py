import requests
import os

# --- OpenRouter Config ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


# --- Core LLM Function ---
def ask_llm(messages):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": messages
            },
            timeout=60
        )

        data = response.json()

        if "error" in data:
            return f"OpenRouter Error: {data['error']}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"LLM Error: {str(e)}"


# --- Chat Function (main brain) ---
def chat(message, history=[]):
    messages = []

    # build memory
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["ai"]})

    messages.append({"role": "user", "content": message})

    return ask_llm(messages)
