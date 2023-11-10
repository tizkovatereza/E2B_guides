# You can use most Debian-based base images
FROM ubuntu:22.04

# Install dependencies and customize sandbox

# Install the ffmpeg tool/
RUN apt update \
    && apt install -y ffmpeg