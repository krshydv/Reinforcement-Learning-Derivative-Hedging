FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY alembic.ini alembic.ini
COPY alembic alembic
COPY scripts scripts
RUN chmod +x /app/scripts/start.sh /app/scripts/worker.sh
EXPOSE 8000 8001
CMD ["/app/scripts/start.sh"]
