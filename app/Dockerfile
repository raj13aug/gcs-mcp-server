# Use lightweight official Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear immediately (important for Cloud Run)
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (optional but recommended)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
RUN pip install --upgrade pip
COPY . .
# Install dependencies
RUN pip install -r requirements.txt

# Copy rest of application code

# Cloud Run requires listening on PORT env variable
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run your app directly (NO uvicorn)
CMD ["python", "main.py"]