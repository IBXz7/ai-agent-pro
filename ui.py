import streamlit as st
import requests

API_URL = "https://ai-agent-pro.onrender.com/chat"

st.set_page_config(page_title="AI Chat Bot", page_icon="💬")

st.title("💬 AI Chat Bot")

# --- session memory ---
if "history" not in st.session_state:
    st.session_state.history = []


# --- input ---
user_input = st.text_input("Type your message:")

# --- send button ---
if st.button("Send"):

    if user_input:

        response = requests.post(API_URL, json={
            "message": user_input,
            "history": st.session_state.history
        }).json()

        ai_response = response["response"]

        st.session_state.history.append({
            "user": user_input,
            "ai": ai_response
        })


# --- chat display ---
for chat in st.session_state.history:
    st.markdown(f"**🧑 You:** {chat['user']}")
    st.markdown(f"**🤖 AI:** {chat['ai']}")
    st.markdown("---")
