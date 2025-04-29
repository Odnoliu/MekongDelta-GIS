<template>
    <div class="home">
    <Header></Header>
    <div class="content">
      <Content></Content>
    </div>
  </div>
</template>
<script>
import Header from '../../components/header.vue';
import Content from '../../components/content.vue'
import UserService from '../../services/user.service'
import AuthService from '../../services/auth.service';
export default {
    name: 'Home',
    components: {
        Header,
        Content
    },
    methods:{
        async handleLogout(){
            const response = await AuthService.logout()
            if(response.statusCode == 200){
                 this.$router.push('/')
                alert(response.message)
            }
        }
    }
}
</script>
<style scoped>
.home {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #ececec;
}
</style>