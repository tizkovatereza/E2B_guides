import e2b
import openai
from dotenv import load_dotenv

load_dotenv()
session = e2b.DataAnalysis(env_vars={})

with open("/Users/terezatizkova/Downloads/Air_Quality.csv", "rb") as f:
    remote_path = session.upload_file(file=f)

file = session.download_file(remote_path) 

downloaded_file_in_bytes = session.download_file(remote_path)
with open("/Users/terezatizkova/Downloads/Air_Quality_Chart.csv", "wb") as f:
  f.write(downloaded_file_in_bytes)  

# Install packages

#session.install_packages("name") - THIS IS JUST GENERIC?
#session.install_system_packages("name")

def handle_new_artifact(artifact):
    chart_file = artifact.download()

session.run_python(
    code="print(\"valid code\")",
    on_stdout=print,
    on_stderr=print,
    on_artifact=handle_new_artifact,
)