#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Framily Dashboard development environment..."

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p static
mkdir -p logs

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate || source .venv/Scripts/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create dev.env if it doesn't exist
if [ ! -f "dev.env" ]; then
    echo "📝 Creating dev.env file..."
    cp dev.env.example dev.env
fi

# Start PostgreSQL with Docker Compose
echo "🐘 Starting PostgreSQL with Docker Compose..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Create database if it doesn't exist
echo "🗄️ Creating database if it doesn't exist..."
docker-compose exec postgres psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'family_dashboard'" | grep -q 1 || docker-compose exec postgres psql -U postgres -c "CREATE DATABASE family_dashboard"

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

echo "✅ Installation complete! You can now run the application with: ./scripts/run.sh" 