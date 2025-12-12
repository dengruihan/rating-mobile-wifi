<template>
  <div class="container">
    <div v-if="wifiModel" class="row">
      <div class="col-md-8">
        <h2>{{ wifiModel.name }}</h2>
        <h3>{{ wifiModel.brand }} - {{ wifiModel.model }}</h3>
        
        <div class="rating mb-3">
          <span class="star" v-for="n in 5" :key="n">
            {{ n <= wifiModel.rating ? '★' : '☆' }}
          </span>
          <span class="rating-value">{{ wifiModel.rating }} ({{ wifiModel.reviewCount }}条评价)</span>
        </div>
        
        <div class="details mb-4">
          <div class="row">
            <div class="col-md-3">
              <p><strong>信号强度：</strong></p>
              <div class="progress">
                <div class="progress-bar" role="progressbar" :style="{width: wifiModel.signalStrength * 20 + '%'}" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
              <p>{{ wifiModel.signalStrength }}/5</p>
            </div>
            <div class="col-md-3">
              <p><strong>速度：</strong></p>
              <div class="progress">
                <div class="progress-bar" role="progressbar" :style="{width: wifiModel.speed * 20 + '%'}" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
              <p>{{ wifiModel.speed }}/5</p>
            </div>
          </div>
        </div>
        
        <div class="price mb-4">
          <h4>设备价格：¥{{ wifiModel.price }}</h4>
        </div>
        
        <div class="data-plans mb-4">
          <h4>资费计划</h4>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>套餐名称</th>
                <th>价格</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="plan in wifiModel.dataPlans" :key="plan.name">
                <td>{{ plan.name }}</td>
                <td>¥{{ plan.price }}/月</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="description mb-4">
          <h4>产品描述</h4>
          <p>{{ wifiModel.description }}</p>
        </div>
        
        <div class="reviews mb-4">
          <h4>用户评价</h4>
          <div v-for="review in modelReviews" :key="review.id" class="review mb-3">
            <div class="review-header">
              <h6>{{ review.userName }}</h6>
              <div class="rating">
                <span class="star" v-for="n in 5" :key="n">
                  {{ n <= review.rating ? '★' : '☆' }}
                </span>
              </div>
              <p class="date">{{ review.date }}</p>
            </div>
            <p class="comment">{{ review.comment }}</p>
          </div>
        </div>
        
        <div class="submit-review mb-4">
          <h4>提交评价</h4>
          <form @submit.prevent="submitReview">
            <div class="mb-4">
              <label class="form-label">评分</label>
              <div class="interactive-rating">
                <span class="star" v-for="n in 5" :key="n" 
                      @click="setRating(n)" 
                      @mouseenter="hoverRating = n" 
                      @mouseleave="hoverRating = 0"
                      :class="{ 'active': n <= (hoverRating || newReview.rating) }">
                  {{ n <= (hoverRating || newReview.rating) ? '★' : '☆' }}
                </span>
                <span class="rating-value ml-2">{{ newReview.rating }}星</span>
              </div>
            </div>
            <div class="mb-4">
              <label for="userComment" class="form-label">评价内容</label>
              <textarea id="userComment" v-model="newReview.comment" class="form-control" rows="3" placeholder="请分享您的使用体验..."></textarea>
            </div>
            <button type="submit" class="btn btn-primary">提交评价</button>
          </form>
        </div>
      </div>
    </div>
    <div v-else>
      <p>未找到该WiFi型号信息</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'WifiModelDetail',
  inject: ['isLoggedIn', 'currentUser'],
  data() {
    return {
      wifiModel: null,
      modelReviews: [],
      newReview: {
        rating: 5,
        comment: ''
      },
      hoverRating: 0
    }
  },
  mounted() {
    this.loadWifiModel()
  },
  methods: {
    async loadWifiModel() {
      try {
        const id = parseInt(this.$route.params.id)
        const response = await axios.get(`http://127.0.0.1:5000/api/wifi-model/${id}`)
        
        this.wifiModel = response.data.wifiModel
        this.wifiModel.dataPlans = response.data.dataPlans
        this.modelReviews = response.data.reviews
      } catch (error) {
        console.error('加载WiFi型号详情失败:', error)
        alert('加载WiFi型号详情失败，请检查网络连接')
      }
    },
    setRating(rating) {
      this.newReview.rating = rating
    },
    async submitReview() {
      // 检查用户是否已登录
      if (!this.isLoggedIn) {
        this.$router.push('/login')
        return
      }
      
      try {
        const id = parseInt(this.$route.params.id)
        
        // 提交评价到后端
        await axios.post('http://127.0.0.1:5000/api/reviews', {
          userId: this.currentUser.id,
          wifiModelId: id,
          userName: this.currentUser.username,
          rating: this.newReview.rating,
          comment: this.newReview.comment
        })
        
        // 重新加载WiFi型号详情，更新评价列表和平均评分
        await this.loadWifiModel()
        
        // 重置评价表单
        this.newReview = {
          rating: 5,
          comment: ''
        }
        this.hoverRating = 0
        
        alert('评价提交成功！')
      } catch (error) {
        console.error('提交评价失败:', error)
        alert('提交评价失败，请检查网络连接')
      }
    }
  }
}
</script>

<style scoped>
.rating {
  color: #ffc107;
  font-size: 1.2rem;
}

.star {
  margin-right: 2px;
  cursor: pointer;
}

.rating-value {
  margin-left: 5px;
  color: #666;
  font-size: 0.9rem;
}

.details {
  margin: 20px 0;
}

.progress {
  margin-bottom: 5px;
}

.review {
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.review:hover {
  background-color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.comment {
  margin: 0;
}

.date {
  font-size: 0.8rem;
  color: #999;
}

/* 交互式评分样式 */
.interactive-rating {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.interactive-rating .star {
  font-size: 2rem;
  color: #ddd;
  transition: all 0.3s ease;
  margin-right: 5px;
}

.interactive-rating .star:hover,
.interactive-rating .star.active {
  color: #ffc107;
  transform: scale(1.2);
}

.interactive-rating .rating-value {
  font-size: 1rem;
  font-weight: 500;
  margin-left: 10px;
}
</style>