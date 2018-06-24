FROM ubuntu:16.04

MAINTAINER togglecorp info@togglecorp.com

# Update and install common packages with apt
RUN apt-get update -y ; \
    apt-get install -y \
        # Basic Packages
        git \
        locales \
        vim \
        curl \
        cron \
        unzip \
        python3 \
        python3-dev \
        python3-setuptools \
        python3-pip \
        unzip

# Support utf-8
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

WORKDIR /code

RUN pip3 install virtualenv && \
    virtualenv /venv

COPY ./requirements.txt /code/requirements.txt
RUN . /venv/bin/activate && \
    pip install -r requirements.txt

COPY . /code/
