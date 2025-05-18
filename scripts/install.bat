@echo off
echo 🚀 Setting up Family Dashboard development environment...

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist static mkdir static
if not exist logs mkdir logs

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is not installed. Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. It should come with Python installation.
    echo Try reinstalling Python and make sure to check "Add Python to PATH" during installation.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check if Docker Desktop is installed and running
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not in PATH.
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    echo After installation:
    echo 1. Make sure Docker Desktop is running
    echo 2. Add Docker to PATH if not already done
    echo 3. Restart your computer
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo 🔧 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies.
    echo Please check your internet connection and try again.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Create dev.env if it doesn't exist
if not exist dev.env (
    echo 📝 Creating dev.env file...
    copy dev.env.example dev.env
    if not exist dev.env (
        echo ❌ Failed to create dev.env file.
        echo Please copy dev.env.example to dev.env manually and update the values.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
)

REM Check if Docker Desktop is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop is not running.
    echo Please start Docker Desktop and try again.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Start PostgreSQL with Docker Compose
echo 🐘 Starting PostgreSQL with Docker Compose...
docker compose up -d postgres
if errorlevel 1 (
    echo ❌ Failed to start PostgreSQL container.
    echo Please make sure Docker Desktop is running and try again.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Wait for PostgreSQL to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 10 /nobreak >nul

REM Create database if it doesn't exist
echo 🗄️ Creating database if it doesn't exist...
docker compose exec postgres psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'family_dashboard'" | findstr "1" >nul
if errorlevel 1 (
    docker compose exec postgres psql -U postgres -c "CREATE DATABASE family_dashboard"
)

REM Run database migrations
echo 🔄 Running database migrations...
alembic upgrade head

echo ✅ Installation complete! You can now run the application with: scripts\run.bat
echo Press any key to exit...
pause >nul 