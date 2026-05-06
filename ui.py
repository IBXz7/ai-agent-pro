import gradio as gr
import requests

API_URL = "https://ai-agent-pro.onrender.com"

def call_agent(user_input):
    try:
        response = requests.post(
            API_URL,
            json={"text": user_input}
        )
        data = response.json()
        return data.get("output", "No response")
    except Exception as e:
        return f"Error: {str(e)}"


interface = gr.Interface(
    fn=call_agent,
    inputs=gr.Textbox(lines=8, placeholder="Enter your text..."),
    outputs="text",
    title="AI Agent Pro",
    description="Smart AI Agent (Summarize, Explain, Questions)"
)

interface.launch()
