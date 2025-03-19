import streamlit as st

# Set page config for chatbot
st.set_page_config(page_title="Coding Chatbot", page_icon="🤖", layout="centered")

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
    .chat-container {
        overflow-y: auto;
        max-height: 500px;
    }
    .button-container {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Check if user is logged in
if not st.session_state.get('authenticated'):
    st.warning("Please login first.")
    st.stop()

# Chatbot Header with Aligned Buttons
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    st.title("🤖 Code Helper Bot")
with col2:
    if st.button("Clear Chat", key="clear_chat_btn"):
        st.session_state['chat_history'] = []  # Clear chat history
        st.rerun()
with col3:
    if st.button("Logout", key="logout_btn"):
        st.session_state["authenticated"] = False  # Logout user
        st.success("You have been logged out!")
        st.rerun()

# Initialize chat history if not available
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to return a hardcoded response
def get_response(_):
    return "This is a placeholder response. I am ready to be replaced with an LLM! 🚀"

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

    # Generate and display hardcoded bot response
    bot_response = get_response(user_input)
    st.session_state['chat_history'].append(("assistant", bot_response, None))
    st.markdown(f"<div class='bot-message'>{bot_response}</div>", unsafe_allow_html=True)
