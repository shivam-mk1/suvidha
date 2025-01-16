import google.generativeai as genai
import pandas as pd

# Configure the API with your key
genai.configure(api_key="AIzaSyCRAYV-tMfWX3Hh4Aa44k1u1wOTQyw75jg")

# Load the dataset
data = pd.read_csv("ecommerce.csv")

# Define the context prompt to guide Gemini for entity detection
context_prompt = (
    "You are an AI assistant specialized in detecting key information from text. "
    "When given a query, identify whether it contains any of the following entities: \n"
    "- Product ID: A unique identifier for a product.\n"
    "- Product Name: The name of the product.\n"
    "- Category: The category the product belongs to.\n"
    "- Price: The price of the product.\n"
    "- Quantity In Stock: The number of items available.\n"
    "- Rating: The average customer rating.\n"
    "- Date Added: The date the product was added to the inventory.\n"
    "Return the detected entities with their respective values if found. "
    "If no relevant entities are found, respond with 'No relevant entities detected.'"
)

# Function to detect entities
def detect_entities(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(context_prompt + "\nQuery: " + query)
    print("Raw Gemini Response:\n", response.text)  # Debugging output to verify Gemini's response

    detected_text = response.text

    # Extract relevant entities from the response
    detected_entities = {}  # Placeholder for parsed entities
    for line in detected_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip() in map(str.strip, data.columns):  # Check if the entity is relevant to the dataset
                detected_entities[key.strip()] = value.strip()

    # Return the list of detected entities relevant to the dataset
    return detected_entities

# Example usage
query = "Can you provide the price and category for Product ID P001?"
result = detect_entities(query)
print("Detected Entities:\n", result)
