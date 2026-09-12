FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -fsSL https://ollama.com/install.sh | sh

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN python scripts/build_index.py

EXPOSE 8000

CMD ["sh", "-c", "ollama serve & sleep 5; ollama pull qwen3:1.7b || true; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"]
