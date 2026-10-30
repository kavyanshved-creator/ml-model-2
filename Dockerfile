FROM python:3.12-slim

# Prevent Python from writing .pyc files & allow live log streaming in Render
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency list and install
COPY requirement.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirement.txt

# Copy all application code and model files (.pkl / .joblib)
COPY . .

# Render defaults to port 10000
EXPOSE 10000

# Start server bound to 0.0.0.0 and Render's dynamic $PORT
CMD ["sh", "-c", "uvicorn fsales_api:app --host 0.0.0.0 --port ${PORT:-10000}"]