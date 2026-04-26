import axios from 'axios';

// Configuración base para el backend (asumiendo FastAPI por defecto en el puerto 8000)
export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});
