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

functions: List[Tool] = [
    {
        "type": "function",
        "function": {
            "name": "save_code_to_file", # $HighlightLine
            "description": "Save code to file",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": { # $HighlightLine
                        "type": "string",
                        "description": "The code to save",
                    },
                    "filename": { # $HighlightLine
                        "type": "string",
                        "description": "The filename including the path and extension",
                    },
                },
            },
        },
    },
    # ... rest of the functions
]

# ... rest of the file
