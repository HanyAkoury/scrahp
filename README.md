# Scrahp Project
<img src="https://images.unsplash.com/photo-1680136758313-42834b15462c?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" width="100%">

## Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Docker Usage](#docker-usage)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Scrahp project is a web scraping and API implementation built with Scrapy and Flask. It provides a simple  solution for extracting bbc articles and making it accessible via a user-friendly API.

## Architecture

The project consists of three main components:

1. **Scrahp (Scrapy Project):**
   - Handles web scraping and data extraction.
   - Utilizes Scrapy spiders to crawl the bbc website and collect information.

2. **API (Flask API):**
   - Exposes endpoints to interact with the scraped data.
   - Built with Flask for simplicity and ease of use.

3. **Database (SQLite3):**
   - Stores the scraped data in an SQLite database.
   - Ensures data persistence and easy retrieval.

## Docker Usage

### Overview
The Scrahp project is containerized using Docker, encompassing three main components: the scraping application (`scrahp`), the API (`api`), and the database (`database`). This setup ensures consistent environments and easy deployment.

### Docker Compose Setup
- `docker-compose.yml` orchestrates the interaction between the three services, defining their dependencies, networking, and volume mappings.
- The services are:
  - `scrahp`: The scraping component, responsible for data collection.
  - `api`: A Python Flask API that interacts with the database and provides endpoints for data access or manipulation.
  - `database`: A lightweight Python-based database server, handling data storage and queries.

### Running the Project
To get the Scrahp project up and running with Docker, follow these steps:

1. **Build the Services**:
   ```bash
   docker-compose build
   ```

2. **Start the Services**:
   ```bash
   docker-compose up
   ```
