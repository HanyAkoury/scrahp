# Use an official Python runtime as a parent image
FROM python:3.9.18-slim


# adds metadata to an image
LABEL MAINTAINER="Hany Akoury"
LABEL GitHub="https://github.com/HanyAkoury/scrahp"
LABEL version="0.0"
LABEL description="A Docker container to serve the Python Flask API related to the SCRAHP project"

# Set the working directory to /api
WORKDIR /api

RUN ls

# Copy only the files needed for installing dependencies
COPY pyproject.toml poetry.lock poetry.toml /api/

# chmod - modifies the boot.sh file so it can be recognized as an executable file.
COPY ./api/serve.sh ./
RUN chmod +x serve.sh

# Copy the current directory contents into the container at /api
COPY ./api/app.py /api

# Install poetry
RUN pip install "poetry==1.7.1"

# Install dependencies using poetry
RUN poetry config virtualenvs.create true \
    && poetry install --no-dev --no-interaction --no-ansi


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# ENTRYPOINT - allows you to configure a container that will run as an executable.
ENTRYPOINT ["./serve.sh"]