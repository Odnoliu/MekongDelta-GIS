import createApiClient from "./api.service"

class UserService{
    constructor(baseUrl = "http://localhost:5000/") {
            this.apiClient = createApiClient(baseUrl)
    }
    async get_user_from_session(){
        try{
            const response = await this.apiClient.get('/get_user_from_session',{
                credentials: "include" //Giữ session khi request
            });
            return response
        }catch (error) {
            console.error("Lỗi khi lấy dữ liệu user:", error);
            return error
        }
    }
}
export default new UserService();