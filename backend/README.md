# Backend

This backend is structured as a single FastAPI application with one entry point at `main.py`.

## Structure

```
backend/
  main.py
  core/
    config.py
  services/
    incidencias/
      router.py
    tiempo_real/
      router.py
```

## Run

From the `backend` folder:

```bash
uvicorn main:app --reload
```

## Available routes

- `/`
- `/api/incidencias/`
- `/api/incidencias/health`
- `/api/tiempo-real/`
- `/api/tiempo-real/health`