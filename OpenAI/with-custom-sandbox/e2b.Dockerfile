# Use the official Python 3.11.6 image as the base image
FROM python:3.11.6

# Run commands to install system dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
  build-essential curl git util-linux

# Set environment variables related to pip
ENV PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1

# Set the working directory inside the container to /code
WORKDIR /code

# Copy the requirements.txt file into the container at /code/requirements.txt
COPY ./requirements.txt requirements.txt

# Install Python dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Create a directory /home/user/artifacts inside the container
RUN mkdir -p /home/user/artifacts

# Append an export command to set the MPLBACKEND environment variable in .bashrc
RUN echo "export MPLBACKEND=module://e2b_matplotlib_backend" >>~/.bashrc

# Copy the e2b_matplotlib_backend.py file into the container at the specified path
COPY e2b_matplotlib_backend.py /usr/local/lib/python3.11/site-packages/e2b_matplotlib_backend.py
