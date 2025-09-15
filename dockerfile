FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# If pip packages need building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code so modules are available
COPY . .

# Optional non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Default command — run golf.py (change if you prefer)
CMD ["python", "golfrefined.py"]
