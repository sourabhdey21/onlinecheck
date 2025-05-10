# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install net-tools for network utilities
RUN apt-get update && apt-get install -y net-tools && rm -rf /var/lib/apt/lists/*

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run the app with root privileges (needed for traceroute)
USER root
CMD ["python", "app.py", "--host", "0.0.0.0"]