import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { createApp } from 'vue'
import App from './App.vue'
import BootstrapVue3 from 'bootstrap-vue-3';
import router from './routes/route';
const app = createApp(App);
app.use(BootstrapVue3);
app.use(router);
app.mount('#app');
