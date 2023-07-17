FROM python:3.11.4-slim AS base

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements/prod.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    libunwind-dev libpq-dev libdw-dev\
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r prod.txt

FROM base as prod

COPY game game
COPY config config

FROM prod as dev

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements/*.txt .

RUN pip install --no-cache-dir --upgrade -r tools.txt
