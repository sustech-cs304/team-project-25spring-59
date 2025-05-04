import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Carousel from "../views/Carousel.vue";
import ImageDetail from "../views/ImageDetail.vue";
// import TrainMission from "../views/TrainMission.vue";
import Register from "../views/Register.vue";
import Transition from "../components/Transition.vue";
import BeforeLogin from "../views/BeforeLogin.vue";
import TrainMission from "../views/TrainMission.vue";
import Gym from "../views/Gym.vue";
import Share from "../views/Share.vue"
import TrainMissionSpecification from "../views/TrainMissionViews/TrainMissionSpecification.vue";
import TrainMissionPlan from "../views/TrainMissionViews/TrainMissionPlan.vue";
import TrainMissionDashboard from "../views/TrainMissionViews/TrainMissionDashboard.vue";

const routes = [
  { path: '/', redirect: '/beforeLogin' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/beforeLogin', component: BeforeLogin },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: false } },
  { path: '/carousel', component: Carousel, meta: { requiresAuth: false } }, // 主页面
  { path: '/transition', component: Transition }, // 新增过渡页面路由
  { path: '/image/:id', component: ImageDetail, meta: { requiresAuth: false } },
  { path: '/gym', component: Gym, meta: { requiresAuth: false } },
  { path: '/share', component: Share, meta: { requiresAuth: false } },

  { path: '/TrainMission', component: TrainMission, meta: { requiresAuth: false } },//训练记录主界面，记录所有的运动数据
  { path: '/TrainMission/Specification', component: TrainMissionSpecification, meta: { requiresAuth: false } },//具体的运动界面
  { path: '/TrainMission/Plans', component: TrainMissionPlan, meta: { requiresAuth: false } },//具体的运动界面
  { path: '/TrainMission/Dashboard', component: TrainMissionDashboard, meta: { requiresAuth: false } },//具体的运动界面
];

const router = createRouter({
  history: createWebHistory(),
  routes
});



  // 路由守卫：检查用户是否已登录
// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('token'); // 获取存储的 token

  // 如果从 '/' 跳转到 '/login'，则直接进入 login 页面，不经过过渡页面
  if ((from.path === '/' && to.path === '/login')
      || (from.path === '/beforeLogin' && to.path === '/login') // 从login前缓冲动画到login也不需要
      || (from.path === '/' && to.path === '/beforeLogin')
  ) {
    next(); // 直接跳转到 /login
  } else if (from.path !== '/transition' && to.path !== "/transition" && to.path !== from.path) {
    // 其他跳转都经过 /transition 页面
    next({
      path: "/transition",
      query: { redirect: to.fullPath } // 传递目标页面
    });
  } else {
    // 如果目标路由需要认证，且用户没有登录，则重定向到登录页面
    if (to.meta.requiresAuth && !isAuthenticated) {
      next('/login'); // 重定向到登录页面
    } else {
      next(); // 继续访问目标页面
    }
  }
});


export default router;
