import groq

# --- Groq API Key ---
GROQ_API_KEY = "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"  # Replace with your actual API key

# --- Initialize Groq Client ---
client = groq.Client(api_key=GROQ_API_KEY)

# --- Model Configuration ---
MODEL_NAME = "qwen-2.5-coder-32b"  # Supports 128K context

# --- Chat History ---
chat_history = []

def get_coding_response(user_query):
    """Sends user query to Groq API and returns the response."""
    # Add user query to chat history
    chat_history.append({"role": "user", "content": user_query})

    try:
        # --- Groq API Request ---
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=chat_history,
            temperature=0.7,
            max_tokens=4096,
        )

        # Extract assistant's reply
        assistant_reply = response.choices[0].message.content.strip()

        # Add assistant reply to chat history
        chat_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except Exception as e:
        return f"Error: {str(e)}"

# --- Main Execution ---
if __name__ == "__main__":
    print("💻 Coding Bot using Qwen2.5-Coder-32B (Groq API)")
    print("Type 'exit' to quit the conversation.\n")

    while True:
        # Get user input
        user_query = input("👤 You: ")
        
        # Exit condition
        if user_query.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        # Get and display response
        response = get_coding_response(user_query)
        print(f"🤖 Bot: {response}")
