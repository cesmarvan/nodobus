import { apiClient } from './config';

export const fetcherService = {
    fetch_lineas: async () => {
        const response = await apiClient.post('/fetch/lineas');
        return response.data;
    },

    fetch_paradas: async () => {
        const response = await apiClient.post('/fetch/paradas');
        return response.data;
    },

    get_real_time_buses: async (lineLabel: string) => {
        const response = await apiClient.get(`/fetch/tussam/buses/${lineLabel}`);
        return response.data;
    }
};
