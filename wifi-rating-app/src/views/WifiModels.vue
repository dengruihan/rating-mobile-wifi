<template>
  <div class="container">
    <h2>移动WiFi型号列表</h2>
    
    <div class="filter-section mb-4">
      <div class="row">
        <div class="col-md-4">
          <select v-model="filterBrand" class="form-select">
            <option value="">全部品牌</option>
            <option value="华为">华为</option>
            <option value="小米">小米</option>
            <option value="腾讯">腾讯</option>
            <option value="中兴">中兴</option>
            <option value="TP-Link">TP-Link</option>
          </select>
        </div>
        <div class="col-md-4">
          <select v-model="sortBy" class="form-select">
            <option value="rating">按评分排序</option>
            <option value="price">按价格排序</option>
            <option value="speed">按速度排序</option>
            <option value="signalStrength">按信号强度排序</option>
          </select>
        </div>
        <div class="col-md-4">
          <select v-model="sortOrder" class="form-select">
            <option value="desc">降序</option>
            <option value="asc">升序</option>
          </select>
        </div>
      </div>
    </div>
    
    <div class="row">
      <div class="col-md-4" v-for="wifi in filteredAndSortedWifis" :key="wifi.id">
        <div class="card mb-4 card-hover">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title mb-0">{{ wifi.name }}</h5>
              <span class="badge bg-primary rounded-pill">
                {{ wifi.brand }}
              </span>
            </div>
            <h6 class="card-subtitle mb-3 text-muted">{{ wifi.model }}</h6>
            <div class="info mb-4">
              <div class="row g-2">
                <div class="col-6">
                  <div class="progress" style="height: 6px; margin-bottom: 5px;">
                    <div class="progress-bar bg-success" role="progressbar" :style="{ width: (wifi.signalStrength * 20) + '%' }"></div>
                  </div>
                  <p class="mb-1 small"><strong>信号强度：</strong>{{ wifi.signalStrength }}/5</p>
                </div>
                <div class="col-6">
                  <div class="progress" style="height: 6px; margin-bottom: 5px;">
                    <div class="progress-bar bg-info" role="progressbar" :style="{ width: (wifi.speed * 20) + '%' }"></div>
                  </div>
                  <p class="mb-1 small"><strong>速度：</strong>{{ wifi.speed }}/5</p>
                </div>
              </div>
              <div class="row g-2 mt-2">
                <div class="col-6">
                  <p class="mb-1 small"><strong>价格：</strong><span class="text-primary fw-bold">¥{{ wifi.price }}</span></p>
                </div>
                <div class="col-6">
                  <p class="mb-1 small"><strong>评价数：</strong>{{ wifi.reviewCount }}</p>
                </div>
              </div>
            </div>
            <div class="rating mb-3">
              <span class="star" v-for="n in 5" :key="n">
                {{ n <= wifi.rating ? '★' : '☆' }}
              </span>
              <span class="rating-value">{{ wifi.rating }}</span>
            </div>
            <router-link :to="'/wifi-model/' + wifi.id" class="btn btn-primary w-100">查看详情</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import wifiModelsData from '../assets/data/wifiModels.json'

export default {
  name: 'WifiModels',
  data() {
    return {
      wifiModels: wifiModelsData,
      filterBrand: '',
      sortBy: 'rating',
      sortOrder: 'desc'
    }
  },
  computed: {
    filteredAndSortedWifis() {
      let result = [...this.wifiModels]
      
      // 筛选
      if (this.filterBrand) {
        result = result.filter(wifi => wifi.brand === this.filterBrand)
      }
      
      // 排序
      result.sort((a, b) => {
        if (this.sortOrder === 'asc') {
          return a[this.sortBy] - b[this.sortBy]
        } else {
          return b[this.sortBy] - a[this.sortBy]
        }
      })
      
      return result
    }
  }
}
</script>

<style scoped>
.info {
  margin: 10px 0;
  font-size: 0.9rem;
}

.rating {
  color: #ffc107;
  font-size: 1.1rem;
  margin: 15px 0;
  display: flex;
  align-items: center;
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