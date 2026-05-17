<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Edit } from '@element-plus/icons-vue'
import { getDocument } from '@/api/document'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()

const doc = ref(null)
const loading = ref(true)
const activeTab = ref('notes')

const docId = computed(() => Number(route.params.id))

const renderedContent = computed(() => {
  if (!doc.value?.content) return ''
  return marked(doc.value.content)
})

const renderedAiNotes = computed(() => {
  if (!doc.value?.ai_notes) return ''
  return marked(doc.value.ai_notes)
})

function goBack() {
  router.push('/knowledge')
}

onMounted(async () => {
  try {
    const { data } = await getDocument(docId.value)
    doc.value = data
  } catch {
    doc.value = null
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <!-- 加载中 -->
  <div class="detail-page" v-if="loading">
    <el-skeleton :rows="5" animated style="padding:40px" />
  </div>

  <!-- 文档详情 -->
  <div class="detail-page" v-else-if="doc">
    <div class="detail-header">
      <el-button text :icon="ArrowLeft" @click="goBack">返回知识库</el-button>
      <el-button type="primary" size="small" :icon="Edit" @click="router.push(`/create?edit=${doc.id}`)">编辑</el-button>
      <span class="detail-title">{{ doc.title }}</span>
      <div class="detail-tags">
        <el-tag
          v-for="tag in (doc.tags || '').split(',').filter(Boolean)"
          :key="tag"
          size="small"
        >{{ tag }}</el-tag>
      </div>
    </div>

    <div class="detail-body">
      <div class="panel panel-left">
        <div class="panel-header">Markdown 原文</div>
        <div class="panel-content markdown-body" v-html="renderedContent"></div>
      </div>

      <div class="panel panel-right">
        <div class="panel-header">
          <el-radio-group v-model="activeTab" size="small">
            <el-radio-button value="notes">知识笔记</el-radio-button>
            <el-radio-button value="mindmap">思维导图</el-radio-button>
          </el-radio-group>
        </div>
        <div class="panel-content" v-show="activeTab === 'notes'">
          <div v-if="doc.ai_notes" class="markdown-body" v-html="renderedAiNotes"></div>
          <el-empty v-else description="尚未 AI 转化" :image-size="80">
            <el-button type="primary" @click="router.push('/create')">去转化</el-button>
          </el-empty>
        </div>
        <div class="panel-content" v-show="activeTab === 'mindmap'">
          <pre v-if="doc.ai_mindmap" class="mindmap-code">{{ doc.ai_mindmap }}</pre>
          <el-empty v-else description="暂无思维导图" :image-size="80" />
        </div>
      </div>
    </div>
  </div>

  <!-- 文档不存在 -->
  <div class="detail-page" v-else>
    <el-empty description="文档不存在">
      <el-button type="primary" @click="goBack">返回知识库</el-button>
    </el-empty>
  </div>
</template>

<style scoped>
.detail-page {
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 24px;
  border-bottom: 1px solid #e4e7ed;
  background: #fff;
}

.detail-title {
  font-size: 17px;
  font-weight: 600;
  color: #1a1a2e;
}

.detail-tags {
  display: flex;
  gap: 4px;
}

.detail-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-left {
  border-right: 1px solid #e4e7ed;
}

.panel-header {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 600;
  color: #606266;
  border-bottom: 1px solid #ebeef5;
  background: #fafafa;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.markdown-body :deep(h1) { font-size: 22px; margin: 16px 0 10px; }
.markdown-body :deep(h2) { font-size: 18px; margin: 14px 0 8px; color: #409eff; }
.markdown-body :deep(h3) { font-size: 15px; margin: 12px 0 6px; }
.markdown-body :deep(p) { line-height: 1.8; margin: 8px 0; color: #303133; }
.markdown-body :deep(strong) { color: #1a1a2e; }
.markdown-body :deep(ul), .markdown-body :deep(ol) { padding-left: 20px; }
.markdown-body :deep(li) { line-height: 1.8; }
.markdown-body :deep(code) { background: #f0f2f5; padding: 2px 6px; border-radius: 3px; font-size: 13px; }
.markdown-body :deep(pre) { background: #f5f7fa; padding: 16px; border-radius: 6px; overflow-x: auto; }

.mindmap-code {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 6px;
  font-size: 13px;
  color: #606266;
  white-space: pre-wrap;
}
</style>
