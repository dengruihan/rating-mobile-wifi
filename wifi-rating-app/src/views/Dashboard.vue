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
                <h6>{{ review.wifiName }}</h6>
                <div class="rating">
                  <span class="star" v-for="n in 5" :key="n">
                    {{ n <= review.rating ? '★' : '☆' }}
                  </span>
                </div>
                <p class="comment">{{ review.comment }}</p>
                <p class="date">{{ review.date }}</p>
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
export default {
  name: 'Dashboard',
  inject: ['currentUser'],
  data() {
    return {
      userReviews: [
        {
          id: 1,
          wifiName: '华为随行WiFi 3',
          rating: 5,
          comment: '信号非常稳定，在山区也能正常使用，续航时间很长，非常满意！',
          date: '2024-01-15'
        },
        {
          id: 2,
          wifiName: '小米移动WiFi',
          rating: 4,
          comment: '性价比很高，信号不错，适合日常使用。',
          date: '2024-01-10'
        }
      ],
      favorites: [
        { id: 1, name: '华为随行WiFi 3', rating: 4.5 },
        { id: 4, name: '中兴MF920U', rating: 4.6 }
      ]
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