# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.5
# --- FIXED: Changed 'as' to 'AS' ---
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser

COPY . .

EXPOSE 8000

# --- FIXED: Corrected the path to your WSGI application ---
# Replace 'your_project_name' with the actual name of your Django project folder
# (the one that contains settings.py and wsgi.py).
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "clothing_factory.wsgi:application"]