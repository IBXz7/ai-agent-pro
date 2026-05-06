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

        
        tool = data.get("tool", "unknown")
        result = data.get("result", "No result")
        success = data.get("success", False)
        length = data.get("input_length", 0)

        if not success:
            return f"""
❌ Error

Result:
{result}
"""

        return f"""
🧠 Tool Used: {tool}

📊 Input Length: {length}

✨ Result:
{result}
"""

    except Exception as e:
        return f"❌ Error: {str(e)}"



interface = gr.Interface(
    fn=call_agent,
    inputs=gr.Textbox(
        lines=8,
        placeholder="Write any text: summary, explanation, or questions..."
    ),
    outputs="text",
    title="🤖 AI Agent Pro",
    description="Smart AI Agent using HuggingFace + FastAPI"
)

interface.launch(
    server_name="0.0.0.0",
    server_port=10000
)
