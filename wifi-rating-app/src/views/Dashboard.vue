<template>
  <div class="container">
    <h2>用户仪表板</h2>
    
    <div class="row dashboard-cards-row">
      <div class="col-md-6">
        <div class="card mb-4 profile-card">
          <div class="card-header">个人信息</div>
          <div class="card-body">
            <div class="d-flex align-items-center gap-3 mb-3">
              <div class="avatar-wrapper">
                <img
                  v-if="userInfo?.avatar"
                  :src="userInfo.avatar"
                  alt="头像"
                  class="avatar-img"
                />
                <i v-else class="bi bi-person-circle avatar-fallback"></i>
              </div>
              <div class="d-flex flex-column gap-2">
                <button class="btn btn-sm btn-outline-primary" @click="triggerAvatarPicker" :disabled="uploadingAvatar">
                  {{ uploadingAvatar ? '上传中...' : '更换头像' }}
                </button>
                <button v-if="userInfo?.avatar" class="btn btn-sm btn-outline-secondary" @click="clearAvatar" :disabled="uploadingAvatar">
                  清除头像
                </button>
                <input
                  ref="avatarInput"
                  type="file"
                  accept="image/*"
                  style="display:none"
                  @change="onAvatarSelected"
                />
              </div>
            </div>
            <p><strong>用户名：</strong>{{ userInfo?.username }}</p>
            <p><strong>邮箱：</strong>{{ userInfo?.email }}</p>
            <p><strong>注册日期：</strong>{{ formattedRegistrationDate }}</p>
            <button class="btn btn-primary">编辑个人信息</button>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card mb-4 reviews-card">
          <div class="card-header">我的评价</div>
          <div class="card-body reviews-container">
            <div v-if="userReviews.length === 0" class="reviews-empty">
              <p>您还没有评价过任何WiFi设备</p>
            </div>
            <div v-else class="reviews-scroll">
              <div v-for="review in userReviews" :key="review.id" class="review-item">
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
    
    <div class="card mb-4 favorites-card">
      <div class="card-header">收藏的WiFi热点</div>
      <div class="card-body favorites-container">
        <div v-if="favorites.length === 0" class="favorites-empty">
          <p>您还没有收藏任何WiFi设备</p>
        </div>
        <div v-else class="favorites-scroll">
          <div class="row">
            <div class="col-md-3" v-for="favorite in favorites" :key="favorite.id">
              <div class="card mb-3">
                <div class="card-body">
                  <h6 class="card-title">{{ favorite.wifi_model.name }}</h6>
                  <div class="rating">
                    <span class="star" v-for="n in 5" :key="n">
                      {{ n <= favorite.wifi_model.rating ? '★' : '☆' }}
                    </span>
                  </div>
                  <router-link :to="'/wifi-model/' + favorite.wifi_model.id" class="btn btn-sm btn-primary">查看</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card mb-4 submissions-card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span>我提交的 Wi-Fi 型号</span>
        <router-link to="/submit-wifi-model" class="btn btn-sm btn-primary">
          提交新型号
        </router-link>
      </div>
      <div class="card-body submissions-container">
        <div v-if="submissions.length === 0" class="submissions-empty">
          <p class="text-muted">暂无提交记录。你提交的新型号会先进入"待审核"，管理员通过后才会出现在首页列表。</p>
        </div>

        <div v-else class="submissions-scroll">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>名称</th>
                  <th>品牌/型号</th>
                  <th>状态</th>
                  <th>提交时间</th>
                  <th class="text-end">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in submissions" :key="item.id">
                  <td class="fw-semibold">{{ item.name }}</td>
                  <td class="text-muted">{{ item.brand }} / {{ item.model }}</td>
                  <td>
                    <span class="badge" :class="statusMeta(item.approval_status).badgeClass">
                      {{ statusMeta(item.approval_status).label }}
                    </span>
                  </td>
                  <td class="text-muted">{{ formatDateTime(item.submitted_at) }}</td>
                  <td class="text-end">
                    <router-link
                      v-if="item.approval_status === 'approved'"
                      :to="'/wifi-model/' + item.id"
                      class="btn btn-sm btn-primary"
                    >
                      查看
                    </router-link>
                    <button
                      v-else
                      class="btn btn-sm"
                      :class="item.approval_status === 'rejected' ? 'btn-outline-danger' : 'btn-outline-secondary'"
                      disabled
                    >
                      {{ item.approval_status === 'rejected' ? '驳回' : '待审核' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
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
      favorites: [],
      userProfile: null,
      uploadingAvatar: false,
      submissions: []
    }
  },
  mounted() {
    this.loadUserData()
  },
  computed: {
    currentUserId() {
      // currentUser 在 App.vue 中是 provide 的 ref；这里同时兼容误传普通对象
      if (this.currentUser && typeof this.currentUser === 'object' && 'value' in this.currentUser) {
        return this.currentUser.value?.id
      }
      return this.currentUser?.id
    },
    injectedUser() {
      if (this.currentUser && typeof this.currentUser === 'object' && 'value' in this.currentUser) {
        return this.currentUser.value
      }
      return this.currentUser
    },
    userInfo() {
      // 优先使用后端拉取的完整资料（含 date_joined），否则退回到本地保存的 user
      return this.userProfile || this.injectedUser
    },
    formattedRegistrationDate() {
      const raw = this.userInfo?.date_joined || this.userInfo?.registration_date
      if (!raw) return '—'
      const d = new Date(raw)
      if (Number.isNaN(d.getTime())) return String(raw)
      return d.toLocaleString()
    }
  },
  watch: {
    // 解决“刷新/直达 dashboard 时 App.vue 还没从 localStorage 恢复 currentUser”
    currentUserId: {
      handler() {
        this.loadUserData()
        this.loadUserProfile()
        this.loadUserSubmissions()
      },
      immediate: true
    }
  },
  methods: {
    statusMeta(status) {
      if (status === 'approved') return { label: '已通过', badgeClass: 'bg-success' }
      if (status === 'rejected') return { label: '已驳回', badgeClass: 'bg-danger' }
      return { label: '待审核', badgeClass: 'bg-warning text-dark' }
    },
    formatDateTime(raw) {
      if (!raw) return '—'
      const d = new Date(raw)
      if (Number.isNaN(d.getTime())) return String(raw)
      return d.toLocaleString()
    },
    triggerAvatarPicker() {
      if (this.$refs.avatarInput) this.$refs.avatarInput.click()
    },
    async onAvatarSelected(event) {
      const file = event.target.files && event.target.files[0]
      if (!file) return

      // 简单限制：避免把超大图片 base64 写进 sqlite
      const maxBytes = 800 * 1024 // 800KB
      if (file.size > maxBytes) {
        alert('图片过大，请选择小于 800KB 的图片（建议截图/压缩后再上传）')
        event.target.value = ''
        return
      }

      const reader = new FileReader()
      reader.onload = async () => {
        const dataUrl = reader.result
        if (typeof dataUrl !== 'string') return
        await this.updateAvatar(dataUrl)
        event.target.value = ''
      }
      reader.readAsDataURL(file)
    },
    async clearAvatar() {
      await this.updateAvatar('')
    },
    async updateAvatar(avatar) {
      if (!this.currentUserId) return
      this.uploadingAvatar = true
      try {
        const response = await axios.patch(`http://127.0.0.1:8000/api/users/${this.currentUserId}/`, { avatar })
        this.userProfile = response.data

        // 同步更新全局 currentUser（App.vue provide 的 ref）
        if (this.currentUser && typeof this.currentUser === 'object' && 'value' in this.currentUser && this.currentUser.value) {
          this.currentUser.value.avatar = response.data.avatar
        }
        // 同步本地缓存（用于刷新恢复）
        const saved = localStorage.getItem('user')
        if (saved) {
          try {
            const u = JSON.parse(saved)
            u.avatar = response.data.avatar
            localStorage.setItem('user', JSON.stringify(u))
          } catch {
            // ignore
          }
        }
      } catch (error) {
        console.error('更新头像失败:', error)
        console.error('错误详情:', error.response ? error.response.data : error.message)
        alert('更新头像失败，请检查网络连接或后端接口')
      } finally {
        this.uploadingAvatar = false
      }
    },
    async loadUserProfile() {
      if (!this.currentUserId) return
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/users/${this.currentUserId}/`)
        this.userProfile = response.data
      } catch (error) {
        // 不影响页面其他部分，静默降级到 injectedUser
        console.error('加载用户资料失败:', error)
      }
    },
    async loadUserSubmissions() {
      if (!this.currentUserId) {
        this.submissions = []
        return
      }
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/wifi-model-submissions/${this.currentUserId}/`)
        this.submissions = res.data || []
      } catch (error) {
        console.error('加载提交记录失败:', error)
        this.submissions = []
      }
    },
    async loadUserData() {
      if (this.currentUserId) {
        try {
          // 同时获取用户评价和收藏列表
          const [reviewsResponse, favoritesResponse] = await Promise.all([
            axios.get(`http://127.0.0.1:8000/api/user-reviews/${this.currentUserId}/`),
            axios.get(`http://127.0.0.1:8000/api/favorites/${this.currentUserId}/`)
          ])
          
          // 兼容后端蛇形字段，映射到前端模板使用的字段名
          this.userReviews = (reviewsResponse.data || []).map(r => ({
            id: r.id,
            wifiModelName: r.wifi_model_name || `WiFi #${r.wifi_model_id}`,
            rating: r.rating,
            comment: r.comment,
            createdAt: r.date
          }))
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
.avatar-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  background: #f1f3f5;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-fallback {
  font-size: 2.2rem;
  color: #6c757d;
}

/* 确保两个卡片高度一致 */
.dashboard-cards-row > div {
  display: flex;
}

.dashboard-cards-row .card {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.dashboard-cards-row .card-header {
  flex-shrink: 0;
}

/* 固定个人信息卡片的高度 */
.profile-card {
  height: 450px;
  max-height: 450px;
}

.reviews-card {
  height: 450px;
  max-height: 450px;
}

.dashboard-cards-row .card-body {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

/* 收藏的WiFi热点卡片 */
.favorites-card {
  height: 450px;
  max-height: 450px;
  display: flex;
  flex-direction: column;
}

.favorites-card .card-header {
  flex-shrink: 0;
}

.favorites-container {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.favorites-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.favorites-scroll {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 10px;
  min-height: 0;
}

/* 我提交的 Wi-Fi 型号卡片 */
.submissions-card {
  height: 450px;
  max-height: 450px;
  display: flex;
  flex-direction: column;
}

.submissions-card .card-header {
  flex-shrink: 0;
}

.submissions-container {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.submissions-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.submissions-scroll {
  flex: 1;
  overflow-y: auto;
  overflow-x: auto;
  padding-right: 10px;
  min-height: 0;
}

.submissions-scroll .table-responsive {
  overflow: visible;
}

/* 我的评价卡片的内容区域 */
.reviews-container {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  min-height: 0;
  overflow: hidden;
}

.reviews-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.reviews-scroll {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 10px;
  min-height: 0;
}

/* 自定义滚动条样式（可选，让滚动条更美观） */
.reviews-scroll::-webkit-scrollbar,
.favorites-scroll::-webkit-scrollbar,
.submissions-scroll::-webkit-scrollbar {
  width: 8px;
}

.reviews-scroll::-webkit-scrollbar-track,
.favorites-scroll::-webkit-scrollbar-track,
.submissions-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.reviews-scroll::-webkit-scrollbar-thumb,
.favorites-scroll::-webkit-scrollbar-thumb,
.submissions-scroll::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.reviews-scroll::-webkit-scrollbar-thumb:hover,
.favorites-scroll::-webkit-scrollbar-thumb:hover,
.submissions-scroll::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.review-item {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.review-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

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
  margin-bottom: 0.5rem;
}

.date {
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 0;
}
</style>