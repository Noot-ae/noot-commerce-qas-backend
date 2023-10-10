# Pull base image
FROM python:3.9.16-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install
RUN apt-get install -y python-psycopg2 libpq-dev gcc


# install dependencies 
COPY ./requirements.txt /srv/requirements.txt

RUN pip install -r /srv/requirements.txt

RUN mkdir code && cd code

ADD . .

WORKDIR /code