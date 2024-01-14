# Dockerfile for Scrahp application - scraping

# Use a slim version of Python 3.9 for a lightweight base image
FROM python:3.9.18-slim

# Set the working directory to /app within the container
WORKDIR /app

# Copy pyproject.toml, poetry.lock, and poetry.toml files for installing dependencies
COPY pyproject.toml poetry.lock poetry.toml /app/

# Install Poetry for dependency management and setting up the virtual environment
RUN pip install "poetry==1.7.1" && \
    poetry config virtualenvs.create true && \
    poetry install --no-dev --no-interaction --no-ansi

# Set the PATH to include the virtualenv created by poetry
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of the application code
COPY ./scrahp /app/scrahp
COPY ./scrapy.cfg /app/

ENTRYPOINT ["./scrahp/crawl.sh"]
