# pip install e2b
# pip install openai

# Latest version
# pip install e2b --upgrade


# Import everything and start the E2B session

import e2b
from e2b import DataAnalysis

from e2b.templates.data_analysis import DataAnalysis


import openai
from dotenv import load_dotenv

load_dotenv()


# Create session variable

session: e2b.Session
session = e2b.DataAnalysis(env_vars={})


# Upload and download a local file

with open("/Users/terezatizkova/Downloads/Air_Quality.csv", "rb") as f:
    remote_path = session.upload_file(file=f)

file = session.download_file(remote_path) 

downloaded_file_in_bytes = session.download_file(remote_path)
with open("/Users/terezatizkova/Downloads/Air_Quality_Chart.csv", "wb") as f:
  f.write(downloaded_file_in_bytes)

  #wb ... opened for writing, "b" indicates that you will work with the file's content as a sequence of binary bytes rather than as text


# Install packages

#session.install_packages("name") - THIS IS JUST GENERIC?
#session.install_system_packages("name")



# Run the session

session.run_python(
    code="llm-generated python code",
    on_stdout=print,
    on_stderr=print,
    on_artifact=handle_new_artifact,
)

# Save the generated charts

def handle_new_artifact(artifact):
    chart_file = artifact.download()





