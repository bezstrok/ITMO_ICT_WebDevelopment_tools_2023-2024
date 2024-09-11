FROM huecker.io/library/python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --no-cache-dir uv

RUN uv venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
ENV VIRTUAL_ENV=/opt/venv

COPY pyproject.toml poetry.lock ./

RUN uv pip install --no-cache -r pyproject.toml

COPY src ./src
COPY migrations ./migrations
COPY alembic.ini .
