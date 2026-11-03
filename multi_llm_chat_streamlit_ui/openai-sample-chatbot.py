
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True, dotenv_path="..\\.env")

client = OpenAI()

st.set_page_config(
    page_title="OpenAI Sample Chat",
    page_icon="🤖",
    layout="centered",
)

# Available models
MODEL_OPTIONS = {
    "GPT-4.1 Mini (Fast)": "gpt-4.1-mini",
    "GPT-4o Mini (Average)": "gpt-4o-mini",
    "GPT-5.4 Mini (Reasoning)": "gpt-5.4-mini",
}

# Sidebar model selection
st.sidebar.title("⚙️ Settings")

selected_model_name = st.sidebar.selectbox(
    "Choose your AI model",
    options=list(MODEL_OPTIONS.keys())
)

selected_model = MODEL_OPTIONS[selected_model_name]

st.sidebar.info(f"Selected model: {selected_model}")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

st.title("👽 OpenAI ChatBot")

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
