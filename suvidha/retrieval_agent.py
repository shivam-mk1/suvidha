import google.generativeai as genai
import pandas as pd
import os

# Load datasets
datasets = {
    "ecommerce": pd.read_csv("ecommerce.csv"),
    "banking": pd.read_csv("banking.csv"),
    "medical": pd.read_csv("medical.csv"),
}

# Clean dataset column names to avoid unexpected issues
for key, df in datasets.items():
    df.columns = df.columns.str.strip()

def setup_gemini(api_key):
    """Setup and return a Gemini model with a specific API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def retrieval_agent(entities, domain, model):
    """
    Retrieve relevant data from the dataset based on detected entities and domain.
    
    Args:
        entities (dict): A dictionary of entities and their values.
        domain (str): The domain classified by the IntentClassifier.
        model: The domain-specific Gemini model.
    
    Returns:
        str: Enhanced response or error message.
    """
    if domain not in datasets:
        return f"Invalid domain '{domain}'. Unable to determine the dataset."
    
    dataset = datasets[domain]

    # Filter the dataset based on the detected entities
    query_conditions = []
    for entity, value in entities.items():
        if "Not found" not in value:
            if entity in dataset.columns:
                query_conditions.append((dataset[entity] == value))
            else:
                return f"Entity '{entity}' not found in the {domain} dataset columns."

    if not query_conditions:
        return "No relevant entities detected in the query."

    # Combine all query conditions using logical AND
    combined_condition = query_conditions[0]
    for condition in query_conditions[1:]:
        combined_condition &= condition

    # Retrieve relevant data
    try:
        results = dataset[combined_condition]
        if results.empty:
            return f"No records found matching all entities in the {domain} dataset."
        
        # Generate enhanced response using Gemini
        context = results.to_dict(orient="records")[0]  # Use the first matching record
        user_context = ", ".join(f"{k}: {v}" for k, v in context.items())
        response = model.start_chat(history=[]).send_message(
            f"Based on this data: {user_context}, provide assistance to the user."
        )
        return response.text
    except Exception as e:
        return f"Error querying the dataset: {e}"
