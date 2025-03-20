import groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

# Model name
MODEL_NAME = "qwen-2.5-coder-32b"

# System message with instruction to prioritize language or default to Python
chat_history = [
    {
        "role": "system",
        "content": (
            "You are a coding assistant that generates code in the language specified by the user. "
            "If the user does not mention a language, provide the code in Python by default."
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
