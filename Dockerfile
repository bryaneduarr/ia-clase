FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install dependencies needed
RUN apt-get update && apt-get install -y \
  build-essential \
  libgl1-mesa-glx \
  libglib2.0-0 \
  libqt5gui5 \
  libqt5widgets5 \
  libqt5network5 \
  libxkbcommon-x11-0 
