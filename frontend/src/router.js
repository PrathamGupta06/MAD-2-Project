import { createRouter, createWebHistory } from 'vue-router';
import Login from './pages/auth/Login.vue';
import Register from './pages/auth/Register.vue';
import AdminDashboard from './pages/AdminDashboard.vue';
import AdminQuiz from './pages/AdminQuiz.vue';
const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { 
    path: '/admin/dashboard', 
    component: AdminDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/quiz',
    component: AdminQuiz,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token');
    if (!token) {
      next('/login');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;