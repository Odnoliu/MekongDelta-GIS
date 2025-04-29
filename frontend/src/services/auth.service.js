import createApiClient from "./api.service"

class AuthService {
    constructor(baseUrl = "http://localhost:5000/") {
        this.apiClient = createApiClient(baseUrl)
    }
    
    async fetchUserInfoGoogle() {
        try {
          const response = await this.apiClient.get("/user-info-google");
          const user = response.data;
          console.log(user)
          return user
        } catch (error) {
          console.error("Lỗi khi lấy thông tin người dùng:", error);
        }
      };
    async fetchUserInfoFacebook(){
      try {
        const response = await this.apiClient.get("/user-info-facebook");
        const user = response.data;
        console.log(user)
        return user
      } catch (error) {
        console.error("Lỗi khi lấy thông tin người dùng:", error);
      }
    };
    async logout(){
      try {
        const response = await this.apiClient.get("/logout");
        return response.data
      } catch (error) {
        console.error("Lỗi khi đăng xuất:", error);
        return error.response.data
      }
    };
    async register(creDentials) {
      try {
          const response = await this.apiClient.post("/register", creDentials)
          return response.data;
      } catch (error) {
          return error.response.data
      }
    };
    async login(creDentials){
      try {
          const response = await this.apiClient.post("/login", creDentials)
          return response.data;
      } catch (error) {
          return error.response.data
      }
    };
    async check_auth(){
      try{
        const response = await this.apiClient.get("/check_login")
        return response.data.logged_in;
      } catch (error){
        return false;
      }
    }
}

export default new AuthService();