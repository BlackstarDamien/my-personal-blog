FROM python:3.11-slim-bullseye AS deps-builder

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


FROM deps-builder AS static-builder

WORKDIR /app
COPY . .
RUN python manage.py collectstatic --noinput


FROM python:3.11-slim-bullseye AS development

ENV PYTHONBUFFERED=1

WORKDIR /app
COPY --from=deps-builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=static-builder /app .

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
