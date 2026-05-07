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
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}


# --- Tools ---

def summarize(text):
    text = text[:1000]

    result = query_api(
        SUMMARIZE_URL,
        {"inputs": text}
    )

    # handle API errors
    if isinstance(result, dict) and result.get("error"):
        return f"Error: {result['error']}"

    return result[0].get(
        "summary_text",
        "No summary generated"
    )


def explain(text):
    prompt = f"Explain this clearly:\n{text}"

    result = query_api(
        GENERATOR_URL,
        {"inputs": prompt}
    )

    # handle API errors
    if isinstance(result, dict) and result.get("error"):
        return f"Error: {result['error']}"

    return result[0].get(
        "generated_text",
        "No explanation generated"
    )


def generate_questions(text):
    prompt = f"Generate 3 study questions:\n{text}"

    result = query_api(
        GENERATOR_URL,
        {"inputs": prompt}
    )

    # handle API errors
    if isinstance(result, dict) and result.get("error"):
        return f"Error: {result['error']}"

    return result[0].get(
        "generated_text",
        "No questions generated"
    )


# --- Tool Registry ---
TOOLS = {
    "summarize": summarize,
    "explain": explain,
    "questions": generate_questions
}


# --- Agent Brain ---
def decide_tool(user_input):
    text = user_input.lower()

    # --- Fast Rules ---
    if "summary" in text or "summarize" in text:
        return "summarize"

    if "explain" in text:
        return "explain"

    if "question" in text or "questions" in text:
        return "questions"

    # --- Fallback ---
    return "summarize"


# --- Main Agent ---
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
