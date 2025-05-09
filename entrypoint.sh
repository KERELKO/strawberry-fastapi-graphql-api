#!/bin/bash
set -e

export PYTHONPATH="/app/src:$PYTHONPATH"

# Function to initialize the database tables
init_db_tables() {
    echo "Initializing database tables..."
    python3 -c "
from product_service.main import init_db
init_db()
"
    echo "Database tables initialized."
}

# Function to start the FastAPI application
start_fastapi_app() {
    echo "Starting FastAPI application..."
    exec uvicorn product_service.main:fastapi_app_factory --reload --host 0.0.0.0 --port 8000 --factory
}

# Run the init_db_tables function
init_db_tables

# Run the start_fastapi_app function
start_fastapi_app
