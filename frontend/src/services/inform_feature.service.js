import createApiClient from "./api.service"
class Feature_Inform{
    constructor(baseUrl = "http://localhost:5000/") {
        this.apiClient = createApiClient(baseUrl)
    };

    async create_feature_inform(credential){
        const response = this.apiClient.post('/create_feature_inform', credential, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        return response
    };

    async get_feature_inform_by_id(credential){
        const response = await this.apiClient.get('/get_feature_inform_by_feature_id',{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            params: credential,
        })
        return response
    };
    
    async update_feature_inform(credential){
        const response = this.apiClient.put(`/update_feature_inform`, credential, {
            headers: { 'Content-Type': 'application/json' }
        });
        return response
    };

    async delete_feature_inform(credential){
        const response = this.apiClient.delete('/delete_feature_inform',{
            data: credential,
            headers: { 'Content-Type': 'application/json' }
        });
        return response
    };

    async search_data_feature(credential){
        const response = this.apiClient.get(`/search_feature_data?title=${credential}`)
        return response
    };

}
export default new Feature_Inform()