FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the script
COPY consumer.py .

# Start the consumer
CMD ["python", "consumer.py"]
