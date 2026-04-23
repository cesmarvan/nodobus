import { apiClient } from './config';

export const paradaLineaService = {
    create_parada_linea: async (data: any) => {
        const response = await apiClient.post('/parada-lineas', data);
        return response.data;
    },

    get_parada_lineas: async () => {
        const response = await apiClient.get('/parada-lineas');
        return response.data;
    },
    
    get_parada_linea_by_id: async (id: number) => {
        const response = await apiClient.get(`/parada-lineas/${id}`);
        return response.data;
    },

    update_parada_linea: async (id: number, data: any) => {
        const response = await apiClient.put(`/parada-lineas/${id}`, data);
        return response.data;
    },

    delete_parada_linea: async (id: number) => {
        const response = await apiClient.delete(`/parada-lineas/${id}`);
        return response.data;
    },

    get_parada_lineas_by_linea_id: async (linea_id: number) => {
        const response = await apiClient.get(`/parada-lineas/by-linea/${linea_id}`);
        return response.data;
    },

    get_parada_lineas_by_parada_id: async (parada_id: number) => {
        const response = await apiClient.get(`/parada-lineas/by-parada/${parada_id}`);
        return response.data;
    },

    get_parada_lineas_relationship: async (parada_id: number, linea_id: number) => {
        const response = await apiClient.get(`/parada-lineas/parada/${parada_id}/linea/${linea_id}`);
        return response.data;
    }
};