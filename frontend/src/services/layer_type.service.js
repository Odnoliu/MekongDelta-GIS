import createApiClient from "./api.service"
class LayerTypeService{
    constructor(baseUrl = "http://localhost:5000/") {
                    this.apiClient = createApiClient(baseUrl)
            }
    async get_all_layer_type(){
        const response = await this.apiClient.get('/get_all_layer_type')
        return response
    }

}

export default new LayerTypeService();