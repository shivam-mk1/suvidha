import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Streamlit configuration
st.set_page_config(
    page_title="E-commerce Intent Classifier",
    page_icon="🛒",
    layout="centered",
)

# Load the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API key is missing. Please set your GOOGLE_API_KEY in the environment variables.")
    st.stop()

# Configure Gemini Pro
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Helper function to translate roles for Streamlit's chat interface
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Define intents and keywords for e-commerce
INTENT_KEYWORDS = {
    # Order-related intents
    "order_status": ["where is my order", "track my package", "order status"],
    "order_cancellation": ["cancel my order", "stop my purchase"],
    "order_modification": ["change my order", "update delivery address"],
    "order_confirmation": ["did my order go through", "order confirmation"],
    "product_information": ["specs of", "does this come in", "product details"],
    "product_availability": ["is this item available", "stock levels", "back in stock"],
    "product_comparison": ["compare", "which is better", "difference between"],
    "payment_issues": ["payment failed", "charged twice"],
    "refunds": ["refund", "get my money back"],
    "payment_methods": ["accept paypal", "pay in installments"],
    "shipping_information": ["shipping charges", "ship internationally"],
    "delivery_timeframe": ["how long will it take", "when will I receive"],
    "delivery_issues": ["package didn’t arrive", "wrong item"],
    "return_policy": ["return policy", "return period"],
    "initiate_return": ["start a return", "return this item"],
    "exchange_requests": ["exchange for a different size", "how does exchange work"],
    "login_issues": ["forgot my password", "can’t log in"],
    "account_management": ["update my address", "change my email"],
    "discount_information": ["sales", "promo codes"],
    "gift_cards": ["redeem gift card", "buy a gift card"],
    "speak_to_human": ["need help from a person", "connect me to support"],
    "general_help": ["i need help", "assist me"],
    "website_issues": ["site isn’t loading", "can’t add items to cart", "having issue"],
    "app_issues": ["app keeps crashing", "update the app"],
    "product_feedback": ["this product is great", "didn’t like the quality"],
    "service_feedback": ["delivery was slow", "great support team"],
    "file_complaint": ["want to complain", "delivery was late"],
    "business_hours": ["when are you open", "support hours"],
    "store_location": ["nearest store", "store in my city"],
    "custom_requests": ["gift wrapping", "bulk discounts"],
    "unrecognized_queries": ["unknown"],
    # Medical
    "symptom_query": ["headache", "fever", "nausea", "cough", "pain in", "symptoms of"],
    "condition_information": ["diabetes", "asthma", "hypertension", "arthritis", "disease information"],
    "emergency_help": ["emergency", "heart attack", "stroke", "chest pain", "call 911"],
    "medication_information": ["dosage", "side effects", "drug interactions", "how to take"],
    "medication_availability": ["is this drug available", "prescription needed", "buy medication"],
    "treatment_options": ["treatment for", "therapy options", "how to treat"],
    "procedure_information": ["surgery details", "procedure risks", "recovery time"],
    "vaccination_information": ["vaccine for", "immunization", "flu shot"],
    "health_checkups": ["annual checkup", "routine tests", "preventive screening"],
    "schedule_appointment": ["book an appointment", "see a doctor", "consult a specialist"],
    "reschedule_appointment": ["reschedule my appointment", "change my appointment"],
    "appointment_cancellation": ["cancel my appointment", "appointment not needed"],
    "lab_results": ["blood test results", "scan report", "interpret my lab report"],
    "insurance_query": ["does my insurance cover", "health insurance", "policy details"],
    "billing_query": ["medical bill", "charges for", "billing issue"],
    "mental_health_support": ["depression", "anxiety", "therapy for mental health", "stress management"],
    "psychiatry_appointment": ["psychiatrist", "mental health consultation"],
    "dietary_advice": ["diet plan", "nutrition for", "healthy eating"],
    "fitness_guidance": ["exercise for", "workout routine", "fitness tips"],
    "unrecognized_queries": ["unknown", "not sure", "confused"],
    # Banking
    "account_balance": ["check my balance", "account balance", "how much money"],
    "account_statement": ["account statement", "transaction history", "mini statement"],
    "account_opening": ["open an account", "create a new account", "new savings account"],
    "account_closure": ["close my account", "delete account", "terminate account"],
    "fund_transfer": ["transfer money", "send funds", "make a payment"],
    "transaction_status": ["transaction failed", "payment status", "transaction confirmation"],
    "transaction_disputes": ["unauthorized transaction", "dispute transaction", "wrong charge"],
    "debit_card_issues": ["lost my debit card", "block debit card", "card not working"],
    "credit_card_issues": ["credit card limit", "credit card bill", "apply for credit card"],
    "card_activation": ["activate my card", "card activation process"],
    "card_replacement": ["replace my card", "expired card", "damaged card"],
    "loan_information": ["loan interest rates", "personal loan details", "loan eligibility"],
    "loan_application": ["apply for a loan", "loan application process"],
    "loan_repayment": ["loan repayment", "pay my loan", "loan installment"],
    "investment_options": ["investment plans", "mutual funds", "stocks and bonds"],
    "fixed_deposits": ["open FD", "fixed deposit rates", "FD maturity"],
    "recurring_deposits": ["start RD", "recurring deposit details", "RD interest rate"],
    "speak_to_human": ["talk to an agent", "connect to support", "customer service"],
    "general_help": ["help with banking", "I need assistance", "banking query"],
    "online_banking": ["how to log in", "internet banking", "online banking password"],
    "mobile_banking": ["app isn’t working", "mobile banking issues", "banking app update"],
    "upi_related": ["UPI transaction", "link UPI", "UPI payment failed"],
    "nearest_branch": ["find a branch", "nearest bank", "bank location"],
    "nearest_atm": ["find an ATM", "nearest ATM", "ATM location"],
    "fraud_report": ["report fraud", "suspicious activity", "phishing"],
    "security_inquiry": ["how secure is", "security features", "online safety tips"],
    "currency_exchange": ["exchange rates", "convert currency", "foreign exchange"],
    "banking_hours": ["branch timings", "banking hours", "when is the bank open"],
    "unrecognized_queries": ["unknown", "not sure", "confused"]
}

