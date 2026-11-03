import os

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv


load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")


MODEL_OPTIONS = {
    "NVIDIA: Nemotron 3 Ultra Reasoning (free)": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "NVIDIA: Nemotron 3.5 Content Safety (free)": "nvidia/nemotron-3.5-content-safety:free",
    "NVIDIA: Nemotron 3 Ultra (free)": "nvidia/nemotron-3-ultra-550b-a55b:free"
}

# Sidebar model selection
st.sidebar.title("⚙️ Settings")

selected_model_name = st.sidebar.selectbox(
    "Choose your AI model",
    options=list(MODEL_OPTIONS.keys())
)

selected_model = MODEL_OPTIONS[selected_model_name]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    timeout=600,
    max_retries=5
)
st.set_page_config(
    page_title="GroQ Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("👽 GroQ Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "You are a helpful AI assistant."
    }]

# Display previous conversation
for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Ask OpenAI...")

if user_prompt:

    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    assistant_response = ""

    with st.chat_message("assistant"):

        st.caption(f"Using {selected_model_name}")

        response_placeholder = st.empty()

        stream = client.chat.completions.create(
            model=selected_model,
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                assistant_response += content
                response_placeholder.markdown(
                    assistant_response + "▌"
                )

        response_placeholder.markdown(assistant_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_response
    })
