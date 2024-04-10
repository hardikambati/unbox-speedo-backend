FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir /app

COPY . /app/

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt