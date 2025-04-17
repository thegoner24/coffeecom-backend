# Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create a non-root user to run the application
RUN groupadd -r coffeeapp && useradd -r -g coffeeapp coffeeapp

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Create directory for logs
RUN mkdir -p /app/logs && chown -R coffeeapp:coffeeapp /app

# Copy application code
COPY --chown=coffeeapp:coffeeapp . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    GUNICORN_WORKERS=4 \
    GUNICORN_THREADS=2 \
    GUNICORN_TIMEOUT=120 \
    GUNICORN_KEEP_ALIVE=5

# Expose the port the app runs on
EXPOSE 5000

# Switch to non-root user
USER coffeeapp

# Command to run the application with optimized settings
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "${GUNICORN_WORKERS}", \
     "--threads", "${GUNICORN_THREADS}", \
     "--timeout", "${GUNICORN_TIMEOUT}", \
     "--keep-alive", "${GUNICORN_KEEP_ALIVE}", \
     "--log-level", "info", \
     "--access-logfile", "/app/logs/access.log", \
     "--error-logfile", "/app/logs/error.log", \
     "--forwarded-allow-ips", "*", \
     "app:create_app()"]
