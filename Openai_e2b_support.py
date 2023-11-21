# IMPORT LIBRARIES
import os
import openai

from openai import OpenAI

# Import preferred actions from Assistants API
from actions import read_file, save_code_to_file, list_files

# SET UP API KEY
from dotenv import load_dotenv

# Defining a way to show assistant's output as a json object.
import json
def show_json(obj):
    print(json.loads(obj.model_dump_json()))

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Optional - import types, allowing for explicit type hints
from typing import Any, Dict

# Import E2B and create sandbox
import e2b
from e2b import Sandbox # $HighlightLine

client = openai.Client()
sandbox = Sandbox() # $HighlightLine

# Import our action
from actions import read_file, save_code_to_file, list_files

# Add action to the sandbox we created in the previous steps
sandbox.add_action(read_file).add_action(save_code_to_file).add_action(list_files)


# Define an assistant. After, you can see it at https://platform.openai.com/assistants
assistant = client.beta.assistants.create(
    name="tt-ai-assistant-001",
    instructions="You are my smart mentor who deeply understands AI and business. Your goal is to provide precise information about AI products I ask about. When given a question, search through the files provided to you. If an answer is not there, search the internet. ",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],   #Assigning the tools premade by OpenAI
    model="gpt-4-1106-preview"
)

# Printing assistant's output
show_json(assistant) # This is just to check the output of the assistant

# Define a thread
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)


# Start polling the run object
while True:
    if run.status == "requires_action": 
        outputs = sandbox.openai.actions.run(run) 
        if len(outputs) > 0: 
            client.beta.threads.runs.submit_tool_outputs( 
                thread_id=thread.id, run_id=run.id, tool_outputs=outputs 
            ) 

    # ... handle rest of the `run` states

    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

# Close the sandbox once everything is done

sandbox.close()