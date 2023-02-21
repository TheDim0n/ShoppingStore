FROM tiangolo/uvicorn-gunicorn:python3.11-slim

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
