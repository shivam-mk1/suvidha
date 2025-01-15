import google.generativeai as genai

# Configure the API with your key
genai.configure(api_key="AIzaSyCRAYV-tMfWX3Hh4Aa44k1u1wOTQyw75jg")

# Define the context prompt to guide Gemini for entity detection
context_prompt = (
    "You are an AI assistant specialized in detecting key information from text. "
    "When given a query, identify whether it contains any of the following entities: \n"
    "- Customer_ID\n"
    "- Customer_Name\n"
    "- Gender\n"
    "- Age\n"
    "- Account_Type\n"
    "- Account_Balance\n"
    "- Branch\n"
    "- Transaction_ID\n"
    "- Transaction_Type\n"
    "- Transaction_Amount\n"
    "- Transaction_Date\n"
    "Return the detected entities with their respective values if found. "
    "If no relevant entities are found, respond with 'No relevant entities detected.'"
)

# Function to detect entities
def detect_entities(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(context_prompt + "\nQuery: " + query)
    return response.text

# Example usage
query = "Can you provide the Transaction_Type and Transaction_Amount for Customer_ID 12345?"
result = detect_entities(query)
print("Detected Entities:\n", result)