import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import WifiModelDetail from '../views/WifiModelDetail.vue'
import SearchResults from '../views/SearchResults.vue'
import SubmitWifiModel from '../views/SubmitWifiModel.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/submit-wifi-model', name: 'SubmitWifiModel', component: SubmitWifiModel },
  // 将WiFi型号页面重定向到首页
  { path: '/wifi-models', redirect: '/' },
  { path: '/wifi-model/:id', name: 'WifiModelDetail', component: WifiModelDetail },
  { path: '/search', name: 'SearchResults', component: SearchResults }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router