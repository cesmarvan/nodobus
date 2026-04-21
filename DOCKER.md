# Docker Setup

This project includes Docker support for the complete stack: PostgreSQL + PostGIS, FastAPI backend, and React frontend.

## Prerequisites

- Docker and Docker Compose installed
- `.env` file configured (copy from `.env.example`)

## Quick Start

```bash
# Copy environment template
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## Services

### PostgreSQL + PostGIS (Port 5432)
- Image: `postgis/postgis:17-3.4`
- Default credentials (from `.env`):
  - User: `nodobus`
  - Password: `nodobus123`
  - Database: `nodobus`

### Backend API (Port 8000)
- FastAPI application at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Endpoints:
  - `GET /` - Root
  - `GET /api/incidencias/` - Incidencias service
  - `GET /api/tiempo-real/` - Real-time service
  - `GET /api/*/health` - Health checks per service

### Frontend (Port 3000)
- React application at `http://localhost:3000`
- Built with Vite and Tailwind CSS

## Common Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Stop services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v

# Rebuild services
docker-compose build --no-cache

# Run a single service
docker-compose up db
docker-compose up backend
docker-compose up frontend

# Access database shell
docker-compose exec db psql -U nodobus -d nodobus

# Rebuild and restart
docker-compose up -d --build
```

## Environment Variables

Create a `.env` file in the project root with:

```
DB_USER=nodobus
DB_PASSWORD=nodobus123
DB_NAME=nodobus
VITE_API_URL=http://localhost:8000/api
```

## Troubleshooting

### Port already in use
Change ports in `docker-compose.yml`:
- Backend: change `8000:8000` to `8001:8000`
- Frontend: change `3000:3000` to `3001:3000`
- Database: change `5432:5432` to `5433:5432`

### Database connection issues
Ensure the `db` service is healthy:
```bash
docker-compose ps db
```

Check backend logs:
```bash
docker-compose logs backend
```

### Frontend can't connect to backend
Verify `VITE_API_URL` in `.env` matches your backend URL during build.

## Accessing Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: `psql postgresql://nodobus:nodobus123@localhost:5432/nodobus`
