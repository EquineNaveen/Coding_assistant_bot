import streamlit as st
import json
import hashlib
import re
import sys
import os
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.runtime import Runtime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set page config at the very top
st.set_page_config(page_title="Gyan Coder - Login", page_icon="🔐", layout="centered")

# Add CSS to remove all space in sidebar before we add any content
st.markdown("""
    <style>
    /* More aggressive sidebar space removal targeting Streamlit's specific structure */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the root sidebar element */
    [data-testid="stSidebar"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the sidebar content specifically */
    .stSidebarContent, .css-1d391kg, .css-163ttbj, .css-1vq4p4l {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target all sidebar blocks and containers */
    [data-testid="stSidebar"] > div > div,
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] .block-container,
    [data-testid="stSidebar"] .element-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the immediate children of the sidebar */
    [data-testid="stSidebar"] > * {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target any additional wrapping divs */
    [data-testid="stSidebar"] div[data-stale="false"],
    [data-testid="stSidebar"] div.withScreencast {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the very first elements in the sidebar */
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebar"] > div > div:first-child,
    [data-testid="stSidebar"] .element-container:first-child,
    [data-testid="stSidebar"] div:first-of-type {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Target the image directly */
    [data-testid="stSidebar"] img,
    [data-testid="stSidebar"] [data-testid="stImage"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* The existing selectors */
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    section[data-testid="stSidebar"] > div > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    section[data-testid="stSidebar"] .element-container:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    section[data-testid="stSidebar"] div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    section[data-testid="stSidebar"] div.block-container > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Display ISRO image in sidebar
with st.sidebar:
    # Use absolute path to the image
    image_path = os.path.join(os.path.dirname(__file__), "assets", "isro.jpg")
    
    # Check if the image exists, if not, create a message
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.warning(f"Image not found at: {image_path}")
        st.info("Please make sure the 'assets' folder exists in the src directory and contains 'isro.jpg'")
    
    # Add a spacer before the horizontal line
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    # Add a horizontal line separator after the image with better spacing
    st.markdown("<hr style='margin-top: 5px; margin-bottom: 10px; border-width: 3px; background-color: #333;'>", unsafe_allow_html=True)
    
    # Add helper text in sidebar
    st.markdown("### Your Coding Assistant")
    st.markdown("- Ask for coding help")
    st.markdown("- Get syntax examples")
    st.markdown("- Request code snippets")
    st.markdown("- Debugging assistance")
    st.markdown("- Code Optimization Tips")

# Hide default Streamlit sidebar navigation
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# Add custom CSS for styling
st.markdown("""
    <style>
    .title-container {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f5f5f5;
        border-right: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Add the same footer CSS as in chatbot.py
st.markdown("""
    <style>
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
    </style>
""", unsafe_allow_html=True)

# Load user data from JSON file
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to JSON file
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify user credentials
def verify_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return True
    return False

# Create user chat directory
def create_user_chat_directory(username):
    # Create the parent directory if it doesn't exist
    parent_dir = "D:\\gyanstreamlit\\gyan-coder-login\\src\\users_chat"
    os.makedirs(parent_dir, exist_ok=True)
    
    # Create user-specific directory
    user_dir = os.path.join(parent_dir, username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

# Add a new user to the system
def add_user(username, password, email):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": hash_password(password), "email": email}
    save_users(users)
    
    # Create chat directory for the new user
    create_user_chat_directory(username)
    return True

# Change user password
def change_password(username, email, new_password):
    users = load_users()
    if username in users and users[username]["email"] == email:
        users[username]["password"] = hash_password(new_password)
        save_users(users)
        return True
    return False

# Validate email format
def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

# UI - Centered Title
st.markdown('<div class="title-container"><span class="main-title">GYAN CODER LOGIN</span></div>', unsafe_allow_html=True)

# Session state for tabs and forgot password
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'login'
if 'show_forgot_password' not in st.session_state:
    st.session_state.show_forgot_password = False

# Initialize authentication state if not present
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Toggle between login and signup
col1, col2, col3 = st.columns([6, 1, 1])
with col2:
    if st.button("Login", key="tab_login"):
        st.session_state.active_tab = 'login'
        st.session_state.show_forgot_password = False
with col3:
    if st.button("Signup", key="tab_signup"):
        st.session_state.active_tab = 'signup'

# Handle Login
if st.session_state.active_tab == "login":
    if not st.session_state.show_forgot_password:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        col_login, col_forgot = st.columns([1, 1])
        with col_login:
            if st.button("Login", key="login_submit"):
                if verify_user(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username  # Store username in session state
                    st.success(f"Welcome, {username}!")
                    st.switch_page("pages/chatbot.py")
                else:
                    st.error("Invalid username or password.")
        with col_forgot:
            if st.button("Forgot Password?", key="forgot_password_button"):
                st.session_state.show_forgot_password = True
                st.rerun()

    else:
        st.subheader("Reset Password")
        reset_username = st.text_input("Username", key="reset_username")
        reset_email = st.text_input("Email", key="reset_email")
        new_password = st.text_input("New Password", type="password", key="new_password")
        confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reset Password", key="reset_password"):
                if not is_valid_email(reset_email):
                    st.error("Please enter a valid email address.")
                elif new_password != confirm_new_password:
                    st.error("Passwords do not match!")
                else:
                    if change_password(reset_username, reset_email, new_password):
                        st.success("Password changed successfully!")
                        st.session_state.show_forgot_password = False
                        st.rerun()
                    else:
                        st.error("Invalid username or email!")
        with col2:
            if st.button("Back to Login", key="back_to_login"):
                st.session_state.show_forgot_password = False
                st.rerun()

# Handle Signup
elif st.session_state.active_tab == "signup":
    st.subheader("Signup")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_email = st.text_input("Email Address", key="signup_email")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Signup", key="signup_submit"):
        if not is_valid_email(new_email):
            st.error("Please enter a valid email address.")
        elif new_password != confirm_password:
            st.error("Passwords do not match!")
        elif add_user(new_username, new_password, new_email):
            st.success(f"Welcome, {new_username}!")
            st.session_state["authenticated"] = True
            st.session_state["username"] = new_username  # Store username in session state
            st.switch_page("pages/chatbot.py")  # Changed from st.rerun() to st.switch_page()
        else:
            st.error("Username already exists. Try another one.")

# Add footer at the bottom of the page
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-text">🚀 Built by Team GYAAN</div>
        </div>
    </div>
""", unsafe_allow_html=True)
