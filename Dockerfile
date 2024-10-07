FROM python:3.11-slim-bullseye

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app
RUN pip install --no-cache -r /app/requirements.txt

# Copy the entire app directory
COPY app /app/app

# Start Uvicorn from the app.main module
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "app.main:app"]