# Domain classification using if-else
# def classify_domain(user_prompt):
#     """
#     Classify the user's input into one of three domains: e-commerce, banking, or medical.
#     """
#     user_prompt = user_prompt.lower()

#     if any(keyword in user_prompt for keyword in [
#         "order", 
#         "product", 
#         "refund", 
#         "payment", 
#         "order_status",
#         "order_cancellation",
#         "order_modification",
#         "order_confirmation",
#         "product_information",
#         "product_availability",
#         "product_comparison",
#         "payment_issues",
#         "refunds",
#         "payment_methods",
#         "shipping_information",
#         "delivery_timeframe",
#         "delivery_issues",
#         "return_policy",
#         "initiate_return",
#         "exchange_requests",
#         "login_issues",
#         "account_management",
#         "discount_information",
#         "gift_cards",
#         "speak_to_human",
#         "general_help",
#         "website_issues",
#         "app_issues",
#         "product_feedback",
#         "service_feedback",
#         "file_complaint",
#         "business_hours",
#         "store_location",
#         "custom_requests",
#         ]):
#         return "ecommerce"
#     elif any(keyword in user_prompt for keyword in [
#         "account", 
#         "balance", 
#         "card", 
#         "loan",
#         "account_balance",
#         "account_statement",
#         "account_opening",
#         "account_closure",
#         "fund_transfer",
#         "transaction_status",
#         "transaction_disputes",
#         "debit_card_issues",
#         "credit_card_issues",
#         "card_activation",
#         "card_replacement",
#         "loan_information",
#         "loan_application",

