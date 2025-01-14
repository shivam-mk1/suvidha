import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    

# Function to classify user intent
def classify_intent(user_prompt):
    """
    Simple rule-based intent classifier that categorizes user input.
    """
    user_prompt = user_prompt.lower()

    # Define predefined intents and associated keywords
    intents = {
        "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
        "goodbye": ["bye", "goodbye", "see you", "take care"],
        "information": ["tell me about", "what is", "how do", "explain", "information on"],
        "help": ["help", "assist", "support", "I need help"],
        "default": ["unknown"]
    }

    # Check if any keywords match the user input
    for intent, examples in intents.items():
        if any(example in user_prompt for example in examples):
            return intent

    return "default"    


if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


st.title("🤖 Gemini Pro - ChatBot")

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    
    st.chat_message("user").markdown(user_prompt)
    
     # Classify the user intent using the helper function
    intent = classify_intent(user_prompt)

    # Define predefined responses for classified intents
    if intent == "greeting":
        gemini_response = "Hello! How can I assist you today?"
    elif intent == "goodbye":
        gemini_response = "Goodbye! Take care!"
    elif intent == "information":
        gemini_response = f"Sure! Let me provide more information about '{user_prompt}'."
    elif intent == "help":
        gemini_response = "I'm here to help! How can I assist you today?"
    else:
        gemini_response = "Sorry, I didn't understand that. Can you please rephrase?"

    # Show the bot's predefined response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)