
# Project Services Overview

This project uses Docker Compose to orchestrate multiple services including BCR, User, Book, and Admin services, each backed by individual PostgreSQL databases, and a shared Redis service.

## Services

- **BCR Service:** Manages business-critical resources.
- **User Service:** Handles user-related operations.
- **Book Service:** Manages book inventory and related operations.
- **Admin Service:** Provides administrative capabilities.
- **PostgreSQL Databases:** Separate PostgreSQL instances for each service for data isolation.
- **Redis:** A shared Redis instance used for caching and session management.

## Prerequisites

- Docker
- Docker Compose (version 3.8 or higher)

## Setup and Running

### Initial Setup

Clone the repository and navigate into the directory:

```bash
git clone [Repository URL]
cd [Repository Directory]
```

### Building Services

Build all Docker images using the following command:

```bash
docker-compose build
```

### Running Services

Start all services with Docker Compose:

```bash
docker-compose up
```

Alternatively, to run in detached mode:

```bash
docker-compose up -d
```

### Stopping Services

To stop running services:

```bash
docker-compose down
```

## Ports

Each service is exposed on different ports on the host machine:

- **BCR Service:** 8000
- **User Service:** 8001
- **Book Service:** 8002
- **Admin Service:** 8003
- **PostgreSQL:** Exposed ports for each service's DB (5432-5435)
- **Redis:** 6379

## Environment Files

Each service uses an `.env` file located in their respective directories for environment variables. Ensure these files are correctly set up before starting the services.

## Volumes

Data for PostgreSQL databases is persisted in Docker volumes as defined in the `docker-compose.yml` file.

