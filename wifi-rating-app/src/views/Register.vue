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
        
        console.log('Response status:', response.status)
        console.log('Response headers:', Object.fromEntries(response.headers.entries()))
        
        const text = await response.text()
        console.log('Response text:', text)
        
        let data
        try {
          data = JSON.parse(text)
          console.log('Parsed data:', data)
        } catch (parseError) {
          console.error('JSON parse error:', parseError)
          alert('服务器响应格式错误')
          return
        }
        
        if (response.ok) {
          // 如果注册时返回了token（后端已经实现），可以选择自动登录或跳转到登录页
          // 这里选择跳转到登录页，让用户手动登录
          if (data && data.message) {
            alert(data.message)
          } else {
            alert('注册成功！请登录')
          }
          this.$router.push('/login')
        } else {
          if (data && data.message) {
            alert(data.message)
          } else if (data && typeof data === 'object') {
            // 如果是验证错误，显示所有错误信息
            const errors = Object.values(data).flat().join('\n')
            alert(errors)
          } else {
            console.error('Error response data:', data)
            alert('注册失败，请稍后重试')
          }
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