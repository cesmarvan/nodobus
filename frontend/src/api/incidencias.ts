import { apiClient } from './config';

export const incidenciaService = {
    create_incidencia: async (data: any) => {
        const response = await apiClient.post('/incidencias', data);
        return response.data;
    },

    get_incidencias: async () => {
        const response = await apiClient.get('/incidencias');
        return response.data;
    },

    get_incidencia_by_id: async (id: number) => {
        const response = await apiClient.get(`/incidencias/${id}`);
        return response.data;
    },

    update_incidencia: async (id: number, data: any) => {
        const response = await apiClient.put(`/incidencias/${id}`, data);
        return response.data;
    },

    delete_incidencia: async (id: number) => {
        const response = await apiClient.delete(`/incidencias/${id}`);
        return response.data;
    },

    get_incidencias_by_linea_id: async (linea_id: number) => {
        const response = await apiClient.get(`/incidencias/by-linea/${linea_id}`);
        return response.data;
    },

    get_incidencias_by_parada_id: async (parada_id: number) => {
        const response = await apiClient.get(`/incidencias/by-parada/${parada_id}`);
        return response.data;
    }
};