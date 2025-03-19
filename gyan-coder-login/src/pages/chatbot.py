import streamlit as st

# Set page config for chatbot
st.set_page_config(page_title="Coding Chatbot", page_icon="🤖", layout="centered")

# Custom CSS to align buttons and make them fit properly
st.markdown("""
    <style>
    .button-container {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
    }
    .button-container button {
        padding: 8px 12px;
        font-size: 16px;
        white-space: nowrap;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .header-container h1 {
        margin: 0;
        font-size: 2rem;
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

# Display chat history
for message in st.session_state['chat_history']:
    role, text, code = message
    with st.chat_message(role):
        st.markdown(text)
        if code:
            st.code(code, language="python")

# Handle user input
user_input = st.chat_input("Ask me anything about coding...")

if user_input:
    # Add user message to chat
    st.session_state['chat_history'].append(("user", user_input, None))
    with st.chat_message("user"):
        st.markdown(user_input)
