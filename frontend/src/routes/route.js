import { createRouter, createWebHistory } from 'vue-router';
import authService from '../services/auth.service';
// Import các view
import Login from '../views/auth/login.vue';
import Register from '../views/auth/register.vue';
import Home from '../views/home/home.vue';
import Map from '../views/home/map.vue'
const routes = [
    {
      path: '/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      meta: { requiresAuth: true}
    },
    {
      path: '/map/:id',
      name: 'Map',
      component: Map,
      props: true,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ];

// Tạo router
const router = createRouter({
    history: createWebHistory(),
    routes,
  });

router.beforeEach(async (to, from, next) =>{
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const isAuthenticated = await authService.check_auth();

    if(isAuthenticated) {
      next();
    } else {
      next({ name: 'Login'});
    }
  } else {
    next();
  }
});

export default router;