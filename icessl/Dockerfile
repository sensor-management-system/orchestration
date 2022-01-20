FROM python:3.9-slim-buster

RUN apt-get update && apt-get -y install openssl

RUN pip install --upgrade pip --no-cache-dir

RUN pip install zeroc-icecertutils

WORKDIR /icessl

ADD ice-ca-certs.py .
