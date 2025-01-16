import streamlit as st
import google.generativeai as genai
from typing import Dict, Any
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class ChatAgent:
    def __init__(self):
        """Initialize the chat agent with Gemini API and session state"""
        # Get API key from environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Initialize session state for chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

    # ... rest of the ChatAgent class remains the same ...

def main():
    st.set_page_config(page_title="AI Assistant", layout="wide")
    
    try:
        # Initialize chat agent
        chat_agent = ChatAgent()
        
        # Create UI and get user input
        user_input = chat_agent.create_ui()
        
        if user_input:
            response = chat_agent.get_response(
                user_input=user_input,
                intent="general",
                entities={},
                retrieved_context=""
            )
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()