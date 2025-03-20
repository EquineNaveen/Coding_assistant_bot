import streamlit as st
from gyancoder import get_coding_response


# Set page config for chatbot
st.set_page_config(page_title="Coding Chatbot", page_icon="🤖", layout="centered")

# Initialize authentication in session state if not set
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# If the user is not authenticated, redirect to login
if not st.session_state['authenticated']:
    st.warning("Please login first.")
    st.stop()

# Chatbot UI
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    st.title("🤖 Code Helper Bot")
with col2:
    if st.button("Clear Chat", key="clear_chat_btn"):
        st.session_state['chat_history'] = []  # Clear chat history
        st.rerun()
with col3:
    if st.button("Logout", key="logout_btn"):
        # Clear login state and redirect to login
        st.session_state["authenticated"] = False
        st.success("You have been logged out!")
        st.rerun()

# Initialize chat history if not available
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


# Custom CSS for right and left alignment of messages with black text
st.markdown("""
    <style>
    .user-message {
        background-color: #DCF8C6;
        border-radius: 12px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
        color: black;
    }
    .bot-message {
        background-color: #F1F0F0;
        border-radius: 12px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)


# Function to send user query to gyancoder.py and get model response
def get_response(user_query):
    """Send user query to gyancoder.py and get model response."""
    return get_coding_response(user_query)


# Display chat history with custom CSS
chat_container = st.container()
with chat_container:
    for message in st.session_state['chat_history']:
        role, text, code = message
        if role == "user":
            st.markdown(f"<div class='user-message'>{text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{text}</div>", unsafe_allow_html=True)
        if code:
            st.code(code, language="python")

# Handle user input
user_input = st.chat_input("Ask me anything about coding...")

if user_input:
    # Add user message to chat
    st.session_state['chat_history'].append(("user", user_input, None))
    st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)

    # Get and display response from gyancoder.py
    bot_response = get_response(user_input)
    st.session_state['chat_history'].append(("assistant", bot_response, None))
    st.markdown(f"<div class='bot-message'>{bot_response}</div>", unsafe_allow_html=True)
