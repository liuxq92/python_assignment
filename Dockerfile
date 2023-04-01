FROM ubuntu:20.04

COPY . /opt/python_assignment

RUN apt update \
    && apt install -y python3.8 \
    && apt install -y python3-pip \
    && pip3 install -r /opt/python_assignment/requirements.txt
    