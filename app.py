import requests
import os
import time

# --- HuggingFace API Config ---
HF_API_KEY = os.getenv("HF_API_KEY")

SUMMARIZE_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
GENERATOR_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


# --- Safe API Call (FIXED + ROBUST) ---
def query_api(url, payload):
    last_error = None  # 🔥 مهم جدًا

    for _ in range(3):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )

            try:
                data = response.json()
            except Exception as e:
                last_error = f"JSON error: {str(e)}"
                time.sleep(2)
                continue

            if isinstance(data, dict) and "error" in data:
                if "loading" in data["error"].lower():
                    last_error = data["error"]
                    time.sleep(3)
                    continue
                return {"error": data["error"]}

            return data

        except Exception as e:
            last_error = str(e)
            time.sleep(2)

    return {
        "error": f"HuggingFace failed after retries: {last_error or 'Unknown error'}"
    }


# --- Tools ---

def summarize(text):
    result = query_api(SUMMARIZE_URL, {"inputs": text[:1000]})

    if isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"

    return result[0].get("summary_text", "No summary")


def explain(text):
    prompt = f"Explain clearly:\n{text}"

    result = query_api(GENERATOR_URL, {"inputs": prompt})

    if isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"

    return result[0].get("generated_text", "No explanation")


def generate_questions(text):
    prompt = f"Generate 3 questions:\n{text}"

    result = query_api(GENERATOR_URL, {"inputs": prompt})

    if isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"

    return result[0].get("generated_text", "No questions")


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
