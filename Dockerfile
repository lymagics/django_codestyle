FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src app/src
COPY scripts app/scripts
COPY tests app/tests
COPY certs app/certs
COPY oas.yml app/oas.yml
COPY pytest.ini app/pytest.ini
COPY setup.cfg /app/setup.cfg

WORKDIR /app/src