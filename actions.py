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



# GUIDE -> e2b.dev/docs

# 1. Import E2B and create sandbox

import openai
from e2b import Sandbox # $HighlightLine

client = openai.Client()
sandbox = Sandbox() # $HighlightLine





# 2. Define assistant's actions

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

