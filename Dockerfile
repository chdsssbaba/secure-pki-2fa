# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Install dependencies + dos2unix for Windows compatibility
RUN apt-get update && apt-get install -y cron tzdata dos2unix && rm -rf /var/lib/apt/lists/*

# Set Timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy Python libs
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy App
COPY . .

# Configure Cron (Fixing line endings automatically)
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN dos2unix /etc/cron.d/2fa-cron && \
    chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron

# Setup Volumes & Entrypoint
RUN mkdir -p /data /cron && chmod 777 /data /cron
RUN echo '#!/bin/bash\nservice cron start\nuvicorn app:app --host 0.0.0.0 --port 8080' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

EXPOSE 8080
CMD ["/app/entrypoint.sh"]