#         ]):
#         return "banking"
#     elif any(keyword in user_prompt for keyword in ["symptom", "appointment", "medication", "doctor"]):
#         return "medical"
#     else:
#         return "unknown"

# Intent classification function
def classify_intent(user_prompt):
    """
    Classify user intent based on predefined categories and keywords.
    """
    user_prompt = user_prompt.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in user_prompt for keyword in keywords):
            return intent
    return "unrecognized_queries"

# Initialize chat session in Streamlit
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# App title
st.title("🛒 E-commerce Intent Classifier")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Capture user input
user_prompt = st.chat_input("Ask about your order, products, or account...")
if user_prompt:
    # Display user's message
    st.chat_message("user").markdown(user_prompt)

    # Classify intent
    intent = classify_intent(user_prompt)

    # Predefined responses for classified intents
    intent_responses = {
        "order_status": "Let me check your order status. Can you provide the order number?",
        "order_cancellation": "I can assist with cancelling your order. Please confirm your order details.",
        "order_modification": "Sure! What changes would you like to make to your order?",
        "order_confirmation": "Let me verify if your order went through. One moment, please.",
        "product_information": "Could you specify the product you're asking about?",
        "product_availability": "I'll check the stock for you. Which product are you referring to?",
        "product_comparison": "Let's compare those products. Can you provide more details?",
        "payment_issues": "Sorry to hear about the payment issue. I'll look into it for you.",
        "refunds": "I can help with your refund request. Can you share the order number?",
        "payment_methods": "We accept several payment methods. What would you like to know?",
        "shipping_information": "Our shipping options include standard and express. What would you like to know?",
        "delivery_timeframe": "Typically, deliveries take 3-5 business days. Let me check your specific order.",
        "delivery_issues": "I apologize for the inconvenience. Can you provide more details about the issue?",
        "return_policy": "Our return policy allows returns within 30 days. Would you like to start a return?",
        "initiate_return": "Sure, let’s initiate a return. Can you provide the order number?",
        "exchange_requests": "Exchanging items is easy! What item would you like to exchange?",
        "login_issues": "Let’s fix your login issue. Did you try resetting your password?",
        "account_management": "You can update your account settings. What changes would you like to make?",
        "discount_information": "We often have sales and promo codes. Would you like to know about current offers?",
        "gift_cards": "Gift cards can be redeemed during checkout. Would you like to buy one?",
        "speak_to_human": "I'll connect you to a human agent right away.",
        "general_help": "Sure, I'm here to assist. What's your question?",
        "website_issues": "I’m sorry about the issue. Can you share more details?",
        "app_issues": "Let’s troubleshoot the app issue. What seems to be the problem?",
        "product_feedback": "Thank you for your feedback! It helps us improve.",
        "service_feedback": "We appreciate your feedback on our service.",
        "file_complaint": "I’m sorry for the inconvenience. Can you share more details about the issue?",
        "business_hours": "Our support is available 24/7 online.",
        "store_location": "We have stores in many cities. Which location are you looking for?",
        "custom_requests": "Let me help with your special request. Can you share more details?",
        "unrecognized_queries": "I didn’t quite get that. Can you rephrase your query?",
        "symptom_query": "I understand you're experiencing symptoms. Can you provide more details about your condition?",
        "condition_information": "Here's some general information about this condition. Would you like to know more about symptoms or treatments?",
        "emergency_help": "If this is an emergency, please call 911 immediately or go to the nearest hospital.",
        "medication_information": "I can provide details about the medication. Which drug or dosage are you inquiring about?",
        "medication_availability": "I’ll check the availability of this medication. Do you have a prescription?",
        "treatment_options": "There are various treatments available. Can you provide more specifics about the condition?",
        "procedure_information": "Here are the details about the procedure. Do you have concerns about risks or recovery?",
        "vaccination_information": "Vaccinations are critical for health. Which vaccine or immunization are you asking about?",
        "health_checkups": "Routine health checkups are essential. What specific test or checkup are you inquiring about?",
        "schedule_appointment": "I can help you schedule an appointment. What date and time work best for you?",
        "reschedule_appointment": "Let’s reschedule your appointment. What new date and time would you prefer?",
        "appointment_cancellation": "I’ll cancel your appointment. Please confirm the details.",
        "lab_results": "I can help interpret your lab results. Can you share the test type or result details?",
        "insurance_query": "I’ll provide details about your insurance coverage. What specific service are you inquiring about?",
        "billing_query": "Let’s review your billing query. Can you provide the bill or service details?",
        "mental_health_support": "Mental health is important. Would you like to discuss therapy options or coping strategies?",
        "psychiatry_appointment": "I can assist with scheduling a psychiatry consultation. What’s your preferred date and time?",
        "dietary_advice": "Nutrition plays a vital role in health. What are your dietary goals or concerns?",
        "fitness_guidance": "Staying fit is essential. What type of fitness advice are you looking for?",
        "unrecognized_queries": "I didn’t quite understand that. Can you rephrase or provide more details?",
        "account_balance": "I can check your account balance. Please provide your account details.",
        "account_statement": "Would you like to view your recent transactions or a detailed statement?",
        "account_opening": "I can assist with opening an account. What type of account are you interested in?",
        "account_closure": "We’re sorry to see you go. Let me guide you through the account closure process.",
        "fund_transfer": "Let’s proceed with the fund transfer. Please share the recipient's details.",
        "transaction_status": "Let me check the status of your transaction. Can you provide the transaction ID?",
        "transaction_disputes": "I’ll help you dispute the transaction. Can you share more details?",
        "debit_card_issues": "I can assist with your debit card issue. Can you provide the card details?",
        "credit_card_issues": "Would you like to know about credit card features, billing, or limits?",
        "card_activation": "To activate your card, please follow the instructions provided with it.",
        "card_replacement": "I can help you replace your card. Is it lost, stolen, or damaged?",
        "loan_information": "Let me provide details about our loan offerings. What type of loan are you looking for?",
        "loan_application": "I’ll guide you through the loan application process. Do you have any specific requirements?",
        "loan_repayment": "Let’s check your repayment options. Can you share the loan account details?",
        "investment_options": "We offer various investment options. What type of investment are you interested in?",
        "fixed_deposits": "Fixed deposits are a secure way to grow your money. Would you like to know the current rates?",
        "recurring_deposits": "Recurring deposits allow you to save monthly. What duration are you considering?",
        "speak_to_human": "I’ll connect you to a human agent right away.",
        "general_help": "I’m here to assist. What banking issue can I help you with?",
        "online_banking": "I can help you with online banking. What issue are you facing?",
        "mobile_banking": "Let’s troubleshoot your mobile banking issue. Can you share more details?",
        "upi_related": "UPI payments are fast and secure. What issue are you experiencing?",
        "nearest_branch": "I’ll help you locate the nearest branch. Can you share your location?",
        "nearest_atm": "Let me find the nearest ATM for you. Please provide your location.",
        "fraud_report": "I’m sorry to hear that. Let’s report the fraudulent activity immediately.",
        "security_inquiry": "Your security is our priority. What concerns or questions do you have?",
        "currency_exchange": "Currency exchange rates fluctuate. Which currency would you like to exchange?",
        "banking_hours": "Our banking hours vary by branch. Do you have a specific branch in mind?",
        "unrecognized_queries": "I didn’t quite understand that. Can you rephrase or provide more details?",
    }

    # Generate dynamic response using Gemini Pro
    base_response = intent_responses.get(intent, "Let me check that for you.")
    enhanced_response = st.session_state.chat_session.send_message(f"{base_response} Context: {user_prompt}").text

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(enhanced_response)