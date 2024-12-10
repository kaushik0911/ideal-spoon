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

RUN rm /app/.env

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]

# Expose the port the app runs on (default Django development server port)
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
