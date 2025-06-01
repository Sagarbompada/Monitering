# Dockerfile

# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask and FastAPI ports
EXPOSE 5000 8000

# Start services using a script or supervisor (multiservice setup)
CMD ["bash", "-c", "uvicorn ingestion:app --host 0.0.0.0 --port 8000 & python app.py & python main.py"]
