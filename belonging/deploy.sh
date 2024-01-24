#!/bin/bash
# Pull the latest changes
git pull origin main

# Build and run the Docker container
docker build -t belonging_app .
docker run -d -p 8000:8000 belonging_app


cd /path/to/your/django/app

# Pull the latest Docker image
docker pull ashtongkinnell/beloning-prod:latest

# Stop the current container
docker stop web_container

# Remove the stopped container
docker rm web_container

# Start a new container with the latest image
docker run --name web_container -d -p 80:80 ashtongkinnell/beloning-prod:latest