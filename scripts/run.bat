@echo off
echo 🚀 Starting Framily...

REM Check if Docker Desktop is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop is not running.
    echo Please start Docker Desktop and try again.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check if PostgreSQL container is running
docker compose ps postgres | findstr "Up" >nul
if errorlevel 1 (
    echo 🐘 Starting PostgreSQL...
    docker compose up -d postgres
    if errorlevel 1 (
        echo ❌ Failed to start PostgreSQL container.
        echo Please make sure Docker Desktop is running and try again.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
    echo ⏳ Waiting for PostgreSQL to be ready...
    timeout /t 10 /nobreak >nul
)

REM Check if virtual environment exists
if not exist .venv (
    echo ❌ Virtual environment not found.
    echo Please run scripts\install.bat first.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    echo Please run scripts\install.bat to set up the environment.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check if dev.env exists
if not exist dev.env (
    echo ❌ dev.env file not found.
    echo Please copy dev.env.example to dev.env and update the values.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Load environment variables
echo 🔧 Loading environment variables...
for /f "tokens=*" %%a in ('type dev.env ^| findstr /v "^#"') do set %%a

REM Start the application
echo 🌐 Starting FastAPI application...
uvicorn main:app --reload --host 0.0.0.0 --port 8000
if errorlevel 1 (
    echo ❌ Failed to start the application.
    echo Please check the error message above.
    echo Press any key to exit...
    pause >nul
    exit /b 1
) 