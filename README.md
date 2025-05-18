# Family Dashboard

A modern, intelligent dashboard for family planning and organization. Built with FastAPI, Jinja2, and PostgreSQL.

## Features

- 📅 Shared Family Calendar
- 💰 Financial Control
- ✅ Task Management
- 🏥 Health Tracking
- 🍽 Meal Planning
- 📄 Document Organization
- 📚 Educational Module
- 📊 Summary Dashboard

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Jinja2 + TailwindCSS
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Template Engine**: Jinja2 (Server-side rendering)

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip (Python package manager)

## Quick Start

### Windows

1. Run the installation script:
   ```cmd
   scripts\install.bat
   ```

2. Start the application:
   ```cmd
   scripts\run.bat
   ```

### Linux/macOS

1. Run the installation script:
   ```bash
   ./scripts/install.sh
   ```

2. Start the application:
   ```bash
   ./scripts/run.sh
   ```

The application will be available at `http://localhost:8000`

## Manual Setup

If you prefer to set up the project manually:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/family-dashboard.git
   cd family-dashboard
   ```

2. Create a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file:
   ```bash
   cp dev.env.example dev.env
   ```
   Edit `dev.env` with your configuration.

5. Start PostgreSQL with Docker:
   ```bash
   docker-compose up -d postgres
   ```

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

## Development

### Environment Variables

The project uses `dev.env` for development configuration. Key variables include:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/family_dashboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=family_dashboard

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
PROJECT_NAME=Family Dashboard
```

### Docker Services

The project includes Docker Compose configuration for:
- PostgreSQL database

To manage Docker services:
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up -d --build
```

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── base.py
│   │   └── crud_user.py
│   ├── db/
│   │   ├── base.py
│   │   ├── base_class.py
│   │   └── session.py
│   ├── models/
│   │   └── user.py
│   └── schemas/
│       └── user.py
├── scripts/
│   ├── install.sh
│   ├── install.bat
│   ├── run.sh
│   └── run.bat
├── static/
├── templates/
│   ├── base.html
│   └── index.html
├── dev.env
├── docker-compose.yml
├── main.py
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 