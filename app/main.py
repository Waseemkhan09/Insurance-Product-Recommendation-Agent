import streamlit as st
import os
from dotenv import load_dotenv
from llm_service import LLMService
from products import INSURANCE_PRODUCTS

# Loading environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash") 
llm_service = LLMService(model_name=MODEL_NAME)

# Defining the questions for the agent to ask
QUESTIONS = [
    {"id": "age", "text": "To start, what is your age?", "type": "number"},
    {"id": "dependents", "text": "Do you have any dependents (e.g., children, elderly parents)? If so, how many?", "type": "number"},
    {"id": "income", "text": "What is your approximate annual income? (e.g., 50000 USD, 10 lakhs INR)", "type": "text"},
    {"id": "assets", "text": "Do you own significant assets like a house, car, or other valuables? Please list them briefly.", "type": "text"},
    {"id": "health", "text": "How would you describe your general health? (e.g., excellent, good, average, specific conditions)", "type": "text"},
    {"id": "travel", "text": "Do you travel frequently, especially internationally?", "type": "text"},
    {"id": "budget", "text": "What is your approximate monthly budget for insurance premiums?", "type": "text"}
]

# --- Streamlit UI ---
st.set_page_config(page_title="Insurance Product Recommendation Agent", layout="centered")
st.title("🛡️ Insurance Product Recommendation Agent")
st.markdown("I'm here to help you find the best insurance products based on your needs.")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "recommendation_done" not in st.session_state:
    st.session_state.recommendation_done = False


def display_message(role, content):
    with st.chat_message(role):
        st.markdown(content)


for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# --- Agent Logic ---
def get_next_question():
    if st.session_state.current_question_idx < len(QUESTIONS):
        return QUESTIONS[st.session_state.current_question_idx]
    return None

def process_recommendation():
    st.session_state.recommendation_done = True
    display_message("assistant", "Thank you for providing your information!")
    st.session_state.messages.append({"role": "assistant", "content": "Thank you for providing your information!"})

    with st.spinner("Analyzing your needs and generating recommendations..."):
        structured_answers = ", ".join([f"{k}: {v}" for k, v in st.session_state.user_answers.items()])

        try:
            recommendation_text = llm_service.generate_recommendation(
                user_answers=st.session_state.user_answers,
                insurance_products=INSURANCE_PRODUCTS
            )
            display_message("assistant", recommendation_text)
            st.session_state.messages.append({"role": "assistant", "content": recommendation_text})
        except Exception as e:
            error_message = f"An error occurred during recommendation generation: {e}"
            display_message("assistant", error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# --- Main Chat Input and Flow ---
if not st.session_state.recommendation_done:
    current_question = get_next_question()

    if current_question:
        if not st.session_state.messages or st.session_state.messages[-1]["role"] == "user" or \
           st.session_state.messages[-1]["content"] != current_question["text"]:
            display_message("assistant", current_question["text"])
            st.session_state.messages.append({"role": "assistant", "content": current_question["text"]})

        user_input = st.chat_input("Your answer here...")
        if user_input:
            display_message("user", user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Store the answer
            st.session_state.user_answers[current_question["id"]] = user_input
            st.session_state.current_question_idx += 1 

            if st.session_state.current_question_idx >= len(QUESTIONS):
                process_recommendation()
            st.rerun() 
    else:
        if not st.session_state.recommendation_done:
            process_recommendation()
else:
    # Restart option 
    display_message("assistant", "Feel free to restart the conversation if you have new needs!")
    if st.button("Restart Conversation"):
        st.session_state.messages = []
        st.session_state.current_question_idx = 0
        st.session_state.user_answers = {}
        st.session_state.recommendation_done = False
        st.rerun()