import createApiClient from "./api.service"

class Flood_And_TempService {
    constructor(baseUrl = "http://localhost:5000/") {
         this.apiClient = createApiClient(baseUrl)
    };
    async get_flood_inform(){
        const response = this.apiClient.get('/get_inform_flood_area')
        return response
    }
}
export default new Flood_And_TempService()