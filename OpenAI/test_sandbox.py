
from dotenv import load_dotenv
load_dotenv()

from e2b import Sandbox
import logging



# Get e2b logger
e2b_logger = logging.getLogger("e2b")  

# Set e2b logger level to INFO
e2b_logger.setLevel(logging.INFO)  

# Setup formatter
formatter = logging.Formatter("E2B    - [%(asctime)s] - %(name)-32s - %(levelname)7s: %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")

# Setup handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add handler to e2b logger
e2b_logger.addHandler(handler)  


def main():
   
   sandbox = Sandbox()
   
   sandbox.filesystem.make_dir(path="/home/user/repo/")
   sandbox.filesystem.write(path="/home/user/repo/test.py", content="Hello World!")
   
   
   filename = sandbox.filesystem.watch_dir(path="/home/user/repo/").add_event_listener(lambda event: event.name)
   
   sandbox.close()


main()


    