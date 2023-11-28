import os
import e2b
import openai
from dotenv import load_dotenv
import json


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

session = e2b.DataAnalysis(env_vars={})
remote_path = ""
with open("/Users/terezatizkova/Downloads/GDP.csv", "rb") as f:
    remote_path = session.upload_file(file=f)

messages = [
    {"role": "system", "content": f"You are a helpful senior programmer and data analyst and you can complete tasks by running python code. You have access to the GDP of US saved in CSV file on this path '{remote_path}'"},
    {"role": "assistant", "content": "Hello, I am a helpful senior programmer and data analyst and I can complete tasks by running python code"},
    {"role": "user", "content": ""},
]

functions = [
  {
      "name": "exec_code",
      "description": "Executes the passed Python code using Nodejs and returns the stdout and stderr.",
      "parameters": {
          "type": "object",
          "properties": {
              "code": {
                  "type": "string",
                  "description": "The Python code to execute.",
              },
          },
          "required": ["code"],
      },
  }
]

user_input = input("Hello, I am your AI data analyst. How can I help you today?: ")
code = ""

# while True:
# user_input = input("Hello, I am your AI data analyst. How can I help you today?: ")
messages.append({"role": "user", "content": user_input})
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,  
    functions=functions,
)



#print(response)

content = response["choices"][0]["message"]["content"]
print(content)

#code_content = response["choices"][0]["message"]["function_call"]["arguments"]
#print(code_content)


if "function_call" in response["choices"][0]["message"]:
    print(response)
    func_args = response["choices"][0]["message"]["function_call"]["arguments"]
    parsed_func_args = json.loads(func_args) #this is a dictionary
    code = parsed_func_args["code"]
    print(code)
else:
    print("")


# Install packages

#session.install_packages("name") - THIS IS JUST GENERIC?
#session.install_system_packages("name")

def handle_new_artifact(artifact):
    chart_file = artifact.download() #in bytes
    with open(f"/Users/terezatizkova/Developer/E2B_guides/charts/{artifact.name}", "wb") as f:
        f.write(chart_file) #bytes saved into file
    # chart_file is not accessed


    # WHY IS THE BELOW NOT LIKE THIS?
    # if func_name == "exec_code":
    #   code = func_args["code"]
    #   stdout, stderr = await e2b.run_code("Node16", code) 
    #   print(stdout) 
    #   print(stderr) 


session.run_python(
    code=code,
    on_stdout=print,
    on_stderr=print,
    on_artifact=handle_new_artifact,
)




# QUESTIONS
# 1. How to get the code into the session? Can I replicate the code interpreter way?
# 2. How do I get out the code from the JSON response? If I try with ["code"] etc. it says that it needs integer, not str
# Why we didnt use this? session: e2b.Session

# TO-DOs
# 1. Infinite loop
# 2. Upload files