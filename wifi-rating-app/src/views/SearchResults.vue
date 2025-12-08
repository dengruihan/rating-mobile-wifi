<template>
  <div class="container">
    <h2>搜索结果</h2>
    <p v-if="searchQuery">搜索关键词："{{ searchQuery }}"</p>
    <p v-else>请输入搜索关键词</p>
    
    <div class="search-section mb-4">
      <form @submit.prevent="search">
        <div class="input-group">
          <input type="text" class="form-control" placeholder="搜索WiFi型号或品牌" v-model="searchQuery">
          <button class="btn btn-primary" type="submit">搜索</button>
        </div>
      </form>
    </div>
    
    <div v-if="searchResults.length === 0">
      <p>没有找到匹配的WiFi型号</p>
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
import wifiModelsData from '../assets/data/wifiModels.json'

export default {
  name: 'SearchResults',
  data() {
    return {
      searchQuery: '',
      allWifis: wifiModelsData
    }
  },
  computed: {
    searchResults() {
      if (!this.searchQuery) return []
      
      const query = this.searchQuery.toLowerCase()
      return this.allWifis.filter(wifi => 
        wifi.name.toLowerCase().includes(query) ||
        wifi.brand.toLowerCase().includes(query) ||
        wifi.model.toLowerCase().includes(query)
      )
    }
  },
  mounted() {
    // 从URL参数获取搜索查询
    if (this.$route.query.q) {
      this.searchQuery = this.$route.query.q
    }
  },
  methods: {
    search() {
      this.$router.push({ name: 'SearchResults', query: { q: this.searchQuery } })
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