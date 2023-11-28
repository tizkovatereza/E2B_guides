import os
import e2b
import openai
from e2b import Sandbox
from typing import Any, Dict # Optional - import types, allowing for explicit type hints
from dotenv import load_dotenv

from openai.guide.actions import read_file, save_code_to_file, list_files

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]