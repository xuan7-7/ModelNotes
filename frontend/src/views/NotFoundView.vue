<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const links = [
  { path: '/', label: '首页' },
  { path: '/knowledge', label: '知识库' },
  { path: '/create', label: '创建/转化' },
  { path: '/mine', label: '我的' },
  { path: '/help', label: '帮助与反馈' },
]
</script>

<template>
  <div class="not-found">
    <h1 class="code">404</h1>
    <p class="msg">你访问的页面不存在</p>
    <div class="links">
      <el-button
        v-for="link in links"
        :key="link.path"
        text
        type="primary"
        @click="router.push(link.path)"
      >
        {{ link.label }}
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
}

.code {
  font-size: 80px;
  font-weight: 800;
  color: #dcdfe6;
  margin: 0;
  letter-spacing: 4px;
}

.msg {
  font-size: 16px;
  color: #909399;
  margin: 12px 0 28px;
}

.links {
  display: flex;
  gap: 8px;
}
</style>
