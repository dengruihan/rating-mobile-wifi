<script setup>
import { ref, onMounted } from 'vue'

const isLoading = ref(true)

onMounted(() => {
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
              <router-link to="/wifi-models" class="nav-link">WiFi型号</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">个人中心</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/login" class="nav-link">登录</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register" class="nav-link">注册</router-link>
            </li>
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

/* 导航栏样式优化 */
.navbar {
  background: var(--primary-color);
  padding: 1rem 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  animation: fadeIn 0.6s ease;
}

.navbar-brand {
  color: rgba(84, 121, 178, 1) !important;
  font-size: 1.6rem;
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
  margin: 0 0.5rem;
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
  border-color: rgba(253, 0, 0, 1);
  transition: all 0.3s ease;
}

.navbar-toggler:hover {
  border-color: rgba(0, 0, 0, 0.5);
  transform: scale(1.05);
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.8%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

/* 页脚样式优化 */
.footer {
  background: var(--primary-color);
  color: white;
  padding: 2rem 0;
  margin-top: 2rem;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.8s ease 0.2s both;
}

.footer .text-muted {
  color: rgba(84, 121, 178, 1) !important;
  font-size: 0.9rem;
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
