from transformers import pipeline
import gradio as gr
import json

# --- Models ---
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
generator = pipeline("text-generation", model="gpt2")

# --- Tools ---

def summarize(text):
    result = summarizer(text, max_length=120, min_length=30, do_sample=False)
    return result[0]["summary_text"]

def explain(text):
    prompt = f"Explain this clearly:\n{text}"
    result = generator(prompt, max_length=120)
    return result[0]["generated_text"]

def generate_questions(text):
    prompt = f"Generate 3 study questions:\n{text}"
    result = generator(prompt, max_length=120)
    return result[0]["generated_text"]

# --- Tool Registry ---
TOOLS = {
    "summarize": summarize,
    "explain": explain,
    "questions": generate_questions
}

# --- Agent Brain (LLM decides) ---
def decide_tool(user_input):
    prompt = f"""
    You are an AI agent.

    Available tools:
    - summarize: summarize text
    - explain: explain text simply
    - questions: generate study questions

    Decide which tool to use.

    Respond ONLY in JSON format like:
    {{"tool": "summarize"}}

    User input:
    {user_input}
    """

    result = generator(prompt, max_length=100)
    output = result[0]["generated_text"]

    try:
        json_start = output.find("{")
        json_data = json.loads(output[json_start:])
        return json_data["tool"]
    except:
        return "summarize"

# --- Main Agent ---
def agent(user_input):
    tool_name = decide_tool(user_input)

    if tool_name not in TOOLS:
        return " Unknown tool"

    result = TOOLS[tool_name](user_input)

    return f" Tool used: {tool_name}\n\n{result}"

# --- UI ---
interface = gr.Interface(
    fn=agent,
    inputs=gr.Textbox(lines=10),
    outputs="text",
    title="AI Agent Pro",
    description="LLM-powered agent that selects tools dynamically"
)

# interface.launch()