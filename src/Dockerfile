# syntax=docker/dockerfile:1
FROM kalilinux/kali-rolling

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nmap \
    ffuf \
    gobuster \
    nikto \
    redis-tools \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --break-system-packages Flask gunicorn redis pytest

# Set working directory
WORKDIR /app

# Copy application code
COPY ./app /app

# Default entrypoint
ENTRYPOINT ["python3", "-m", "app.api.main"]
