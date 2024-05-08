# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install any necessary system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the directory where static files will be collected
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --no-input

# Make port 8000 available to the outside world
EXPOSE 8000

# Define command to run the app using gunicorn
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]