#!/bin/bash

# Exit on error
set -e

# Function to cleanup background processes on exit
cleanup() {
    echo "🛑 Stopping application..."
    kill $(jobs -p) 2>/dev/null
}

# Register the cleanup function to be called on exit
trap cleanup EXIT

echo "🚀 Starting Framily Dashboard..."

# Check if PostgreSQL container is running
if ! docker-compose ps postgres | grep -q "Up"; then
    echo "🐘 Starting PostgreSQL..."
    docker-compose up -d postgres
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 5
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate || source .venv/Scripts/activate

# Export environment variables
echo "🔧 Loading environment variables..."
export $(cat dev.env | grep -v '^#' | xargs)

# Start the application
echo "🌐 Starting FastAPI application..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Keep the script running
wait 