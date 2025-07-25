FROM python:3.11-slim-bullseye AS deps-builder

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


FROM deps-builder AS static-builder

COPY . .
RUN python manage.py collectstatic --noinput


FROM python:3.11-slim-bullseye AS development

ENV PYTHONBUFFERED=1

COPY --from=deps-builder /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY --from=static-builder /app .
COPY --from=static-builder /app/static /app/static

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
