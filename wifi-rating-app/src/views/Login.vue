<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card card-hover scroll-in">
          <div class="card-body">
            <h2 class="text-center mb-4 scroll-in scroll-in-delay-1">用户登录</h2>
            <form @submit.prevent="handleLogin">
              <div class="mb-4 scroll-in scroll-in-delay-2">
                <label for="email" class="form-label">邮箱</label>
                <input type="email" class="form-control" id="email" v-model="email" required placeholder="请输入邮箱地址">
              </div>
              <div class="mb-4 scroll-in scroll-in-delay-3">
                <div class="d-flex justify-content-between">
                  <label for="password" class="form-label">密码</label>
                  <a href="#" class="text-primary small">忘记密码？</a>
                </div>
                <input type="password" class="form-control" id="password" v-model="password" required placeholder="请输入密码">
              </div>
              <div class="mb-4 form-check scroll-in scroll-in-delay-4">
                <input type="checkbox" class="form-check-input" id="rememberMe" v-model="rememberMe">
                <label class="form-check-label" for="rememberMe">记住我</label>
              </div>
              <button type="submit" class="btn btn-primary w-100 btn-submit scroll-in scroll-in-delay-5" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                {{ isLoading ? '登录中...' : '登录' }}
              </button>
              <div class="text-center mt-3 scroll-in scroll-in-delay-6">
                <p>还没有账号？<router-link to="/register" class="text-primary">立即注册</router-link></p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  inject: ['login'],
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true
      try {
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
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
          if (data && data.message) {
            alert(data.message)
          } else {
            alert('登录成功！')
          }
          
          if (data && data.user) {
            this.login(data.user) // 调用全局登录方法，传递用户信息
            // 保存用户信息到本地存储
            localStorage.setItem('user', JSON.stringify(data.user))
            this.$router.push('/dashboard')
          } else {
            console.error('Response data missing user:', data)
            alert('登录成功，但用户信息不完整')
            this.$router.push('/dashboard')
          }
        } else {
          if (data && data.message) {
            alert(data.message)
          } else {
            console.error('Error response data:', data)
            alert('登录失败，请检查邮箱和密码')
          }
        }
      } catch (error) {
        console.error('登录失败:', error)
        console.error('错误详情:', JSON.stringify(error))
        alert('登录失败，请检查网络连接和控制台日志')
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>