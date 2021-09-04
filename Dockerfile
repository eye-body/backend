FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

ENV PYTHONUNBUFFERED=1

COPY ./app /app
COPY ./requirements.txt requirements.txt
COPY ./.env ./.env
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
