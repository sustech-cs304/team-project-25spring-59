import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import ArcoDesign from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'


import router from './router'; // 引入路由


const app = createApp(App);
app.use(ElementPlus);
app.use(ArcoDesign);
app.use(router); // 挂载 Vue Router
app.mount('#app');

