import streamlit as st
from gyancoder import get_coding_response
import json
import os
from datetime import datetime
from pathlib import Path

# Initialize session state variables at the very beginning
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'current_chat_id' not in st.session_state:
    st.session_state['current_chat_id'] = None
if 'logout' not in st.session_state:
    st.session_state['logout'] = False

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
    
    first_message = next((msg for msg in st.session_state['chat_history'] if msg[0] == "user"), None)
    if not first_message:
        return
    
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
        filepath.unlink() 
        return True
    return False

def get_response(user_query):
    """Send user query to gyancoder.py and get model response."""
    return get_coding_response(user_query)

query_params = st.query_params

if not st.session_state['authenticated'] and 'authenticated' in query_params and 'username' in query_params:
    st.session_state['authenticated'] = query_params['authenticated'] == 'true'
    st.session_state['username'] = query_params['username']
    # Load last chat or initialize new one
    chat_histories = load_chat_histories()
    if chat_histories:
        latest_chat = sorted(chat_histories, key=lambda x: x[1].get('timestamp', ''), reverse=True)[0]
        st.session_state['chat_history'] = latest_chat[1]['messages']
        st.session_state['current_chat_id'] = latest_chat[0]

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

col1, col2 = st.columns([6, 1])
with col1:
    st.title("🤖 Code Helper Bot")
with col2:
    if st.button("New Chat", key="clear_chat_btn"):
        if st.session_state['chat_history']:  
            save_chat_history()
        st.session_state['chat_history'] = []  
        st.session_state['current_chat_id'] = None
        st.rerun()

st.markdown("""
    <style>
    /* Hide default Streamlit sidebar navigation */
    div[data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Hide sidebar header with logo and collapse button */
    div[data-testid="stSidebarHeader"] {
        display: none !important;
    }
    
    /* Remove space above first element in sidebar (coding image) */
    section[data-testid="stSidebar"] > div:first-child > div:first-child {
        margin-top: -25px !important;
        padding-top: 0 !important;
    }
    
    section[data-testid="stSidebar"] > div > div:first-child .element-container {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* More aggressive targeting of sidebar padding */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0 !important;
    }
    
    section[data-testid="stSidebar"] img {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Sidebar image container */
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
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

    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 22%; /* Position after the sidebar (sidebar is typically ~22% of screen width) */
        right: 0;
        background-color: transparent;
        padding: 10px 0;
        text-align: center;
        font-size: 14px;
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 78%; /* Width should be 100% minus the sidebar width */
        margin-top: 20px;
        z-index: 100;
    }
    
    .footer-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    
    .footer-logo {
        height: 30px;
        width: auto;
    }
    
    .footer-text {
        font-weight: bold;
        margin: 0 10px;
    }
    
    /* Logout button in sidebar */
    .logout-btn {
        width: 100%;
        text-align: center !important;
        padding: 8px !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
        background-color: transparent !important;
        color: black !important;
        border-radius: 4px !important;
        border: 1px solid black !important;
        cursor: pointer !important;
        font-weight: bold !important;
    }
    
    .logout-btn:hover {
        background-color: #f0f2f6 !important;
    }
    
    </style>
""", unsafe_allow_html=True)


try:

    image_paths = [
        Path(__file__).parent.parent / "assets" / "codingbot.png",

    ]
    
    image_found = False
    for img_path in image_paths:
        try:
            if Path(img_path).exists():
                st.sidebar.image(str(img_path), width=150, use_column_width=True)
                image_found = True
                break
        except:
            continue
    
    if not image_found:
        st.sidebar.markdown("### Coding Bot")
except Exception as e:
    st.sidebar.write("Coding Bot") 


