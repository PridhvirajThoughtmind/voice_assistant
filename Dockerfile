FROM python:3.10-slim

WORKDIR /app

# Install system dependencies

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/\*

# Copy requirements and install

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy VOSK model (assumes model is downloaded separately)

COPY vosk-model /app/vosk-model

# Copy application code

COPY app /app/app

# Expose port

EXPOSE 8000

# Command to run the application

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]