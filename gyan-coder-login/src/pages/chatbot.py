import streamlit as st
from gyancoder import get_coding_response
import json
import os
from datetime import datetime
from pathlib import Path

# Function definitions
def get_user_chat_dir():
    """Create and return the user's chat directory path."""
    if not st.session_state.get('username'):
        st.error("No username found in session. Please login again.")
        st.session_state['authenticated'] = False
        st.rerun()
    
    base_dir = Path(__file__).parent.parent / "users_chat"
    user_dir = base_dir / st.session_state['username']
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def save_chat_history():
    """Save current chat history to a JSON file."""
    if not st.session_state.get('chat_history'):
        return
    
    # Get the first query from chat history
    first_message = next((msg for msg in st.session_state['chat_history'] if msg[0] == "user"), None)
    if not first_message:
        return
    
    # Create filename from first query (limited to 50 chars, sanitized)
    first_query = first_message[1][:50]  # Limit length
    # Remove special characters and spaces, replace with underscores
    safe_filename = "".join(c if c.isalnum() else "_" for c in first_query).strip("_")
    filename = f"{safe_filename}.json"
    
    user_dir = get_user_chat_dir()
    filepath = user_dir / filename
    
    chat_data = {
        'first_query': first_query,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'messages': st.session_state['chat_history']
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(chat_data, f, indent=2)

def load_chat_histories():
    """Load all available chat histories for the user."""
    user_dir = get_user_chat_dir()
    chat_files = []
    
    if user_dir.exists():
        for filepath in user_dir.glob('*.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                chat_data = json.load(f)
                chat_files.append((filepath.name, chat_data))
    
    return sorted(chat_files, key=lambda x: x[0], reverse=True)

def get_response(user_query):
    """Send user query to gyancoder.py and get model response."""
    return get_coding_response(user_query)

# Initialize authentication state and session variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state.get('username'):
    st.warning("Please login first.")
    st.stop()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Check authentication
if not st.session_state['authenticated']:
    st.warning("Please login first.")
    st.stop()

# Set page config for chatbot
st.set_page_config(page_title="Coding Chatbot", page_icon="🤖", layout="centered")

# Chatbot UI
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    st.title("🤖 Code Helper Bot")
with col2:
    if st.button("New Chat", key="clear_chat_btn"):
        if st.session_state['chat_history']:  # Save current chat before clearing
            save_chat_history()
        st.session_state['chat_history'] = []  # Clear chat history
        st.rerun()
with col3:
    if st.button("Logout", key="logout_btn"):
        # Clear login state and redirect to login
        st.session_state["authenticated"] = False
        st.success("You have been logged out!")
        st.rerun()

# Add chat history selector in the sidebar
st.sidebar.title("Chat History")
chat_histories = load_chat_histories()
if chat_histories:
    selected_chat = st.sidebar.selectbox(
        "Select previous chat",
        options=[f"{chat[1]['first_query']}" for chat in chat_histories],
        index=None
    )
    
    if selected_chat:
        # Load selected chat
        selected_index = [f"{chat[1]['first_query']}" for chat in chat_histories].index(selected_chat)
        st.session_state['chat_history'] = chat_histories[selected_index][1]['messages']
        st.rerun()

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

# Display chat history with custom CSS
chat_container = st.container()
with chat_container:
    for message in st.session_state['chat_history']:
        role, text, code = message
        if role == "user":
            st.markdown(f"<div class='user-message'>{text}</div>", unsafe_allow_html=True)
        else:
            # If the response has code and explanation
            if code:
                st.markdown(f"<div class='bot-message'>{text}</div>", unsafe_allow_html=True)
                st.code(code, language="python")  # ✅ Proper code block with highlighting
            else:
                # Properly render markdown for headings and explanations
                st.markdown(text, unsafe_allow_html=False)  # ✅ Correct markdown parsing

# Handle user input
user_input = st.chat_input("Ask me anything about coding...")

if user_input:
    # Add user message to chat
    st.session_state['chat_history'].append(("user", user_input, None))
    st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)

    # Get and display response from gyancoder.py
    bot_response = get_response(user_input)

    # Check if the response contains a code block
    if "```python" in bot_response and "```" in bot_response:
        # Extract the explanation and code block
        code_start = bot_response.find("```python") + 9
        code_end = bot_response.find("```", code_start)
        code_block = bot_response[code_start:code_end].strip()
        bot_message = bot_response.replace(f"```python\n{code_block}\n```", "").strip()

        # Add bot response to history with extracted code
        st.session_state['chat_history'].append(("assistant", bot_message, code_block))

        # Display explanation (if any) and code block
        if bot_message:
            st.markdown(bot_message, unsafe_allow_html=False)  # ✅ Fixed: Correctly display headings
        st.code(code_block, language="python")  # ✅ Properly display code
    else:
        # Add plain text bot response if no code is detected
        st.session_state['chat_history'].append(("assistant", bot_response, None))
        st.markdown(bot_response, unsafe_allow_html=False)  # ✅ Correct markdown display
    
    # Save chat after each message
    save_chat_history()
