# Import libraries
import os

import openai
from openai import OpenAI

# Import actions from Assistants API (we have defined them in the "actions.py")
# from OpenAI.Guide_Without_Custom_Sandbox.actions import read_file, save_code_to_file, list_files

# Set up OpenAI API key
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Optional - import types, allowing for explicit type hints
from typing import Any, Dict

# Import E2B and create sandbox
import e2b
from e2b import Sandbox

client = openai.Client()
sandbox = Sandbox(id="1nmphrgeuzqmtqv5dgkg")

# Import our action
# from OpenAI.Guide_Without_Custom_Sandbox.actions import read_file, save_code_to_file, list_files

# Add action to the sandbox we created in the previous steps
# sandbox.add_action(read_file).add_action(save_code_to_file).add_action(list_files)

# "Call" the assistant, using its ID
AI_ASSISTANT_ID = os.getenv("AI_ASSISTANT_ID")

# Use the OpenAI API to retrieve the assistant
assistant = client.beta.assistants.retrieve(AI_ASSISTANT_ID)

# Define a function to run the assistant in the E2B sandbox
def main():
    sandbox = Sandbox(id="1nmphrgeuzqmtqv5dgkg")

    # sandbox.add_action(read_file).add_action(save_code_to_file).add_action(list_files)

    task = "Write a function that takes a list of strings and returns the longest string in the list."

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Carefully plan this task and start working on it: {task}",
            },
        ],
    )

    # Create a thread, send messages to the thread, and finally run the thread. Here, we are using the OpenAI's concept of threads and runs.
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

    while True:
        print("Assistant is currently ", run.status)
        if run.status == "requires_action":
            outputs = sandbox.openai.actions.run(run)
            if len(outputs) > 0:
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id, run_id=run.id, tool_outputs=outputs
                )

        elif run.status == "completed":
            print("Run completed")
            messages = (
                client.beta.threads.messages.list(thread_id=thread.id).data[0].content
            )
            text_messages = [message for message in messages if message.type == "text"]
            print("Thread finished:", text_messages[0].text.value)
            break

        elif run.status in ["queued", "in_progress"]:
            pass

        elif run.status in ["cancelled", "cancelling", "expired", "failed"]:
            break

        else:
            print(f"Unknown status: {run.status}")
            break

        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    sandbox.close()


if __name__ == "__main__":
    main()

    