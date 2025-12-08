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
            <div class="mb-3">
              <label for="userRating" class="form-label">评分</label>
              <select id="userRating" v-model="newReview.rating" class="form-select">
                <option value="1">1星</option>
                <option value="2">2星</option>
                <option value="3">3星</option>
                <option value="4">4星</option>
                <option value="5">5星</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="userComment" class="form-label">评价内容</label>
              <textarea id="userComment" v-model="newReview.comment" class="form-control" rows="3"></textarea>
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
import wifiModelsData from '../assets/data/wifiModels.json'
import reviewsData from '../assets/data/reviews.json'

export default {
  name: 'WifiModelDetail',
  data() {
    return {
      wifiModel: null,
      modelReviews: [],
      newReview: {
        rating: 5,
        comment: ''
      }
    }
  },
  mounted() {
    this.loadWifiModel()
  },
  methods: {
    loadWifiModel() {
      const id = parseInt(this.$route.params.id)
      this.wifiModel = wifiModelsData.find(model => model.id === id)
      this.modelReviews = reviewsData.filter(review => review.wifiModelId === id)
    },
    submitReview() {
      // 模拟提交评价
      alert('评价提交成功！\n评分：' + this.newReview.rating + '星\n内容：' + this.newReview.comment)
      this.newReview = {
        rating: 5,
        comment: ''
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
</style>