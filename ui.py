import gradio as gr
import requests
import os

API_URL = "https://your-api.onrender.com/agent"


def call_agent(user_input):
    try:
        response = requests.post(
            API_URL,
            json={"text": user_input},
            timeout=60
        )

        data = response.json()

        tool = data.get("tool", "unknown")
        result = data.get("result", "No result")

        return f"""
🧠 Tool Used: {tool}

✨ Result:
{result}
"""

    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.Interface(
    fn=call_agent,
    inputs=gr.Textbox(lines=8),
    outputs="text",
    title="AI Agent Pro",
    description="HuggingFace + FastAPI AI Agent"
)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 10000))
    )
