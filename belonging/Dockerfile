# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory for Django app
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Set up Nginx
COPY path/to/your/nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Expose the port Nginx is reachable on
EXPOSE 80

# Start Nginx and Gunicorn
CMD service nginx start && gunicorn --bind=0.0.0.0:8000 belonging.wsgi:application
