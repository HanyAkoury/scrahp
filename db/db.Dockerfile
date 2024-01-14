# Dockerfile for Scrahp application - database

# Use a slim version of Python 3.9 for a lightweight base image
FROM python:3.9.18-slim

# Set the working directory to /db
WORKDIR /db

# Copy the initialization script and query script to the container
COPY ./db/db_service.py /db/

# Run the initialization script using Python
RUN python db_service.py
