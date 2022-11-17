FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /web
COPY requirements.txt /web/

RUN python3.10 -m pip install --upgrade pip
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /web/
