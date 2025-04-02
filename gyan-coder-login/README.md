# Gyan Coder Login

A Streamlit-based coding assistant application with user authentication and chat functionality. The application helps users with coding-related queries and maintains chat history.

## Features

- **User Authentication System**
  - Secure login/signup functionality
  - Password hashing for security
  - Password reset capability
  - Email validation

- **Interactive Coding Assistant**
  - Real-time code generation
  - Support for multiple programming languages
  - Code explanation capabilities
  - Syntax highlighting for code snippets

- **Chat Management**
  - Persistent chat history
  - User-specific chat storage
  - Ability to create new chats
  - Option to delete previous chats


 **How to run**
cd gyan-coder-login

**Installing the requirements**
pip install -r src/requirements.txt

**Create a .env file in the root directory with**
GROQ_API_KEY=your_groq_api_key_here

**Start the application**
cd src
streamlit run app.py