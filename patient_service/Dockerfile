# Base image
FROM python:3.10-slim

# Create and set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Remove the .env file (if necessary)
RUN [ -f /app/.env ] && rm /app/.env || echo "File not found, skipping removal"

# Running the test cases on sqlite on memory
RUN python manage.py test

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port the app runs on (default Django development server port)
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
