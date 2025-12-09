<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card card-hover scroll-in">
          <div class="card-body">
            <h2 class="text-center mb-4 scroll-in scroll-in-delay-1">用户登录</h2>
            <form @submit.prevent="login">
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
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      isLoading: false
    }
  },
  methods: {
    login() {
      // 模拟登录逻辑
      this.isLoading = true
      
      // 模拟网络请求延迟
      setTimeout(() => {
        alert('登录功能已触发，邮箱：' + this.email)
        this.$router.push('/dashboard')
        this.isLoading = false
      }, 1000)
    }
  }
}
</script>