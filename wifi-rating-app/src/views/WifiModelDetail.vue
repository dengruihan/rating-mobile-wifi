<template>
  <div class="container">
    <div v-if="wifiModel" class="row">
      <div class="col-md-8">
        <button @click="goBack" class="btn btn-outline-secondary mb-3">
          返回
        </button>
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
          <div class="d-flex justify-content-between align-items-center">
            <h4>设备价格：¥{{ wifiModel.price }}</h4>
            <button 
              @click="toggleFavorite" 
              class="btn"
              :class="isFavorite ? 'btn-danger' : 'btn-outline-danger'"
              title="收藏"
            >
              {{ isFavorite ? '已收藏' : '收藏' }}
            </button>
          </div>
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
              <div class="d-flex align-items-center gap-2">
                <img v-if="review.avatar" :src="getAvatarUrl(review.user_id)" alt="头像" class="review-avatar" />
                <i v-else class="bi bi-person-circle review-avatar-fallback"></i>
                <h6 class="mb-0">{{ review.userName }}</h6>
              </div>
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
            <div class="mb-4 form-check">
              <input id="anonymousReview" type="checkbox" class="form-check-input" v-model="newReview.isAnonymous" />
              <label class="form-check-label" for="anonymousReview">匿名评价</label>
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
import apiClient from '../api/axios'

export default {
  name: 'WifiModelDetail',
  inject: ['isLoggedIn', 'currentUser'],
  data() {
    return {
      wifiModel: null,
      modelReviews: [],
      newReview: {
        rating: 5,
        comment: '',
        isAnonymous: false
      },
      hoverRating: 0,
      isFavorite: false
    }
  },
  computed: {
    loggedIn() {
      return this.getIsLoggedIn()
    },
    currentUserId() {
      return this.getCurrentUserId()
    }
  },
  watch: {
    // 解决“刷新详情页时 App.vue 还没恢复 currentUser，导致收藏状态不加载”
    loggedIn: {
      handler() {
        this.checkFavoriteStatus()
      },
      immediate: true
    },
    currentUserId: {
      handler() {
        this.checkFavoriteStatus()
      },
      immediate: true
    }
  },
  mounted() {
    this.loadWifiModel()
  },
  methods: {
    getIsLoggedIn() {
      return typeof this.isLoggedIn === 'object' && this.isLoggedIn !== null && 'value' in this.isLoggedIn
        ? this.isLoggedIn.value
        : !!this.isLoggedIn
    },
    getCurrentUserId() {
      if (typeof this.currentUser === 'object' && this.currentUser !== null && 'value' in this.currentUser) {
        return this.currentUser.value?.id
      }
      return this.currentUser?.id
    },
    goBack() {
      this.$router.go(-1)
    },
    // 检查当前WiFi是否已收藏
    async checkFavoriteStatus() {
      const userId = this.getCurrentUserId()
      if (this.getIsLoggedIn() && userId && this.wifiModel) {
        try {
          const response = await apiClient.get(`/favorites/${userId}/`)
          const favoriteIds = response.data.map(fav => fav?.wifi_model?.id).filter(id => typeof id === 'number')
          this.isFavorite = favoriteIds.includes(this.wifiModel.id)
        } catch (error) {
          console.error('检查收藏状态失败:', error)
        }
      }
    },
    // 切换收藏状态
    async toggleFavorite() {
      const userId = this.getCurrentUserId()
      if (!this.getIsLoggedIn() || !userId) {
        this.$router.push('/login')
        return
      }
      
      try {
        if (this.isFavorite) {
          // 取消收藏
          await apiClient.delete('/favorites/delete/', {
            data: { wifiModelId: this.wifiModel.id }
          })
          this.isFavorite = false
        } else {
          // 添加收藏
          await apiClient.post('/favorites/', {
            wifiModelId: this.wifiModel.id
          })
          this.isFavorite = true
        }
      } catch (error) {
        console.error('切换收藏状态失败:', error)
        console.error('错误详情:', error.response ? error.response.data : error.message)
        alert('操作失败，请检查网络连接')
      }
    },
    async loadWifiModel() {
      try {
        const id = parseInt(this.$route.params.id)
        const response = await apiClient.get(`/wifi-models/${id}/`)
        
        // 兼容后端蛇形字段，映射为前端模板使用的驼峰字段
        const api = response.data || {}
        this.wifiModel = {
          ...api,
          signalStrength: api.signalStrength ?? api.signal_strength,
          reviewCount: api.reviewCount ?? api.review_count,
          dataPlans: api.dataPlans ?? api.data_plans ?? []
        }
        // 获取评价
        try {
          const reviewsResponse = await apiClient.get(`/reviews/${id}/`)
          // 兼容后端蛇形字段，并处理匿名显示
          this.modelReviews = (reviewsResponse.data || []).map(r => ({
            id: r.id,
            userId: r.user_id,
            userName: r.display_name || r.user_name || '匿名',
            avatar: r.display_avatar || null,
            rating: r.rating,
            comment: r.comment,
            date: r.date
          }))
        } catch (error) {
          console.error('加载评价失败:', error)
          this.modelReviews = []
        }
        // 加载完成后检查收藏状态
        this.checkFavoriteStatus()
      } catch (error) {
        console.error('加载WiFi型号详情失败:', error)
        alert('加载WiFi型号详情失败，请检查网络连接')
      }
    },
    setRating(rating) {
      this.newReview.rating = rating
    },
    getAvatarUrl(userId) {
      return `/api/avatar/${userId}/`
    },
    async submitReview() {
      // 检查用户是否已登录
      if (!this.loggedIn) {
        this.$router.push('/login')
        return
      }
      
      try {
        const id = parseInt(this.$route.params.id)
        
        // 提交评价到后端
        await apiClient.post('/reviews/', {
          wifiModelId: id,
          rating: this.newReview.rating,
          comment: this.newReview.comment,
          isAnonymous: this.newReview.isAnonymous
        })
        
        // 重新加载WiFi型号详情，更新评价列表和平均评分
        await this.loadWifiModel()
        
        // 重置评价表单
        this.newReview = {
          rating: 5,
          comment: '',
          isAnonymous: false
        }
        this.hoverRating = 0
        
        alert('评价提交成功！')
      } catch (error) {
        console.error('提交评价失败:', error)
        console.error('错误详情:', error.response ? error.response.data : error.message)
        alert('提交评价失败，请检查网络连接或后端接口')
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

.review-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.review-avatar-fallback {
  font-size: 1.6rem;
  color: #6c757d;
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
/* 按钮文字垂直居中 */
.btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.25rem;
  line-height: 1;
  padding: 0.5rem 1rem !important;
  border-radius: 0.25rem !important;
}

/* 确保图标和文字在按钮内正确对齐 */
.btn i {
  vertical-align: middle;
  line-height: inherit;
}
</style>