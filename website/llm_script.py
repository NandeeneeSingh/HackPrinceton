import os
from dotenv import load_dotenv
import subprocess
from groq import Groq
        

load_dotenv()
# Create the Groq client
class MedicalAssistant:
    def __init__(self) -> None:
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )

        self.chat_history = []

    def query_diagnosis(self, diagnosis : str) -> str:
        # Set the system prompt
        system_prompt = {
            "role": "system",
            "content": "You are talking to a fifth grader in a neutral, professional tone. Simplify the following diagnosis into one short sentences.",
        }
        
        self.chat_history = [ system_prompt ]
        self.chat_history.append(
            {
                "role": "user",
                "content": diagnosis
             }
        )

        response = self.client.chat.completions.create(
            model = "llama3-70b-8192", messages = self.chat_history, max_tokens=100, temperature=0.8
        )
        # Append the response to the chat history
        self.chat_history.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        # Print the response
        return(f"Simpified Diagnosis: {response.choices[0].message.content}")
