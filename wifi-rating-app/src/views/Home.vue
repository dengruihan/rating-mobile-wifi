<template>
  <div class="container">
    <h1>移动WiFi评级网站</h1>
    <p>查找和评价最佳的移动WiFi服务</p>
    
    <div class="search-section">
      <form @submit.prevent="search">
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="搜索WiFi型号或地点" v-model="searchQuery">
          <button class="btn btn-primary" type="submit">搜索</button>
        </div>
      </form>
    </div>
    
    <h2>推荐WiFi热点</h2>
    <div class="row">
      <div class="col-md-4" v-for="wifi in recommendedWifis" :key="wifi.id">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">{{ wifi.name }}</h5>
            <p class="card-text">{{ wifi.location }}</p>
            <div class="rating">
              <span class="star" v-for="n in 5" :key="n">
                {{ n <= wifi.rating ? '★' : '☆' }}
              </span>
            </div>
            <router-link :to="'/wifi-model/' + wifi.id" class="btn btn-primary">查看详情</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      searchQuery: '',
      recommendedWifis: [
        { id: 1, name: '华为随行WiFi 3', location: '北京', rating: 4.5 },
        { id: 2, name: '小米移动WiFi', location: '上海', rating: 4.2 },
        { id: 3, name: '腾讯随身WiFi', location: '广州', rating: 3.9 }
      ]
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
</style>