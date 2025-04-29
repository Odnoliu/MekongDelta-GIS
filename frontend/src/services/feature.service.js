import createApiClient from "./api.service"

class FeatureService {
    constructor(baseUrl = "http://localhost:5000/") {
         this.apiClient = createApiClient(baseUrl)
    };
    async get_default_feature(){
        const response = this.apiClient.get('/get_default_feature')
        return response
    };
    
    async get_feature_by_layer_id(credential){
        const response = this.apiClient.get(`/get_feature_by_layer_id?layer_id=${credential}`)
        return response
    };

    async get_default_feature_by_id(credential){
        const response = await this.apiClient.get('/get_default_feature_by_feature_id',{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            params: credential,
        })
        return response
    };

    async get_feature_by_id(credential){
        const response = await this.apiClient.get('/get_feature_by_feature_id',{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            params: credential,
        })
        return response
    };

    async create_draw_feature(credential){
        const response = this.apiClient.post('/create_draw_feature',{
            headers: {
                'Content-Type': 'application/json',
              },
            body: JSON.stringify(credential),
        })
        return response
    };

    async delete_feature(credential){
        const response = await this.apiClient.get(`/delete_feature?feature_id=${credential}`)
        return response
    };
}

export default new FeatureService()