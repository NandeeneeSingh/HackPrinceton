import os
from groq import Groq

# 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

# Create the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Set the system prompt
system_prompt = {
    "role": "system",
    "content": "You are talking to a fifth grader in a neutral, professional tone. Simplify the following diagnosis into one short sentences.",
}

# Initialize the chat history
chat_history = [system_prompt]

while True:
    # Get user input from the console
    user_input = input("Diagnosis: ")

    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3-70b-8192", messages=chat_history, max_tokens=100, temperature=0.8
    )
    # Append the response to the chat history
    chat_history.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
    # Print the response
    print("Medical Assistant:", response.choices[0].message.content)
