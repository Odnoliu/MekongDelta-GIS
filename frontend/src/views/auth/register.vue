<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <b-card class="shadow-lg p-4" style="width: 400px;">
      <div class="text-center mb-3">
        <b-img src="/src/assets/logo.svg" height="50" alt="Postman Logo" />
      </div>
      <h4 class="text-center mb-4">Create Web GIS Account</h4>

      <b-form @submit.prevent="handleRegister">
        <b-form-group label="Email" label-for="email">
          <b-form-input id="email" v-model="form.email" type="text" required></b-form-input>
        </b-form-group>

        <b-form-group label="Password" label-for="password">
          <b-form-input id="password" v-model="form.password" type="password" required></b-form-input>
        </b-form-group>

        <b-form-group label="Retype password" label-for="password">
          <b-form-input id="Retype_password" v-model="form.Retype_password" type="password" required></b-form-input>
        </b-form-group>

        <b-button type="submit" block id="login" class="btn-hover">Register</b-button>

        <div class="text-center my-3">or</div>

        <b-button variant="outline-secondary" block class="w-100 mb-3 btn-hover" @click="loginwithGoogle">
          <img src="/src/assets/google.svg" alt="Google" class="mr-2" height="20" /> Sign In with Google
        </b-button>
        <b-button variant="outline-secondary" block class="w-100 mb-3 btn-hover" @click="loginwithFacebook">
          <img src="/src/assets/facebook.svg" alt="Facebook" class="mr-2" height="20" /> Sign In with Facebook
        </b-button>
      </b-form>

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
        password: '',
        Retype_password: ''
      },
      errorMessage: ''
    };
  },
  methods: {
    async loginwithGoogle() {
      window.location.href = "http://localhost:5000/login_google";
      this.loginSuccess = true;
    },
    async loginwithFacebook() {
      window.location.href = "http://127.0.0.1:5000/facebook/login"
      this.loginSuccess = true;
    },
    async handleRegister() {
      if (this.form.password !== this.form.Retype_password) {
            alert('Nhập khẩu của bạn không khớp')
            return;
      }

      try {
        const form = {
          email: this.form.email,
          password: this.form.password
        }
        const response = await authService.register(form)
        alert(response.message)
        if(response.statusCode == 200){
          this.$router.push({ name: 'Login' })
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
