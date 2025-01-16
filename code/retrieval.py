import google.generativeai as genai
import pandas as pd

# Configure the API with your key
genai.configure(api_key="YOUR_API_KEY")

# Load the datasets
datasets = {
    "ecommerce": pd.read_csv("ecommerce.csv"),
    "banking": pd.read_csv("banking.csv"),
    "medical": pd.read_csv("medical.csv")
}

# Clean the dataset column names to avoid unexpected issues
for key, df in datasets.items():
    # Strip any leading/trailing spaces from column names
    df.columns = df.columns.str.strip()


# Define a retrieval agent function
def retrieval_agent(entities, intent):
    # Determine the relevant dataset based on the intent
    if intent in ["product_query", "ecommerce"]:
        dataset_name = "ecommerce"
    elif intent in ["banking_query", "banking"]:
        dataset_name = "banking"
    elif intent in ["medical_query", "medical"]:
        dataset_name = "medical"
    else:
        return "Invalid intent. Unable to determine the dataset."

    dataset = datasets[dataset_name]

    # Filter the dataset based on the detected entities
    query_conditions = []
    for entity, value in entities.items():
        # Only check the entity if its value is not "Not found"
        if "Not found" not in value:
            if entity in dataset.columns:
                query_conditions.append((dataset[entity] == value))
            else:
                return f"Entity '{entity}' not found in the dataset columns."

    if not query_conditions:
        return "No relevant entities detected in the query."

    # Combine all query conditions using logical AND
    combined_condition = query_conditions[0]
    for condition in query_conditions[1:]:
        combined_condition &= condition

    # Retrieve the relevant data
    try:
        results = dataset[combined_condition]
        if results.empty:
            return f"No records found matching all entities in the {dataset_name} dataset."
        return results
    except Exception as e:
        return f"Error querying the dataset: {e}"

# Example usage
entities = {"ProductID": "P001", "Category": "Not found"}  # Category is not checked
intent = "ecommerce"
result = retrieval_agent(entities, intent)
print("Query Results:\n", result)
