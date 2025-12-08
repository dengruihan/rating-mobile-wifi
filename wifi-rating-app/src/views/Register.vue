<template>
  <div class="container">
    <h2>用户注册</h2>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label for="username" class="form-label">用户名</label>
        <input type="text" class="form-control" id="username" v-model="username" required>
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">邮箱</label>
        <input type="email" class="form-control" id="email" v-model="email" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">密码</label>
        <input type="password" class="form-control" id="password" v-model="password" required>
      </div>
      <button type="submit" class="btn btn-primary">注册</button>
      <p class="mt-3">已有账号？<router-link to="/login">立即登录</router-link></p>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: ''
    }
  },
  methods: {
    register() {
      // 模拟注册逻辑
      alert('注册功能已触发，用户名：' + this.username)
      this.$router.push('/login')
    }
  }
}
</script>