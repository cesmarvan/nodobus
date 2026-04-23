import { apiClient } from './config';

export const paradaService = {

    create_parada: async (data: any) => {
        const response = await apiClient.post('/paradas', data);
        return response.data;
    },
    
    get_paradas: async () => {
        const response = await apiClient.get('/paradas');
        return response.data;
    },
    
    get_parada_by_id: async (id: number) => {
        const response = await apiClient.get(`/paradas/${id}`);
        return response.data;
    },

    update_parada: async (id: number, data: any) => {
        const response = await apiClient.put(`/paradas/${id}`, data);
        return response.data;
    },

    delete_parada: async (id: number) => {
        const response = await apiClient.delete(`/paradas/${id}`);
        return response.data;
    },

    get_parada_by_nodo: async (nodo: number) => {
        const response = await apiClient.get(`/paradas/by-nodo/${nodo}`);
        return response.data;
    },

    get_parada_by_nombre: async (nombre: string) => {
        const response = await apiClient.get(`/paradas/search/${nombre}`);
        return response.data;
    }
};