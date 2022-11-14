FROM python:3.6
ENV PYTHONUNBUFFERED=1

WORKDIR /backend
COPY requirements.txt /backend/

RUN apt-get update && apt-get install -y python3-pip postgresql
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /backend/
