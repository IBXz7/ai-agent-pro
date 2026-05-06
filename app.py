import requests
import os
import json

# --- HuggingFace API Config ---

HF_API_KEY = os.getenv("HF_API_KEY")

SUMMARIZE_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
GENERATOR_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# --- Helper Function ---
def query_api(url, payload):
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # handle API errors
    if isinstance(data, dict) and data.get("error"):
        return {"error": data["error"]}

    return data


# --- Tools ---

def summarize(text):
    text = text[:1000]
    result = query_api(SUMMARIZE_URL, {"inputs": text})

    if "error" in result:
        return f"Error: {result['error']}"

    return result[0]["summary_text"]


def explain(text):
    prompt = f"Explain this clearly:\n{text}"
    result = query_api(GENERATOR_URL, {"inputs": prompt})

    if "error" in result:
        return f"Error: {result['error']}"

    return result[0]["generated_text"]


def generate_questions(text):
    prompt = f"Generate 3 study questions:\n{text}"
    result = query_api(GENERATOR_URL, {"inputs": prompt})

    if "error" in result:
        return f"Error: {result['error']}"

    return result[0]["generated_text"]


# --- Tool Registry ---
TOOLS = {
    "summarize": summarize,
    "explain": explain,
    "questions": generate_questions
}


# --- Agent Brain ---
def decide_tool(user_input):
    text = user_input.lower()

    # --- Rules (fast routing) ---
    if "summary" in text or "summarize" in text or "تلخيص" in text:
        return "summarize"

    if "explain" in text or "اشرح" in text:
        return "explain"

    if "question" in text or "أسئلة" in text:
        return "questions"

    # --- AI fallback ---
    prompt = f"""
Choose ONE tool:
- summarize
- explain
- questions

Respond ONLY JSON:
{{"tool": "summarize"}}

User:
{text}
"""

    result = query_api(GENERATOR_URL, {"inputs": prompt})

    try:
        output = result[0]["generated_text"]
        json_start = output.find("{")
        json_data = json.loads(output[json_start:])
        return json_data.get("tool", "summarize")
    except:
        return "summarize"


# --- Main Agent (FINAL OUTPUT FORMAT) ---
def agent(user_input):
    tool_name = decide_tool(user_input)

    if tool_name not in TOOLS:
        return {
            "success": False,
            "tool": "unknown",
            "result": "Unknown tool selected",
            "input_length": len(user_input)
        }

    result = TOOLS[tool_name](user_input)

    return {
        "success": True,
        "tool": tool_name,
        "result": result,
        "input_length": len(user_input)
    }
