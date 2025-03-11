import { createRouter, createWebHistory } from 'vue-router';
import Login from './pages/Login.vue';
import Register from './pages/Register.vue';
import AdminDashboard from './pages/AdminDashboard.vue';
import AdminQuiz from './pages/AdminQuiz.vue';
import AdminSummary from './pages/AdminSummary.vue';

import UserDashboard from './pages/UserDashboard.vue';
import UserAttemptQuiz from './pages/UserAttemptQuiz.vue';
import UserScores from './pages/UserScores.vue';
import UserSummary from './pages/UserSummary.vue';

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
  },
  {
    path: '/admin/summary',
    component: AdminSummary,
    meta: { requiresAuth: true }
  },
  {
    path: '/user/dashboard',
    component: UserDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/user/scores',
    component: UserScores,
    meta: { requiresAuth: true }
  },
  {
    path: '/user/summary',
    component: UserSummary,
    meta: { requiresAuth: true }
  },
  {
    path: '/user/quiz/:id',
    component: UserAttemptQuiz,
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