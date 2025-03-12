import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Carousel from "../views/Carousel.vue";
import ImageDetail from "../views/ImageDetail.vue";
import TrainMission from "../views/TrainMission.vue";
import Register from "../views/Register.vue";

const routes = [
  { path: '/', redirect: '/login' }, // 默认跳转到登录页
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } }, // 需要认证的路由
  { path: '/carousel', component: Carousel, meta: { requiresAuth: true } }, // 需要认证的路由
  { path: '/trainMission', component: TrainMission, meta: { requiresAuth: true } }, // 需要认证的路由
  { path: '/image/:id', component: ImageDetail, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由守卫：检查用户是否已登录
router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('token'); // 获取存储在 localStorage 的 token

  // 如果目标路由需要认证，且用户没有登录，则重定向到登录页面
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // 重定向到登录页面
  } else {
    next(); // 继续访问目标页面
  }
});

export default router;
