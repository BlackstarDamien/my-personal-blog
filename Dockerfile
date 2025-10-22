# Base stage with security updates
FROM python:3.11-slim-bullseye AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Security: Apply security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*


# Dependencies builder stage
FROM base AS deps-builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Static files builder stage
FROM deps-builder AS static-builder

WORKDIR /app

COPY manage.py .
COPY my_personal_blog/ ./my_personal_blog/
COPY blog/ ./blog/

RUN python manage.py collectstatic --noinput


# Development stage
FROM base AS development

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install runtime dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY --from=deps-builder /opt/venv /opt/venv

# Copy application code
COPY manage.py .
COPY my_personal_blog/ ./my_personal_blog/
COPY blog/ ./blog/

# Setup Playwright
RUN playwright install-deps && playwright install

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


# Production stage
FROM base AS production

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Security: Create non-root user
RUN groupadd -r django && \
    useradd -r -g django -u 1000 -m -d /home/django django && \
    chown -R django:django /app

# Install runtime dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY --from=deps-builder --chown=django:django /opt/venv /opt/venv

# Copy application code
COPY --chown=django:django manage.py .
COPY --chown=django:django my_personal_blog/ ./my_personal_blog/
COPY --chown=django:django blog/ ./blog/

# Copy static files
COPY --from=static-builder --chown=django:django /app/static ./static

USER django

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').read()" || exit 1

CMD ["gunicorn", "my_personal_blog.wsgi:application", "--bind", "0.0.0.0:8000"]
