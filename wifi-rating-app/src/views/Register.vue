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
      <button type="submit" class="btn btn-primary" :disabled="isLoading">
        <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
        {{ isLoading ? '注册中...' : '注册' }}
      </button>
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
      password: '',
      isLoading: false
    }
  },
  methods: {
    async register() {
      this.isLoading = true
      try {
        const response = await fetch('http://127.0.0.1:8000/api/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          })
        })
        
        const data = await response.json()
        
        if (response.ok) {
          alert(data.message)
          this.$router.push('/login')
        } else {
          alert(data.message)
        }
      } catch (error) {
        console.error('注册失败:', error)
        console.error('错误详情:', JSON.stringify(error))
        alert('注册失败，请检查网络连接和控制台日志')
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>