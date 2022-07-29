FROM python:3.10.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /books/config

COPY Pipfile Pipfile.lock /books/
RUN pip install pipenv && pipenv install --system
RUN pip install psycopg2

COPY . /books/