<template>
  <header class="bg-success text-white p-2 d-flex justify-content-between align-items-center custom-header">
    <div class="logo d-flex align-items-center">
      <img src="/src/assets/logo.svg" alt="Logo" style="height: 40px; margin-right: 10px; margin-left: 13px;" />
      <h6 class="m-0">MEKONG DELTA GIS APPLICATION</h6>
    </div>
    <div class="auth d-flex" >
      <p v-if="user != null">{{ user.email }}</p>
      <button @click="logout" class="btn bg-success text-white"><i class="fa-solid fa-right-from-bracket"></i></button>
    </div>
  </header>
</template>

<script>
import AuthService from '../services/auth.service';
import UserService from '../services/user.service';
export default {
  name: 'Header',
  data() {
    return {
      user: null,
    };
  },
  methods: {
    async logout() {
      this.user = null
      const response = await AuthService.logout()
      this.$router.push({ name: 'Login' });
      alert(response.message)
    },
    async check_auth(){
      this.isLoggedIn = await AuthService.check_auth()
      if(this.isLoggedIn){
        const response = await UserService.get_user_from_session()
        this.user = response.data
      }
    }
  },
  mounted() {
    this.check_auth();
  }
};
</script>
<style scoped>
  p{
    margin-bottom: 0;
    display: flex;
    align-items: center;
  }
</style>
