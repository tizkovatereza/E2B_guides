import os
import e2b
import openai
from dotenv import load_dotenv
import json


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]



# 1. Import E2B
from e2b import Sandbox

# 2. Get your Sandbox session
# sandbox = Sandbox() # Is this base?
sandbox = Sandbox(id="terezatizkova_v01") 

# 3. Close the sandbox once done
sandbox.close()

