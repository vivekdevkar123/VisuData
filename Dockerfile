FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /demo

WORKDIR /demo

ADD . /demo

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD python manage.py runserver 0:8000
