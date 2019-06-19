FROM python:3.7-alpine

MAINTAINER togglecorp info@togglecorp.com

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache git bash libpq \
    && apk add --no-cache --virtual .build-deps \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        geos-dev \
        libc-dev \
        gcc \
        python3-dev \
        musl-dev \
        postgresql-dev \
        ca-certificates \
    && pip install -r requirements.txt \
    && apk del --no-cache .build-deps

COPY . /code/
