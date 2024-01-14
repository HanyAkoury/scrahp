# Dockerfile for Scrahp application - api

# Use a slim version of Python 3.9 for a lightweight base image
FROM python:3.9.18-slim


# Maintainer and project information
LABEL maintainer="Hany Akoury" \
      github="https://github.com/HanyAkoury/scrahp" \
      version="0.0" \
      description="A Docker container to serve the Python Flask API related to the SCRAHP project"


# Set the working directory to /api
WORKDIR /api

# Copy pyproject.toml, poetry.lock, and poetry.toml files for installing dependencies
COPY pyproject.toml poetry.lock poetry.toml /api/

# Install Poetry for dependency management and setting up the virtual environment
RUN pip install "poetry==1.7.1" && \
    poetry config virtualenvs.create true && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application files to the container
COPY ./api /api

# chmod - modifies the serve.sh file so it can be recognized as an executable file.
RUN chmod +x serve.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# ENTRYPOINT - allows you to configure a container that will run as an executable.
ENTRYPOINT ["./serve.sh"]
