<script setup>
import { ref, onMounted, provide } from 'vue'

const isLoading = ref(true)
const isLoggedIn = ref(false)
const currentUser = ref(null)

// 登录方法
const login = (user) => {
  isLoggedIn.value = true
  currentUser.value = user
}

// 退出登录方法
const logout = () => {
  isLoggedIn.value = false
  currentUser.value = null
  localStorage.removeItem('user')
  // 退出后重定向到首页
  window.location.href = '/'
}

// 提供全局登录状态和方法
provide('isLoggedIn', isLoggedIn)
provide('currentUser', currentUser)
provide('login', login)
provide('logout', logout)

onMounted(() => {
  // 检查本地存储中的用户信息
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try {
      const user = JSON.parse(savedUser)
      isLoggedIn.value = true
      currentUser.value = user
    } catch (error) {
      console.error('解析用户信息失败:', error)
      localStorage.removeItem('user')
    }
  }
  
  // 模拟页面加载
  setTimeout(() => {
    isLoading.value = false
  }, 1500)
})
</script>

<template>
  <div class="app">
    <!-- 页面加载动画 -->
    <div class="page-loading" :class="{ 'fade-out': !isLoading }">
      <div class="page-loading-content">
        <div class="spinner"></div>
        <h3>WiFi评级网站</h3>
      </div>
    </div>
    
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-light">
      <div class="container">
        <a class="navbar-brand" href="#">WiFi评级</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link">首页</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">个人中心</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <template v-if="isLoggedIn">
              <li class="nav-item">
                <router-link to="/dashboard" class="nav-link">欢迎, {{ currentUser?.username }}</router-link>
              </li>
              <li class="nav-item">
                <a href="#" class="nav-link" @click.prevent="logout">退出登录</a>
              </li>
            </template>
            <template v-else>
              <li class="nav-item">
                <router-link to="/login" class="nav-link">登录</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link">注册</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </main>
    
    <!-- 页脚 -->
    <footer class="footer">
      <div class="container text-center">
        <span class="text-muted">移动WiFi评级网站 &copy; 2024</span>
      </div>
    </footer>
  </div>
</template>

<style>
/* 全局样式 */
body {
  margin: 0;
  padding: 0;
  background-color: #f8fafc;
  background-image: none;
}

/* 主内容区 */
.main-content {
  min-height: calc(100vh - 120px);
  padding: 2rem 0;
}

/* 主内容区在小屏幕下的响应式优化 */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem 0;
  }
}

/* 确保内容区域有适当的边距 */
.container {
  max-width: 1200px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.05);
  padding: 2.5rem;
  margin-top: 2rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(0, 0, 0, 0.02);
}

/* 内容区域在小屏幕下的响应式优化 */
@media (max-width: 768px) {
  .container {
    padding: 1.5rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
}

/* 导航栏样式优化 */
.navbar {
  background: var(--primary-color);
  padding: 0.3rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 1000;
  animation: fadeIn 0.6s ease;
  border-radius: 0 0 20px 20px;
}

/* 导航栏内部容器样式 */
.navbar .container {
  background-color: transparent;
  padding: 0 1rem;
  margin-top: 0;
  margin-bottom: 0;
  box-shadow: none;
  border: none;
  border-radius: 0;
}

.navbar-brand {
  color: rgba(84, 121, 178, 1) !important;
  font-size: 1.3rem;
  font-weight: 700;
  transition: all 0.3s ease;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.23);
}

.navbar-brand:hover {
  transform: scale(1.05);
  color: rgba(84, 121, 178, 1) !important;
}

.navbar-nav .nav-link {
  color: rgba(84, 121, 178, 1) !important;
  font-weight: 600;
  margin: 0 0.3rem;
  padding: 0.3rem 0.6rem !important;
  transition: all 0.3s ease;
  position: relative;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.navbar-nav .nav-link:hover {
  color: #5f5d5dff !important;
  transform: translateY(-1px);
  text-shadow: 0 3px 6px rgba(0, 0, 0, 0.4);
}

.navbar-toggler {
  border-color: transparent;
  transition: all 0.3s ease;
}

.navbar-toggler:hover {
  border-color: rgba(0, 0, 0, 0.5);
  transform: scale(1.05);
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.8%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

/* 移动端导航栏样式优化 */
@media (max-width: 768px) {
  .navbar {
    padding: 0.2rem 0;
  }
  
  .navbar-brand {
    font-size: 1.1rem;
  }
  
  .navbar-nav {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .navbar-nav .nav-link {
    padding: 0.5rem 0 !important;
    font-size: 0.95rem;
    border-radius: 8px;
    transition: all 0.3s ease;
  }
  
  .navbar-nav .nav-link:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(0);
  }
  
  .navbar-collapse {
    text-align: center;
    padding: 0.5rem;
  }
  
  /* 优化移动端导航展开效果 */
  .navbar-collapse {
    transition: all 0.3s ease-in-out;
  }
  
  /* 增加移动端导航链接的点击区域 */
  .nav-item {
    margin: 0.2rem 0;
  }
  
  /* 确保导航菜单在小屏幕下完全展开 */
  .navbar-expand-lg .navbar-collapse {
    flex-direction: column;
  }
}

/* 页脚样式优化 */
.footer {
  background: var(--primary-color);
  color: white;
  padding: 2rem 0;
  margin-top: 2rem;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.8s ease 0.2s both;
  border-radius: 20px 20px 0 0;
}

.footer .text-muted {
  color: rgba(84, 121, 178, 1) !important;
  font-size: 0.9rem;
}

/* 页脚在小屏幕下的响应式优化 */
@media (max-width: 768px) {
  .footer {
    padding: 1.5rem 0;
    margin-top: 1rem;
  }
  
  .footer .text-muted {
    font-size: 0.85rem;
  }
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
