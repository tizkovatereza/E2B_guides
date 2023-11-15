# INSTALL OPENAI IN TERMINAL

# !pip install --upgrade openai

# Check version:
# !pip show openai | grep Version
    # ERROR


# IMPORT LIBRARIES AND SET UP API KEY

import os
import e2b
import openai
from openai import OpenAI

from dotenv import load_dotenv
import json


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


# Pretty printing helper
import json
def show_json(obj):
    print(json.loads(obj.model_dump_json()))


# Create an assistant
client = OpenAI()

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
    model="gpt-4-1106-preview",
)
show_json(assistant)

# Create a new thread

thread = client.beta.threads.create()
show_json(thread)


# Add message to the thread

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)
show_json(message)

# Create run

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
show_json(run)

# Poll the run in a loop

import time

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

run = wait_on_run(run, thread)
show_json(run)

# List the messages in the thread


messages = client.beta.threads.messages.list(thread_id=thread.id)
show_json(messages)

# Ask assistant to explain results a bit further

# # Create a message to append to our thread
# message = client.beta.threads.messages.create(
#     thread_id=thread.id, role="user", content="Could you explain this to me?"
# )

# # Execute our run
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
# )

# # Wait for completion
# wait_on_run(run, thread)

# # Retrieve all the messages added after our last user message
# messages = client.beta.threads.messages.list(
#     thread_id=thread.id, order="asc", after=message.id
# )
# show_json(messages)