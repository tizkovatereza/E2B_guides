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



