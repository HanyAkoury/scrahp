# Create a docker image to be able to run the code and execute it but not modify it.
FROM python:3.9.18-slim

# Set the working directory to /app
WORKDIR /app

# Install poetry
RUN pip install "poetry==1.7.1"

# Copy only the files needed for installing dependencies
COPY pyproject.toml poetry.lock poetry.toml /app/

# Install dependencies using poetry
RUN poetry config virtualenvs.create true \
    && poetry install --no-dev --no-interaction --no-ansi

# Set the PATH to include the virtualenv created by poetry
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of the application code
COPY ./scrahp /app/scrahp