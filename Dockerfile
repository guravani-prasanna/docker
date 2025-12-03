FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir fastapi uvicorn cryptography pyotp
RUN apt-get update && apt-get install -y cron

# Copy cron job file
COPY 2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron

EXPOSE 8080

# Start cron and FastAPI together
CMD cron && uvicorn main:app --host 0.0.0.0 --port 8080