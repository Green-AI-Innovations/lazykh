FROM python:3.9

RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    build-essential \
    libssl-dev \
    libcurl4-openssl-dev \
    libasound2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]