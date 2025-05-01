import groq
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

# Model name
MODEL_NAME = "qwen-qwq-32b"

# System message with instruction to prioritize language or default to Python
chat_history = [
    {
        "role": "system",
        "content": (
            "You are a helpful coding assistant. Your sole purpose is to assist with programming and software development tasks. "
            "Only answer questions that are directly related to coding, software engineering, or technical implementation. "
            "If a user asks something unrelated to programming, politely respond that you can only help with coding questions. "
            "When the user does not specify a programming language, respond using Python by default."
        )
    }
]


# File to store conversation history
LOG_FILE = "chat_history.txt"


def log_conversation(user_query, assistant_reply):
    """Logs user query and assistant response to a file with separators."""
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"👤 User: {user_query}\n")
        file.write(f"🤖 Bot: {assistant_reply}\n")
        file.write("-----\n")  # Add separator for clarity


def clean_response(text):
    """Remove <think> tags and their content from the response."""
    # Pattern to match <think> tags and everything between them
    pattern = r'<think>.*?</think>'
    # Remove the matched patterns
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
    # Remove any extra whitespace that might result from the removal
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text.strip())
    return cleaned_text


def get_coding_response(user_query):
    """Sends user query to Groq API and returns the response."""
    chat_history.append({"role": "user", "content": user_query})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=chat_history,
            temperature=0.7,
            max_tokens=4096,
        )
        assistant_reply = response.choices[0].message.content.strip()
        
        # Clean the response to remove <think> tags and their content
        assistant_reply = clean_response(assistant_reply)
        
        chat_history.append({"role": "assistant", "content": assistant_reply})

        # Log query and response to file
        log_conversation(user_query, assistant_reply)

        return assistant_reply

    except Exception as e:
        error_message = f"Error: {str(e)}"
        log_conversation(user_query, error_message)
        return error_message


if __name__ == "__main__":
    print("💻 Coding Bot using Qwen2.5-Coder-32B (Groq API)")
    print("Type 'exit' to quit the conversation.\n")

    while True:
        user_query = input("👤 You: ")

        if user_query.lower() == "exit":
            print("👋 Goodbye!")
            break

        response = get_coding_response(user_query)
        print(f"🤖 Bot: {response}")
