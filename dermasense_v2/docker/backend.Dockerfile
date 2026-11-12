FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend backend
COPY data data
RUN useradd -m app && mkdir -p chroma_storage && chown -R app /app
USER app
WORKDIR /app/backend
EXPOSE 8000
# Index the reference documents (idempotent), then start the API.
CMD ["sh", "-c", "python -m scripts.load_docs && uvicorn main:app --host 0.0.0.0 --port 8000"]
