import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import router from './router'; // 引入路由

const app = createApp(App);
app.use(ElementPlus);
app.use(router); // 挂载 Vue Router
app.mount('#app');