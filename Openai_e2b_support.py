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



# 3. Add action to sandbox

# Import our action
from actions import read_file, save_code_to_file, list_files

# Add action to the sandbox we created in the previous steps
sandbox.add_action(read_file).add_action(save_code_to_file).add_action(list_files)


