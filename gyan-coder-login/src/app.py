import streamlit as st
import json
import hashlib

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

# Add a new user to the system
def add_user(username, password, email):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": hash_password(password), "email": email}
    save_users(users)
    return True

# Streamlit UI
st.title("Login / Signup System")

# Create two columns for the Login and Signup buttons
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    login_button = st.button("Login", key="login_tab_button")
with col2:
    signup_button = st.button("Signup", key="signup_tab_button")

# Initialize session state for tracking active tab if not exists
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'login'

# Update active tab based on button clicks
if login_button:
    st.session_state.active_tab = 'login'
if signup_button:
    st.session_state.active_tab = 'signup'

# Display content based on active tab
if st.session_state.active_tab == "login":
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_submit"):
        if verify_user(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password.")

elif st.session_state.active_tab == "signup":
    st.subheader("Signup")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_email = st.text_input("Email Address", key="signup_email")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Signup", key="signup_submit"):
        if new_password != confirm_password:
            st.error("Passwords do not match!")
        elif add_user(new_username, new_password, new_email):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already exists. Try another one.")

# Dashboard for authenticated users
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.subheader("Welcome to your Dashboard!")
    st.write("You have successfully logged in.")
    if st.button("Logout", key="logout_button"):
        st.session_state["authenticated"] = False
        st.rerun()
