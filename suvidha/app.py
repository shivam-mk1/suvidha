import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()

st.set_page_config(
    page_title="Chat with Suvidha!",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel(model_name="tunedModels/ecommerce--sheet1-qur60c6fu4oi")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("🧠 Suvidha - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

# Handle new user input
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Display user input
    st.chat_message("user").markdown(user_prompt)

    # Send user prompt to the model
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display model response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
