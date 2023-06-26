FROM ubuntu:20.04

# Avoid timezone prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    python3.9 \
    python3-pip \
    libgl1-mesa-glx \
    build-essential \
    libssl1.1 \
    ffmpeg \
    libcurl4-openssl-dev \
    libasound2 \
    libpulse0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
