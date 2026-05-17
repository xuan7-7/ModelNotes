<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const navItems = [
  { path: '/', label: '首页' },
  { path: '/knowledge', label: '知识库' },
  { path: '/create', label: '创建/转化' },
  { path: '/mine', label: '我的' },
]

const activeIndex = computed(() => route.path)

function handleSelect(path) {
  router.push(path)
  // "AI 转化" 跳转到创建页后自动聚焦输入框，待 CreateView 实现后补充
}
</script>

<template>
  <el-header class="app-header">
    <div class="header-left">
      <span class="header-logo">🧠</span>
      <span class="header-name">ModelNotes</span>
    </div>

    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
      class="header-nav"
    >
      <el-menu-item v-for="item in navItems" :key="item.label" :index="item.path">
        {{ item.label }}
      </el-menu-item>
    </el-menu>

    <div class="header-right">
      <el-button text @click="router.push('/help')">帮助与反馈</el-button>
    </div>
  </el-header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
  border-bottom: 1px solid #e4e7ed;
  background: #fff;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  color: #1a1a2e;
  white-space: nowrap;
}

.header-logo {
  font-size: 24px;
}

.header-nav {
  flex: 1;
  display: flex;
  justify-content: center;
  border-bottom: none !important;
}

.header-nav .el-menu-item {
  border-bottom: none;
}

.header-right {
  white-space: nowrap;
}
</style>
