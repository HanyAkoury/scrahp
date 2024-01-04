# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /db
WORKDIR /db

# Copy the initialization script and query script to the container
COPY ./db/init_db.py /db/
COPY ./db/db_queries.py /db/

# Run the initialization script using Python
RUN python init_db.py

# CMD to execute the queries (override with 'docker run my_db_container python db_queries.py')
# CMD ["python", "db_queries.py"]
