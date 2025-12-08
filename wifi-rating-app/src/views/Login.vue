<template>
  <div class="container">
    <h2>用户登录</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="email" class="form-label">邮箱</label>
        <input type="email" class="form-control" id="email" v-model="email" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">密码</label>
        <input type="password" class="form-control" id="password" v-model="password" required>
      </div>
      <button type="submit" class="btn btn-primary">登录</button>
      <p class="mt-3">还没有账号？<router-link to="/register">立即注册</router-link></p>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login() {
      // 模拟登录逻辑
      alert('登录功能已触发，邮箱：' + this.email)
      this.$router.push('/dashboard')
    }
  }
}
</script>