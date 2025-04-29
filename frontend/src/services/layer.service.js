import createApiClient from "./api.service"

class LayerService {
    constructor(baseUrl = "http://localhost:5000/") {
                this.apiClient = createApiClient(baseUrl)
        }

    async create_default_layer(credential){
        const response = await this.apiClient.post('/create_default_layer', credential)
        return response
    };

    async create_file_layer(credential){
        try {
            const response = await this.apiClient.post('/create_file_layer', credential, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            return response;
        } catch (error) {
            console.error('Error creating file layer:', error.response?.data || error.message);
            throw error;
        }
    };

    async proxy_wms_capabilities(credential){
        const response = await this.apiClient.get(`/proxy_wms_capabilities?wms_url=${encodeURIComponent(credential)}`)
        return response
    };

    async create_wms_layer(credential){
        const response = await this.apiClient.post('/create_wms_layer', credential, {
            headers : { "Content-Type": "multipart/form-data"},
        });
        return response
    };
    async create_layer_from_layer(credential){
        try{
            const response = await this.apiClient.post('/create_layer_from_layer', credential, {
                headers : { "Content-Type": "multipart/form-data"},
            })
            return response
        }catch (error) {
            console.error('Error creating layer from layer:', error.response?.data || error.message);
            throw error;
        }
    }
    async get_all_layer(credential){
        const response = await this.apiClient.get(`/get_all_layer?project_id=${credential}`)
        return response
    };

    async get_all_layer_by_type(credential){
        const response = await this.apiClient.get('/get_layer_by_type',{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            params: credential,
        })
        return response
    };

    async get_layer_by_id(credential){
        const response = await this.apiClient.get(`/get_layer_by_id?layer_id=${credential}`)
        return response
    };

    async update_layer(credential){
        const response = await this.apiClient.post('/update_layer', credential)
        return response
    };
    async update_status_layer(credential){
        const response = await this.apiClient.post('/update_status',{
            id: credential[0],
            status: credential[11]
        });
        return response
    };

    async update_priority_layer(credential){
        const response = await this.apiClient.post('/update_priority',{
            id: credential[0],
            priority: credential[10]
        });
        return response
    };

    async update_vector_layer(credential){
        const response = await this.apiClient.post('/update_vector_layer', credential, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response
    };

    async update_tile_layer(credential){
        const response = await this.apiClient.post('/update_tile_layer', credential, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response
    };

    async delete_layer(credential){
        const response = await this.apiClient.get(`/delete?layer_id=${credential}`)
        return response
    };

    async get_max_z_index(credential){
        const response = await this.apiClient.get(`/get_max_z_index?project_id=${credential}`)
        return response
    };
}

export default new LayerService();