FROM python:3.13.3-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    libmagic1 \
    libmagic-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create log directory with proper permissions
RUN mkdir -p /var/log/app && chmod 755 /var/log/app

RUN apt-get update && apt-get install -y netcat-openbsd


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

ENV PYTHONUNBUFFERED=1

# Set up volume for logs
VOLUME ["/var/log/app"]

# Run gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level=info", "main:app"]