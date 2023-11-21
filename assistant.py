# IMPORT LIBRARIES
import os
import e2b
import openai
from openai import OpenAI

# SET UP API KEY
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


# Optional
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
    Start by listing all files inside the repo. You work inside the home/user/repo directory.
    Don't argue with me and just complete the task.
    """,
        name="AI Developer",
        tools=functions,
        model="gpt-4-1106-preview",
    )

    print("AI Developer Assistant created, please copy its ID below to your .env file. You can find all your created assistants at https://platform.openai.com/assistants.")
    print(ai_developer.id)


if __name__ == "__main__":
    create_assistant()