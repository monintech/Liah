import streamlit as st
import os
import requests

# Page config
st.set_page_config(page_title="OpenClaw AI", page_icon="🤖", layout="centered")
st.title("🤖 OpenClaw AI Assistant")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

if not OPENROUTER_API_KEY:
    st.error("OPENROUTER_API_KEY is not set. Please add it to your Railway environment variables.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": st.session_state.messages,
                },
            )
            data = response.json()
            if "choices" in data:
                reply = data["choices"][0]["message"]["content"]
            else:
                reply = f"Error: {data.get('error', {}).get('message', 'Unknown error')}"
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
