
# Keep a close attention to the functions definition inside the assistant.py file.
# We're using the Function calling feature to give our assistant the ability to call the sandbox actions we defined.



# Import libraries
import os
import e2b
import openai
from openai import OpenAI

# Set up API key
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


# Optional - import types, allowing for explicit type hints
from typing import Any, Dict


from typing import List
from openai.types.beta.assistant_create_params import Tool



# client = openai.Client()

# assistant = client.beta.assistants.create(
#     name="tt-ai-assistant-001",
#     instructions="You are very helpful assistant. You provide concise answer to my questions. You are friendly and occasionally add a random joke. ",
#     tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],   #Assigning the tools premade by OpenAI
#     model="gpt-4-1106-preview"
# )

def create_assistant():
    client = openai.Client()
    
    functions: List[Tool] = [
        {
            "type": "function",
            "function": {
                "name": "save_code_to_file",
                "description": "Save code to file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The code to save",
                        },
                        "filename": {
                            "type": "string",
                            "description": "The filename including the path and extension",
                        },
                    },
                },
            },
        },

    ]

    # current_directory = os.getcwd()

    ai_developer = client.beta.assistants.create(
        instructions="""You are an AI developer.

    When given a coding task, write and save code to files and install any packages if needed.
    Start by listing all files inside the repo. You work inside the '/home/user/repo' directory.

    Please print any code that you have written to the code also to the terminal.

    Then you provide step-by-step guide on how to download the resulting file from the '/home/user/repo' directory to my local directory. 
    Don't argue with me and just complete the task.

    Thank you, you're the best!
    """,
        name="AI Developer",
        tools=functions,
        model="gpt-4-1106-preview",
    )

    print("AI Developer Assistant created, please copy its ID below to your .env file. You can find all your created assistants at https://platform.openai.com/assistants.")
    print(ai_developer.id)


if __name__ == "__main__":
    create_assistant()