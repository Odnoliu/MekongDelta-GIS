<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <b-card class="shadow-lg p-4" style="width: 400px;">
      <div class="text-center mb-3">
        <b-img src="/src/assets/logo.svg" height="50" alt="Postman Logo" />
      </div>
      <h4 class="text-center mb-4">Welcome to GIS Application</h4>

      <b-form @submit.prevent="handleLogin">
        <b-form-group label="Email" label-for="email">
          <b-form-input id="email" v-model="form.email" type="text" required></b-form-input>
        </b-form-group>

        <b-form-group label="Password" label-for="password">
          <b-form-input id="password" v-model="form.password" type="password" required></b-form-input>
        </b-form-group>

        <b-button type="submit" block id="login" class="btn-hover">Sign In</b-button>
      </b-form>

      <div class="text-center my-3">or</div>

      <b-button variant="outline-secondary" block class="w-100 mb-3 btn-hover" @click="loginwithGoogle">
        <img src="/src/assets/google.svg" alt="Google" class="mr-2" height="20" /> Sign In with Google
      </b-button>
      <b-button variant="outline-secondary" block class="w-100 mb-3 btn-hover" @click="loginwithFacebook">
        <img src="/src/assets/facebook.svg" alt="Facebook" class="mr-2" height="20" /> Sign In with Facebook
      </b-button>

      <div class="text-center mt-2">
        <a href="/register">Create free account</a>
      </div>
    </b-card>
  </div>
</template>

<script>
import authService from '../../services/auth.service';
export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      errorMessage: ''
    };
  },
  methods: {
    async loginwithGoogle() {
      window.location.href = "http://localhost:5000/login_google";
    },
    async loginwithFacebook() {
      window.location.href = "http://localhost:5000/facebook/login"
    },
    async handleLogin() {
      this.errorMessage = '';

      try {
        const response = await authService.login(this.form)
        alert(response.message)
        if(response.statusCode == 200){
          this.$router.push({ name: 'Home' })
        } 
      } catch (error) {
        console.log(error)
      }
    },
  }
};
</script>
<style scoped>
.shadow-lg {
  border-radius: 10px;
}

#login {
  width: 100%;
  background-color: rgb(231, 140, 74);
  border: none;
}

.btn-hover:hover {
  transform: scale(1.05);
  transition: all 0.3s ease-in-out;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);

}
</style>
