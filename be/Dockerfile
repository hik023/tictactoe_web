# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt update -y && apt upgrade -y
RUN apt-get install build-essential python3 gcc -y
RUN pip install -r requirements.txt
COPY . /code/

