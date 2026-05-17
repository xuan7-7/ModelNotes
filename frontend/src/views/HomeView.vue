<script setup>
import { useRouter } from 'vue-router'
import { Right } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<template>
  <div class="home-page">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">ModelNotes</h1>
        <p class="hero-subtitle">AI 驱动的知识库管理平台</p>
        <p class="hero-desc">
          将你的文档一键转化为结构化、可交互的知识笔记与思维导图。
          让知识整理不再枯燥，让学习效率翻倍。
        </p>
        <el-button
          type="primary"
          size="large"
          :icon="Right"
          @click="router.push('/create')"
        >
          开始创建
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  min-height: calc(100vh - 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8edf5 100%);
}

.hero-section {
  text-align: center;
  max-width: 640px;
  padding: 48px 24px;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 12px;
  letter-spacing: -1px;
}

.hero-subtitle {
  font-size: 20px;
  color: #409eff;
  margin-bottom: 24px;
  font-weight: 500;
}

.hero-desc {
  font-size: 15px;
  color: #606266;
  line-height: 1.8;
  margin-bottom: 36px;
}
</style>
