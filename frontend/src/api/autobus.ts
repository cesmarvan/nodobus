import { apiClient } from './config';

export const autobusService = {
    create_linea: async (data: any) => {
        const response = await apiClient.post('/autobuses', data);
        return response.data;
    },

    get_all_buses: async () => {
        const response = await apiClient.get('/autobuses');
        return response.data;
    },
    
    get_autobus_by_id: async (id: number) => {
        const response = await apiClient.get(`/autobuses/${id}`);
        return response.data;
    },

    update_autobus: async (id: number, data: any) => {
        const response = await apiClient.put(`/autobuses/${id}`, data);
        return response.data;
    },

    delete_autobus: async (id: number) => {
        const response = await apiClient.delete(`/autobuses/${id}`);
        return response.data;
    },

    get_autobuses_by_vehiculo: async (vehiculo: number) => {
        const response = await apiClient.get(`/autobuses/by-vehiculo/${vehiculo}`);
        return response.data;
    },

    get_autobuses_by_linea: async (linea_id: number) => {
        const response = await apiClient.get(`/autobuses/by-linea/${linea_id}`);
        return response.data;
    },

    get_autobuses_by_sentido: async (sentido: number) => {
        const response = await apiClient.get(`/autobuses/by-sentido/${sentido}`);
        return response.data;
    }
};
