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

def delete_chat_history(chat_file):
    """Delete a specific chat history file."""
    user_dir = get_user_chat_dir()
    filepath = user_dir / chat_file
    
    if filepath.exists():
        filepath.unlink()  # Delete the file
        return True
    return False

def get_response(user_query):
    """Send user query to gyancoder.py and get model response."""
    return get_coding_response(user_query)

# Initialize authentication state and session variables
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = None

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'logout' not in st.session_state:
    st.session_state['logout'] = False

# Persist authentication state using query parameters
query_params = st.query_params

# Restore session state from query parameters if available
if not st.session_state['authenticated'] and 'authenticated' in query_params and 'username' in query_params:
    st.session_state['authenticated'] = query_params['authenticated'] == 'true'
    st.session_state['username'] = query_params['username']

# Check authentication
if not st.session_state['authenticated']:
    if st.session_state.get('logout', False):  # Check if the user has logged out
        st.warning("You are not logged in. Please log in to continue.")
        st.stop()
    else:
        st.warning("You are not logged in. Please log in to continue.")
        st.stop()

# Ensure username is set if authenticated
if st.session_state['authenticated'] and not st.session_state['username']:
    st.error("Session error: Username not found. Please log in again.")
    st.session_state['authenticated'] = False
    st.stop()

# Update query parameters to persist session state
st.query_params = {
    "authenticated": str(st.session_state['authenticated']).lower(),
    "username": st.session_state['username']
}

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
        if st.session_state.get('authenticated', False):
            # Clear login state and redirect to login
            st.session_state.clear()  # Clear all session state variables
            st.session_state['logout'] = True  # Set logout flag
            st.query_params = {}  # Clear query parameters
            st.markdown(
                "<p style='color: green; font-size: 16px; font-weight: bold; text-align: center;'>Logged out</p>",
                unsafe_allow_html=True
            )  # Display "Logged out" with styling
            st.query_params = {"page": "login"}  # Redirect to login page
            st.stop()  # Stop further execution to ensure the page is reset
        else:
            st.warning("You are not logged in. Please log in to continue.")
            st.stop()

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

    /* Target only sidebar buttons using more specific selectors */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left !important;
        padding: 7px 8px !important;
        border: none;
        background-color: transparent;
        font-size: 13px;
        margin: 0 !important;
        line-height: 1.5;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        min-height: 0 !important;
        height: auto !important;
        border-radius: 6px !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button > div {
        text-align: left !important;
        display: inline-block;
        width: 100%;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #f0f2f6;
    }
    
    /* Additional spacing reduction for sidebar elements */
    section[data-testid="stSidebar"] .element-container {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    section[data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    section[data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        margin-bottom: 0 !important;
        margin-top: 0 !important;
    }
    
    section[data-testid="stSidebar"] .stButton {
        margin-bottom: -10px !important;
        border-radius: 2px !important;
    }
    
    /* Style for delete button - modified to make it smaller */
    .delete-btn {
        color: #ff4b4b;
        background: none;
        border: none;
        cursor: pointer;
        float: right;
        padding: 0 3px;
        font-size: 12px;
        line-height: 1;
    }
    
    /* For the delete icon button in sidebar */
    section[data-testid="stSidebar"] .stButton:nth-child(2) > button {
        font-size: 10px !important;
        padding: 0 2px !important;
        min-width: 20px !important;
        height: 20px !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Custom close button styling */
    .close-button {
        color: #777777 !important; /* Neutral gray color instead of red */
        font-size: 8px !important; /* Smaller font size */
        padding: 0 !important;
        min-width: 16px !important;
        height: 16px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        line-height: 1 !important;
    }
    
    /* Improved chat history row styling */
    .chat-history-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }
    
    /* Custom styling for sidebar column layout */
    section[data-testid="stSidebar"] div.row-widget.stHorizontal {
        display: flex;
        align-items: center;
        gap: 2px;
    }
    
    /* Chat history button in sidebar */
    section[data-testid="stSidebar"] div.row-widget.stHorizontal > div:first-child .stButton > button {
        padding: 2px 6px !important;
        min-height: 24px !important;
    }
    
    /* Delete button in sidebar */
    section[data-testid="stSidebar"] div.row-widget.stHorizontal > div:last-child .stButton > button {
        padding: 2px !important;
        min-height: 24px !important;
        min-width: 24px !important;
        width: 24px !important;
        height: 24px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        font-size: 12px !important;
        color: #777 !important;
    }
    
    .chat-title {
        flex-grow: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    </style>
""", unsafe_allow_html=True)

# Updated chat history section with improved alignment
st.sidebar.title("Chat History")
chat_histories = load_chat_histories()

if chat_histories:
    # Sort by timestamp in descending order
    sorted_histories = sorted(
        chat_histories,
        key=lambda x: x[1].get('timestamp', ''),
        reverse=True
    )
    
    # Create a container for each history entry with a well-aligned close button
    for idx, (chat_file, chat_data) in enumerate(sorted_histories):
        col1, col2 = st.sidebar.columns([8, 1])  # Adjusted ratio for better alignment
        
        with col1:
            # Chat history button
            if st.button(
                f"{chat_data['first_query'][:30]}{'...' if len(chat_data['first_query']) > 30 else ''}",
                key=f"chat_history_{idx}",
                use_container_width=True
            ):
                st.session_state['chat_history'] = chat_data['messages']
                st.rerun()
        
        with col2:
            # Close button - properly aligned
            if st.button("✕", key=f"delete_{idx}", help="Delete this chat history", 
                        type="secondary"):
                if delete_chat_history(chat_file):
                    st.success("Chat deleted")
                    st.rerun()
                else:
                    st.error("Failed to delete chat")
else:
    st.sidebar.info("No chat history available")

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