st.sidebar.markdown(
    """
    <style>
    /* Ensure the logout button always has a black border */
    [data-testid="stButton"] button[kind="primary"] {
        background-color: transparent !important;
        color: black !important;
        border: 1px solid black !important; 
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stButton"] button[kind="primary"] > div {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    [data-testid="stButton"] button[kind="primary"]:hover {
        background-color: rgba(0, 0, 0, 0.05) !important;
        color: black !important;
        border: 1px solid black !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* More specific selector to override any conflicting styles */
    section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
        border: 2px solid black !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
    }
    
    /* Additional hover effect for sidebar logout button */
    section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover {
        background-color: rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("Logout", key="sidebar_logout_btn", type="primary", use_container_width=True):
    if st.session_state.get('authenticated', False):
        st.session_state.clear() 
        st.session_state['logout'] = True  
        st.query_params = {}  
  
        st.success("Logged out successfully!")
        
        html_redirect = """
            <meta http-equiv="refresh" content="1; url=/" />
            <script>
                window.onload = function() {
                    setTimeout(function() {
                        window.location.href = '/';
                    }, 0);
                }
            </script>
        """
        st.markdown(html_redirect, unsafe_allow_html=True)
    
        try:
            st._rerun_with_location(location="/")
        except:
            pass
        st.stop()
    else:
        st.warning("You are not logged in. Please log in to continue.")
        st.stop()


st.sidebar.markdown("<hr style='margin: 5px 0px 0px 0px; border: none; height: 1px; background-color: #e0e0e0;'>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='margin-top: 0px; margin-bottom: 10px;'>Previous Chats</h3>", unsafe_allow_html=True)
chat_histories = load_chat_histories()

if chat_histories:
    # Sort by timestamp in descending order
    sorted_histories = sorted(
        chat_histories,
        key=lambda x: x[1].get('timestamp', ''),
        reverse=True
    )
    
  
    for idx, (chat_file, chat_data) in enumerate(sorted_histories):
        col1, col2 = st.sidebar.columns([8, 1])  
        
        with col1:
         
            if st.button(
                f"{chat_data['first_query'][:30]}{'...' if len(chat_data['first_query']) > 30 else ''}",
                key=f"chat_history_{idx}",
                use_container_width=True
            ):
                st.session_state['chat_history'] = chat_data['messages']
                st.session_state['current_chat_id'] = chat_file
                st.rerun()
        
        with col2:
          
            if st.button("✕", key=f"delete_{idx}", help="Delete this chat history", 
                        type="secondary"):
                if delete_chat_history(chat_file):
                    st.success("Chat deleted")
                    st.rerun()
                else:
                    st.error("Failed to delete chat")
else:
    st.sidebar.info("No chat history available")

# Display welcome message if chat history is empty
if not st.session_state['chat_history']:
    username = st.session_state.get('username', 'there')  
    capitalized_username = username[0].upper() + username[1:] if username else 'There'
    st.markdown(
        f"<div class='bot-message'>"
        f"👋 Hi {capitalized_username} I’m here to help you with coding—whether it's solving problems, building projects, or learning new languages. To get started, just type your question what you need help with, and I’ll guide you through it!"
        "</div>", 
        unsafe_allow_html=True
    )


chat_container = st.container()
with chat_container:
    for message in st.session_state['chat_history']:
        role, text, code = message
        if role == "user":
            st.markdown(f"<div class='user-message'>{text}</div>", unsafe_allow_html=True)
        else:
           
            if code:
                st.markdown(f"<div class='bot-message'>{text}</div>", unsafe_allow_html=True)
                st.code(code, language="python")  
            else:
               
                st.markdown(text, unsafe_allow_html=False)  


st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-text">🚀 Built by NAVEEN</div>
        </div>
    </div>
""", unsafe_allow_html=True)

user_input = st.chat_input("Ask me anything about coding...")

if user_input:
 
    st.session_state['chat_history'].append(("user", user_input, None))
    st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)

    thinking_placeholder = st.empty()
    with thinking_placeholder.container():
        st.markdown("""
            <div class='bot-message' style='display: flex; align-items: center; gap: 10px;'>
                <div style='display: flex; gap: 4px;'>
                    <div style='width: 8px; height: 8px; background-color: #666; border-radius: 50%; animation: thinking 1.4s infinite ease-in-out both; animation-delay: -0.32s;'></div>
                    <div style='width: 8px; height: 8px; background-color: #666; border-radius: 50%; animation: thinking 1.4s infinite ease-in-out both; animation-delay: -0.16s;'></div>
                    <div style='width: 8px; height: 8px; background-color: #666; border-radius: 50%; animation: thinking 1.4s infinite ease-in-out both;'></div>
                </div>
                <span>Thinking...</span>
            </div>
            <style>
                @keyframes thinking {
                    0%, 80%, 100% { 
                        transform: scale(0);
                        opacity: 0.5;
                    } 
                    40% { 
                        transform: scale(1);
                        opacity: 1;
                    }
                }
            </style>
        """, unsafe_allow_html=True)


    # Get and display response from gyancoder.py
    bot_response = get_response(user_input)

    thinking_placeholder.empty()

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
            st.markdown(bot_message, unsafe_allow_html=False)  
        st.code(code_block, language="python") 
    else:
        st.session_state['chat_history'].append(("assistant", bot_response, None))
        st.markdown(bot_response, unsafe_allow_html=False) 
    
    save_chat_history()
    
    # Refresh the page after response generation
    st.rerun()
