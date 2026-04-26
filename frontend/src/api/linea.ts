import { apiClient } from './config';

export const lineaService = {
    create_linea: async (data: any) => {
        const response = await apiClient.post('/lineas', data);
        return response.data;
    },

    get_lineas: async () => {
        const response = await apiClient.get('/lineas');
        return response.data;
    },
    
    get_linea_by_id: async (id: number) => {
        const response = await apiClient.get(`/lineas/${id}`);
        return response.data;
    },

    update_linea: async (id: number, data: any) => {
        const response = await apiClient.put(`/lineas/${id}`, data);
        return response.data;
    },

    delete_linea: async (id: number) => {
        const response = await apiClient.delete(`/lineas/${id}`);
        return response.data;
    },

    get_linea_by_numero: async (numero: number) => {
        const response = await apiClient.get(`/lineas/by-numero/${numero}`);
        return response.data;
    },

    get_lineas_by_nombre: async (nombre: string) => {
        const response = await apiClient.get(`/lineas/search/${nombre}`);
        return response.data;
    },

    get_lineas_by_color: async (color: string) => {
        const response = await apiClient.get(`/lineas/by-color/${color}`);
        return response.data;
    }
};