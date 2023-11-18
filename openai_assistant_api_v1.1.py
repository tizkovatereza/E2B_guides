# INSTALL OPENAI IN TERMINAL

# !pip install --upgrade openai

# Check version:
# !pip show openai | grep Version
    # ERROR


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

# Pretty printing helper
import json
def show_json(obj):
    print(json.loads(obj.model_dump_json()))


client = OpenAI()

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
    model="gpt-4-1106-preview",
)
show_json(assistant)




MATH_ASSISTANT_ID = assistant.id  # or a hard-coded ID like "asst-..."


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")



# Create user requests in threads

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(MATH_ASSISTANT_ID, thread, user_input)
    return thread, run


# Emulating concurrent user requests
thread1, run1 = create_thread_and_run(
    "I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
thread2, run2 = create_thread_and_run("Could you explain linear algebra to me?")
thread3, run3 = create_thread_and_run("I don't like math. What can I do?")

# Now all Runs are executing...


# Get responses from runs

import time

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


# Wait for Run 1
run1 = wait_on_run(run1, thread1)
pretty_print(get_response(thread1))

# Wait for Run 2
run2 = wait_on_run(run2, thread2)
pretty_print(get_response(thread2))

# Wait for Run 3
run3 = wait_on_run(run3, thread3)
pretty_print(get_response(thread3))

# Thank our assistant on Thread 3 :)
run4 = submit_message(MATH_ASSISTANT_ID, thread3, "Thank you!")
run4 = wait_on_run(run4, thread3)
pretty_print(get_response(thread3))


# Update th assistant with a tool: Code interpreter

assistant = client.beta.assistants.update(
    MATH_ASSISTANT_ID,
    tools=[{"type": "code_interpreter"}],
)
show_json(assistant)


# Ask assistant to use the tool

thread, run = create_thread_and_run(
    "Generate the first 20 fibbonaci numbers with code."
)
run = wait_on_run(run, thread)
pretty_print(get_response(thread))



assistant = client.beta.assistants.retrieve("ai-developer-assistant")
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