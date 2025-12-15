<template>
  <div class="container">
    <h2>用户仪表板</h2>
    
    <div class="row">
      <div class="col-md-6">
        <div class="card mb-4">
          <div class="card-header">个人信息</div>
          <div class="card-body">
            <p><strong>用户名：</strong>{{ currentUser?.username }}</p>
            <p><strong>邮箱：</strong>{{ currentUser?.email }}</p>
            <p><strong>注册日期：</strong>{{ currentUser?.registration_date }}</p>
            <button class="btn btn-primary">编辑个人信息</button>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card mb-4">
          <div class="card-header">我的评价</div>
          <div class="card-body">
            <div v-if="userReviews.length === 0">
              <p>您还没有评价过任何WiFi设备</p>
            </div>
            <div v-else>
              <div v-for="review in userReviews" :key="review.id" class="mb-3">
                <h6>{{ review.wifiModelName }}</h6>
                <div class="rating">
                  <span class="star" v-for="n in 5" :key="n">
                    {{ n <= review.rating ? '★' : '☆' }}
                  </span>
                </div>
                <p class="comment">{{ review.comment }}</p>
                <p class="date">{{ review.createdAt }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card mb-4">
      <div class="card-header">收藏的WiFi热点</div>
      <div class="card-body">
        <div v-if="favorites.length === 0">
          <p>您还没有收藏任何WiFi设备</p>
        </div>
        <div v-else class="row">
          <div class="col-md-3" v-for="wifi in favorites" :key="wifi.id">
            <div class="card">
              <div class="card-body">
                <h6 class="card-title">{{ wifi.name }}</h6>
                <div class="rating">
                  <span class="star" v-for="n in 5" :key="n">
                    {{ n <= wifi.rating ? '★' : '☆' }}
                  </span>
                </div>
                <router-link :to="'/wifi-model/' + wifi.id" class="btn btn-sm btn-primary">查看</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Dashboard',
  inject: ['currentUser'],
  data() {
    return {
      userReviews: [],
      favorites: []
    }
  },
  mounted() {
    this.loadUserData()
  },
  methods: {
    async loadUserData() {
      if (this.currentUser && this.currentUser.value && this.currentUser.value.id) {
        try {
          // 同时获取用户评价和收藏列表
          const [reviewsResponse, favoritesResponse] = await Promise.all([
            axios.get(`http://127.0.0.1:8000/api/user-reviews/${this.currentUser.value.id}/`),
            axios.get(`http://127.0.0.1:8000/api/favorites/${this.currentUser.value.id}/`)
          ])
          
          this.userReviews = reviewsResponse.data
          this.favorites = favoritesResponse.data
        } catch (error) {
          console.error('加载用户数据失败:', error)
          alert('加载用户数据失败，请检查网络连接')
        }
      }
    }
  }
}
</script>

<style scoped>
.rating {
  color: #ffc107;
  font-size: 1rem;
  margin: 5px 0;
}

.star {
  margin-right: 2px;
}

.comment {
  font-size: 0.9rem;
  color: #666;
}

.date {
  font-size: 0.8rem;
  color: #999;
}
</style>