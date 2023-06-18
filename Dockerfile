FROM python:3.11-slim AS base

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt

FROM base as prod

COPY game game
COPY ssl ssl
COPY 269A70F350A0B4D7182D7A3D7788AF98.txt 269A70F350A0B4D7182D7A3D7788AF98.txt
