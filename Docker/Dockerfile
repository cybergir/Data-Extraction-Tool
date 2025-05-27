# Dockerfile
FROM python:3.9-slim
WORKDIR /app

# Secure dependency installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    adduser --disabled-password extractor

COPY . .
USER extractor

# Health check
HEALTHCHECK --interval=30s CMD python -c "import requests; requests.get('http://localhost:8000/health')"

ENTRYPOINT ["python", "-m", "extractor.cli"]