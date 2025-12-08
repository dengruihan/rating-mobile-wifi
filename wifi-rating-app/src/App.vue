<script setup>
</script>

<template>
  <div class="app">
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
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
    <main class="container mt-4">
      <router-view />
    </main>
    
    <!-- 页脚 -->
    <footer class="footer mt-4 py-3 bg-light">
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* 确保内容区域有适当的边距 */
.container {
  max-width: 1200px;
}

/* 页脚样式 */
.footer {
  position: relative;
  bottom: 0;
  width: 100%;
}
</style>
