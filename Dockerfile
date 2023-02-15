# syntax = docker/dockerfile:1.2

FROM python:3.11.2-bullseye

ENV TZ=America/Sao_Paulo
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app

# install requirements
COPY ./requirements /app/requirements
RUN pip install -r /app/requirements/base.txt --no-cache-dir

# copy code
COPY ./dyel /app/dyel
