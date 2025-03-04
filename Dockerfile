FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install dependencies needed
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  build-essential \
  libgl1-mesa-glx \
  libglib2.0-0 \
  libqt5gui5 \
  libqt5widgets5 \
  libqt5network5 \
  libxkbcommon-x11-0 \
  python3-opencv \
  libopencv-dev \
  x11-xserver-utils

COPY requirements.txt /workspace/requirements.txt
  
# Set up a working directory
WORKDIR /workspace
  
RUN pip install -r requirements.txt
  
  # Copy project files
COPY . /workspace

CMD ["bash"]
