# gyan-coder-login

This project is a user login system for a code bot named Gyan Coder, built using Streamlit. It allows users to log in or create an account, storing user credentials in a JSON file.

## Project Structure

```
gyan-coder-login
├── src
│   ├── app.py          # Main entry point of the Streamlit application
│   ├── users.json      # Stores user credentials in JSON format
│   ├── pages
│   │   ├── login.py    # Login page implementation
│   │   └── signup.py   # Signup page implementation
│   └── utils
│       ├── auth.py     # Utility functions for authentication
│       └── database.py  # Functions for interacting with users.json
├── requirements.txt     # Lists project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gyan-coder-login
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run src/app.py
   ```

## Usage Guidelines

- Navigate to the login page to log in with your credentials.
- If you do not have an account, you can create one on the signup page.
- User credentials are stored in `users.json` and are verified during login.

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.