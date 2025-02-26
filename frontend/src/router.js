import { createRouter, createWebHistory } from 'vue-router';
import Login from './pages/auth/Login.vue';
import Register from './pages/auth/Register.vue';
import AdminDashboard from './pages/AdminDashboard.vue';
const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin/dashboard', component: AdminDashboard }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;