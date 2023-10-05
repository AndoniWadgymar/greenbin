FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR src/

COPY requirements.txt .

RUN pip3 install --upgrade pip setuptools

RUN pip3 install -r requirements.txt

COPY greenbin/ .

CMD python manage.py runserver 0.0.0.0:8000