<template>
  <div class="container">
    <div class="d-flex align-items-center mb-3">
      <button class="btn btn-outline-secondary me-3" @click="goBack" title="返回">
        <i class="bi bi-arrow-left"></i> 返回
      </button>
      <h2 class="mb-0">搜索结果</h2>
    </div>
    <p v-if="searchQuery" class="mb-4">搜索关键词："{{ searchQuery }}"</p>
    
    <div class="search-section mb-4">
      <form @submit.prevent="search">
        <div class="input-group">
          <input type="text" class="form-control" placeholder="搜索WiFi型号或品牌" v-model="searchQuery" @input="handleSearchInput">
          <button class="btn btn-primary" type="submit">搜索</button>
        </div>
      </form>
    </div>
    
    <div v-if="loading" class="text-center">
      <p>加载中...</p>
    </div>
    <div v-else-if="searchResults.length === 0">
      <div class="alert alert-warning">
        <p>没有找到匹配的WiFi型号</p>
        <router-link to="/" class="btn btn-outline-primary">返回首页</router-link>
      </div>
    </div>
    <div v-else>
      <div class="row">
        <div class="col-md-4" v-for="wifi in searchResults" :key="wifi.id">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">{{ wifi.name }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ wifi.brand }} - {{ wifi.model }}</h6>
              <div class="rating">
                <span class="star" v-for="n in 5" :key="n">
                  {{ n <= wifi.rating ? '★' : '☆' }}
                </span>
                <span class="rating-value">{{ wifi.rating }}</span>
              </div>
              <p><strong>价格：</strong>¥{{ wifi.price }}</p>
              <router-link :to="'/wifi-model/' + wifi.id" class="btn btn-primary">查看详情</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../api/axios'

export default {
  name: 'SearchResults',
  data() {
    return {
      searchQuery: '',
      allWifis: [],
      loading: false
    }
  },
  computed: {
    searchResults() {
      // 如果搜索关键词为空，返回所有WiFi型号
      if (!this.searchQuery || this.searchQuery.trim() === '') {
        return this.allWifis
      }
      
      const query = this.searchQuery.toLowerCase().trim()
      return this.allWifis.filter(wifi => {
        const name = (wifi.name || '').toLowerCase()
        const brand = (wifi.brand || '').toLowerCase()
        const model = (wifi.model || '').toLowerCase()
        const description = (wifi.description || '').toLowerCase()
        
        return name.includes(query) ||
               brand.includes(query) ||
               model.includes(query) ||
               description.includes(query)
      })
    }
  },
  watch: {
    '$route.query.q'(newQuery) {
      if (newQuery !== undefined) {
        this.searchQuery = newQuery || ''
      }
    },
    searchQuery(newVal) {
      // 如果搜索关键词被清空，清除URL查询参数但保持在搜索结果页面
      if (!newVal || newVal.trim() === '') {
        if (this.$route.query.q) {
          this.$router.replace({ name: 'SearchResults' })
        }
      }
    }
  },
  async mounted() {
    // 从URL参数获取搜索查询
    if (this.$route.query.q) {
      this.searchQuery = this.$route.query.q
    }
    await this.loadWifiModels()
  },
  methods: {
    async loadWifiModels() {
      this.loading = true
      try {
        const response = await apiClient.get('/wifi-models/')
        const list = response.data || []
        // 兼容后端蛇形字段，映射为前端使用的字段名
        this.allWifis = list.map(item => ({
          ...item,
          signalStrength: item.signalStrength ?? item.signal_strength,
          reviewCount: item.reviewCount ?? item.review_count
        }))
      } catch (error) {
        console.error('加载WiFi型号列表失败:', error)
        this.allWifis = []
      } finally {
        this.loading = false
      }
    },
    search() {
      if (!this.searchQuery || this.searchQuery.trim() === '') {
        // 如果搜索关键词为空，清除URL查询参数但保持在搜索结果页面（显示所有产品）
        this.$router.replace({ name: 'SearchResults' })
        return
      }
      this.$router.push({ name: 'SearchResults', query: { q: this.searchQuery.trim() } })
    },
    handleSearchInput() {
      // 当用户清空搜索框时，清除URL查询参数但保持在搜索结果页面（显示所有产品）
      if (!this.searchQuery || this.searchQuery.trim() === '') {
        if (this.$route.query.q) {
          this.$router.replace({ name: 'SearchResults' })
        }
      }
    },
    goBack() {
      // 如果浏览器历史记录中有上一页，则返回上一页，否则返回首页
      if (window.history.length > 1) {
        this.$router.go(-1)
      } else {
        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped>
.rating {
  color: #ffc107;
  font-size: 1.2rem;
  margin: 10px 0;
}

.star {
  margin-right: 2px;
}

.rating-value {
  margin-left: 5px;
  color: #666;
  font-size: 0.9rem;
}
</style>