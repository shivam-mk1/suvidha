import streamlit as st
from ecommerce_entity import detect_entities as ecommerce_entities
from banking_entity import detect_entities as banking_entities
from medical_entity import detect_entities as medical_entities
from retrieval_agent import retrieval_agent
from chat_agent import ChatAgent

ENTITY_DETECTORS = {
    "e_commerce": ecommerce_entities,
    "banking": banking_entities,
    "medical": medical_entities,
}

API_KEYS = {
    "e_commerce": "ECOMMERCE_API_KEY",
    "banking": "BANKING_API_KEY",
    "medical": "MEDICAL_API_KEY",
}

def main():
    st.set_page_config(page_title="Domain-Specific Query Assistant", layout="wide")

    st.title("AI Assistant for Domain-Specific Queries")
    st.subheader("Choose a domain for your query:")
    selected_domain = st.radio(
        "Select your domain:", 
        options=["e_commerce", "banking", "medical"],
        format_func=lambda x: x.replace("_", " ").capitalize(),
    )

    user_query = st.text_area("Enter your query:", placeholder="Type your question here...")

    if st.button("Submit"):
        if not user_query.strip():
            st.error("Please enter a valid query!")
            return
        
        st.info(f"Detecting entities for the domain: {selected_domain.capitalize()}...")
        entity_detector = ENTITY_DETECTORS[selected_domain]
        detected_entities = entity_detector(user_query)
        st.success(f"Detected entities: {detected_entities}")

        st.info("Retrieving context based on detected entities...")
        chat_agent = ChatAgent(API_KEYS[selected_domain])
        response = retrieval_agent(detected_entities, selected_domain, chat_agent.model)

        st.info("Generating a response for the query...")
        if isinstance(response, str):
            st.error(response)
        else:
            final_response = chat_agent.get_response(
                user_input=user_query,
                intent=selected_domain,
                entities=detected_entities,
                retrieved_context=response,
            )
            st.success("Response:")
            st.write(final_response)

if __name__ == "__main__":
    main()
