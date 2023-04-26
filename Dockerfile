FROM python:3.9

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y libasound2-dev


COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]