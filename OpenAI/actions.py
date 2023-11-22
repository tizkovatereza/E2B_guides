
# In this file, we will define Python functions as a runnable actions for the AI assistant and the LLM.
# In the main file, we use the sandbox.add_action() method to register the actions with the sandbox.


# IMPORT LIBRARIES
import os
import e2b
import openai
from openai import OpenAI

# Set up OpenAI API key
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


# Optional - import types, allowing for explicit type hints
from typing import Any, Dict


# Import E2B and create sandbox

import openai
from e2b import Sandbox # $HighlightLine

client = openai.Client()
sandbox = Sandbox() # $HighlightLine



# Define assistant's actions
def save_code_to_file(sandbox: Sandbox, args: Dict[str, Any]) -> str:
    filename = args["filename"]
    code = args["code"]

    try:
        dir = os.path.dirname(filename)

        sandbox.filesystem.make_dir(dir)
        sandbox.filesystem.write(filename, code)

        return "success"
    except Exception as e:
        return f"Error: {e}"


def list_files(sandbox: Sandbox, args: Dict[str, Any]) -> str:
    path = args["path"]

    try:
        files = sandbox.filesystem.list(path)
        response = "\n".join(
            [f"dir: {file.name}" if file.is_dir else file.name for file in files]
        )
        return response
    except Exception as e:
        return f"Error: {e}"


def read_file(sandbox: Sandbox, args: Dict[str, Any]) -> str:
    path = args["path"]

    try:
        return sandbox.filesystem.read(path)
    except Exception as e:
        return f"Error: {e}"
    

# def download_file(sandbox: Sandbox, args: Dict[str, Any]) -> str:
#     path = args["path"]

#     try:
#         # Read the contents of the file from the sandbox
#         file_content = sandbox.filesystem.read(path)

#         # Extract the filename from the path
#         filename = os.path.basename(path)

#         # Write the file locally in the current working directory
#         local_path = os.path.join(os.getcwd(), filename)
#         with open(local_path, "w") as local_file:
#             local_file.write(file_content)

#         return f"File downloaded to local directory: {local_path}"
#     except Exception as e:
#         return f"Error: {e}"
