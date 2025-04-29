import createApiClient from "./api.service"
class CommunityService {
    constructor(baseUrl = "http://localhost:5000/") {
        this.apiClient = createApiClient(baseUrl)
    }
    async create_community(credential) {
        const response = await this.apiClient.post('/create_community', {
            layer_id: credential[0],
            layer_name: credential[1],
            layer_type: credential[5],
        });
        return response
    };

    async get_all_community(){
        const response = await this.apiClient.get(`/get_all_community`)
        return response
    };

    async delete_community(credential) {
        const response = await this.apiClient.post('/delete_community', {
            layer_id: credential[0],
        });
        return response
    }

}

export default new CommunityService();