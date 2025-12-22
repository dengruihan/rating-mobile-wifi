<template>
  <div class="container">
    <div class="d-flex align-items-center mb-4">
      <button class="btn btn-outline-secondary me-3" @click="goBack" title="返回">
        <i class="bi bi-arrow-left"></i> 返回
      </button>
      <h2 class="mb-0">提交新 WiFi 型号</h2>
    </div>

    <div v-if="!loggedIn" class="alert alert-warning">
      需要登录后才能提交新型号。
      <router-link to="/login" class="alert-link">去登录</router-link>
    </div>

    <form v-else @submit.prevent="submit" class="card p-4">
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">名称</label>
          <input v-model="form.name" class="form-control" required placeholder="例如：华为随行WiFi 3" />
        </div>
        <div class="col-md-3">
          <label class="form-label">品牌</label>
          <input v-model="form.brand" class="form-control" required placeholder="例如：华为" />
        </div>
        <div class="col-md-3">
          <label class="form-label">型号</label>
          <input v-model="form.model" class="form-control" required placeholder="例如：E5576-855" />
        </div>

        <div class="col-md-4">
          <label class="form-label">信号强度（0-5）</label>
          <input v-model.number="form.signalStrength" type="number" step="0.1" min="0" max="5" class="form-control" required />
        </div>
        <div class="col-md-4">
          <label class="form-label">速度（0-5）</label>
          <input v-model.number="form.speed" type="number" step="0.1" min="0" max="5" class="form-control" required />
        </div>
        <div class="col-md-4">
          <label class="form-label">设备价格（元）</label>
          <input v-model.number="form.price" type="number" step="0.01" min="0" class="form-control" required />
        </div>

        <div class="col-12">
          <label class="form-label">描述</label>
          <textarea v-model="form.description" class="form-control" rows="3" placeholder="补充说明（可选）"></textarea>
        </div>
      </div>

      <hr class="my-4" />

      <div class="d-flex justify-content-between align-items-center mb-2">
        <h5 class="mb-0">资费套餐</h5>
        <button type="button" class="btn btn-sm btn-outline-primary" @click="addPlan">
          添加套餐
        </button>
      </div>

      <div v-if="form.dataPlans.length === 0" class="text-muted mb-3">
        暂无套餐（可以不填，但建议至少添加 1 个）。
      </div>

      <div v-for="(plan, idx) in form.dataPlans" :key="idx" class="row g-2 align-items-end mb-2">
        <div class="col-md-8">
          <label class="form-label">套餐名称</label>
          <input v-model="plan.name" class="form-control" placeholder="例如：月包10GB" />
        </div>
        <div class="col-md-3">
          <label class="form-label">价格（元）</label>
          <input v-model.number="plan.price" type="number" step="0.01" min="0" class="form-control" />
        </div>
        <div class="col-md-1 d-grid">
          <button type="button" class="btn btn-outline-danger" @click="removePlan(idx)" title="删除">
            ×
          </button>
        </div>
      </div>

      <div class="d-flex gap-2 mt-4">
        <button class="btn btn-primary" type="submit" :disabled="submitting">
          {{ submitting ? '提交中...' : '提交审核' }}
        </button>
      </div>

      <div v-if="lastResult" class="alert alert-info mt-3 mb-0">
        已提交，当前状态：<strong>{{ statusLabel(lastResult.approval_status) }}</strong>。
        管理员通过后将会出现在首页列表。
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SubmitWifiModel',
  inject: ['isLoggedIn', 'currentUser'],
  data() {
    return {
      submitting: false,
      lastResult: null,
      form: {
        name: '',
        brand: '',
        model: '',
        signalStrength: 4.0,
        speed: 4.0,
        price: 199,
        description: '',
        dataPlans: []
      }
    }
  },
  computed: {
    loggedIn() {
      return typeof this.isLoggedIn === 'object' && this.isLoggedIn !== null && 'value' in this.isLoggedIn
        ? this.isLoggedIn.value
        : !!this.isLoggedIn
    },
    currentUserId() {
      if (typeof this.currentUser === 'object' && this.currentUser !== null && 'value' in this.currentUser) {
        return this.currentUser.value?.id
      }
      return this.currentUser?.id
    }
  },
  mounted() {
    // 页面加载时滚动到顶部
    window.scrollTo(0, 0)
  },
  methods: {
    goBack() {
      // 如果浏览器历史记录中有上一页，则返回上一页，否则返回首页
      if (window.history.length > 1) {
        this.$router.go(-1)
      } else {
        this.$router.push('/')
      }
    },
    addPlan() {
      this.form.dataPlans.push({ name: '', price: 0 })
    },
    removePlan(idx) {
      this.form.dataPlans.splice(idx, 1)
    },
    statusLabel(status) {
      if (status === 'approved') return '已通过'
      if (status === 'rejected') return '已驳回'
      return '待审核'
    },
    async submit() {
      if (!this.loggedIn || !this.currentUserId) {
        this.$router.push('/login')
        return
      }

      // 过滤掉空套餐
      const dataPlans = (this.form.dataPlans || [])
        .filter(p => p && p.name && p.price !== null && p.price !== undefined)
        .map(p => ({ name: p.name, price: p.price }))

      this.submitting = true
      try {
        const payload = {
          userId: this.currentUserId,
          name: this.form.name,
          brand: this.form.brand,
          model: this.form.model,
          signalStrength: this.form.signalStrength,
          speed: this.form.speed,
          price: this.form.price,
          description: this.form.description,
          dataPlans
        }
        const res = await axios.post('http://127.0.0.1:8000/api/wifi-model-submissions/', payload)
        this.lastResult = res.data
        alert('提交成功，等待管理员审核！')
      } catch (e) {
        console.error('提交新型号失败:', e)
        console.error('错误详情:', e.response ? e.response.data : e.message)
        alert('提交失败，请检查网络连接或输入内容')
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>


