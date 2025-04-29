import createApiClient from "./api.service"

class ProjectService{
    constructor(baseUrl = "http://localhost:5000/") {
                    this.apiClient = createApiClient(baseUrl)
            };
    async create_project(credential){
        const response = await this.apiClient.post('/create_project', credential, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response
    };
    async get_all_project(){
        const response = await this.apiClient.get('/get_all_project')
        return response
    };
    async get_project_by_id(credential){
        const response = await this.apiClient.get(`/get_project_by_id?id=${credential}`)
        return response
    };
    async update_project(credential){
        const response = await this.apiClient.post('/update_project', credential, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response
    };
    async delete_project(credential){
        const response = await this.apiClient.get(`/delete_project?id=${credential}`)
        return response
    };
}

export default new ProjectService()