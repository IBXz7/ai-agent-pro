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

    if isinstance(data, dict) and data.get("error"):
        return f"Error: {data['error']}"

    return data


# --- Tools ---

def summarize(text):
    text = text[:1000]  # temporary limit length
    result = query_api(SUMMARIZE_URL, {"inputs": text})
    return result[0]["summary_text"]


def explain(text):
    prompt = f"Explain this clearly:\n{text}"
    result = query_api(GENERATOR_URL, {"inputs": prompt})
    return result[0]["generated_text"]


def generate_questions(text):
    prompt = f"Generate 3 study questions:\n{text}"
    result = query_api(GENERATOR_URL, {"inputs": prompt})
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

    # --- Rules ---
    if "summary" in text or "summarize" in text:
        return "summarize"

    if "explain" in text:
        return "explain"

    if "question" in text:
        return "questions"

    # --- fallback to AI ---
    prompt = f"""
Choose ONE tool:
- summarize
- explain
- questions

Respond JSON:
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


# --- Main Agent ---
def agent(user_input):
    tool_name = decide_tool(user_input)

    if tool_name not in TOOLS:
        return "Unknown tool"

    result = TOOLS[tool_name](user_input)

    return f"Tool used: {tool_name}\n\n{result}"
