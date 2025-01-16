import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Intent keywords for domain classification
INTENT_KEYWORDS = {
    "ecommerce": ["buy", "order", "product", "cart", "delivery"],
    "banking": ["account", "loan", "transaction", "bank", "balance"],
    "medical": ["doctor", "appointment", "prescription", "medicine", "health"],
}

class IntentClassifier:
    def classify(self, user_prompt):
        """
        Classify user intent based on predefined domains and keywords.
        """
        user_prompt = user_prompt.lower()
        for domain, keywords in INTENT_KEYWORDS.items():
            if any(keyword in user_prompt for keyword in keywords):
                return domain
        return "unrecognized_domain"

def initialize_components():
    """Initialize models for each domain with their respective API keys."""
    try:
        return {
            'intent_classifier': IntentClassifier(),
            'ecommerce_model': setup_gemini(api_key=os.getenv("ECOMMERCE_API_KEY")),
            'banking_model': setup_gemini(api_key=os.getenv("BANKING_API_KEY")),
            'medical_model': setup_gemini(api_key=os.getenv("MEDICAL_API_KEY")),
        }
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        return None

def setup_gemini(api_key):
    """Setup and return a Gemini model with a specific API key."""
    if not api_key:
        raise ValueError("API key not found in environment variables")
    
    gen_ai.configure(api_key=api_key)
    return gen_ai.GenerativeModel('gemini-pro')

def get_intent_response(domain, user_input, model):
    """Generate response using the domain-specific Gemini model."""
    try:
        response = model.start_chat(history=[]).send_message(
            f"User query: {user_input}"
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    # Streamlit configuration
    st.set_page_config(
        page_title="AI Assistant",
        page_icon="🤖",
        layout="centered"
    )
    
    # Initialize components
    components = initialize_components()
    if not components:
        return
    
    st.title("🤖 AI Assistant")
    
    # Get user input
    user_input = st.text_input("How can I assist you today?")
    
    if user_input:
        st.markdown(f"**You:** {user_input}")
        
        try:
            # Classify intent to determine the domain
            intent_classifier = components['intent_classifier']
            domain = intent_classifier.classify(user_input)
            
            if domain == "unrecognized_domain":
                st.error("Sorry, I couldn't understand your query.")
                return
            
            # Select the appropriate model
            model_key = f"{domain}_model"
            if model_key not in components:
                st.error(f"No model available for the '{domain}' domain.")
                return
            
            model = components[model_key]
            
            # Generate the response
            response = get_intent_response(domain, user_input, model)
            
            # Display the response
            st.markdown(f"**Assistant ({domain}):** {response}")
        
        except Exception as e:
            st.error(f"Error processing your request: {e}")

if __name__ == "__main__":
    main()
    