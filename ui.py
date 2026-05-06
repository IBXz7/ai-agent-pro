
import gradio as gr
import requests
import os

API_URL = "https://ai-agent-pro.onrender.com"

def call_agent(user_input):
    try:
        response = requests.post(
            API_URL,
            json={"text": user_input}
        )
        data = response.json()

        
        return f"""
🧠 Tool: {data.get('tool', 'unknown')}

📊 Result:
{data.get('output', 'No response')}
"""
    except Exception as e:
        return f"❌ Error: {str(e)}"


interface = gr.Interface(
    fn=call_agent,
    inputs=gr.Textbox(
        lines=8,
        placeholder="Type your text here..."
    ),
    outputs="text",
    title="🤖 AI Agent Pro",
    description="Summarize | Explain | Generate Questions باستخدام AI"
)

interface.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
