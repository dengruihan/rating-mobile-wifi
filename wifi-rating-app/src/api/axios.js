import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：添加token到请求头
apiClient.interceptors.request.use(
  (config) => {
    // 优先检查sessionStorage，然后检查localStorage
    let token = sessionStorage.getItem('token')
    if (!token) {
      token = localStorage.getItem('token')
    }
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    // 如果是FormData，删除默认的Content-Type，让浏览器自动设置
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：处理401未授权错误
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token过期或无效，清除所有存储并跳转到登录页
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('storageType')
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('user')
      sessionStorage.removeItem('storageType')
      // 只有在非登录/注册页面时才跳转
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient

