FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

ENV PYTHONUNBUFFERED=1

COPY ./app /app
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app