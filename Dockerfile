FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./app/requirements.txt /opt
WORKDIR /opt
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app
