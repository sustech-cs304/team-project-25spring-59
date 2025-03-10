import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Carousel from "../views/Carousel.vue";
import ImageDetail from "../views/ImageDetail.vue";
import TrainMission from "../views/TrainMission.vue";


const routes = [
  { path: '/', redirect: '/login' }, // 默认跳转到登录页
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard },
  { path: '/carousel', component: Carousel },
  { path: '/image/:id', component: ImageDetail },
  { path: '/trainMission', component: TrainMission }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
