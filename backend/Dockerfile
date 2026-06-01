FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
COPY app app
COPY alembic.ini alembic.ini
COPY alembic alembic
COPY tests tests
COPY scripts scripts
RUN chmod +x /app/scripts/start.sh /app/scripts/worker.sh
EXPOSE 8000 8001
CMD ["/app/scripts/start.sh"]
