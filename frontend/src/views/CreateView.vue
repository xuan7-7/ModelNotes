<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Upload, MagicStick, DocumentAdd, Loading } from '@element-plus/icons-vue'
import { useDocumentsStore } from '@/stores/documents'
import { getDocument, updateDocument, aiTransform } from '@/api/document'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const store = useDocumentsStore()

// --- 编辑模式 ---
const editId = ref(null)
const isEdit = computed(() => !!editId.value)

// --- 表单数据 ---
const title = ref('')
const tagInput = ref('')
const content = ref('')
const editorRef = ref(null)

const tags = computed(() =>
  tagInput.value
    .split(/[,，]/)
    .map((t) => t.trim())
    .filter(Boolean)
    .slice(0, 3),
)

// --- 实时预览 ---
const previewHtml = computed(() => {
  if (!content.value) return '<p style="color:#c0c4cc">输入 Markdown 内容，此处实时预览</p>'
  return marked(content.value)
})

// --- 保存 ---
const saving = ref(false)
async function handleSave() {
  if (!title.value.trim() || !content.value.trim()) {
    ElMessage.warning('请填写标题和内容')
    return
  }
  saving.value = true
  const payload = {
    title: title.value.trim(),
    content: content.value,
    tags: tags.value.join(','),
    ai_notes: aiNotes.value || null,
    ai_mindmap: aiMindmap.value || null,
  }
  if (isEdit.value) {
    await updateDocument(editId.value, payload)
    ElMessage.success('更新成功')
  } else {
    await store.addDocument({ ...payload, tags: tags.value })
    ElMessage.success('保存成功')
  }
  saving.value = false
  router.push(`/knowledge/${editId.value || store.documents[0]?.id}`)
}

// --- 上传 .md ---
const uploadRef = ref(null)
function handleUpload() {
  uploadRef.value?.click()
}
function onFileChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => {
    const text = ev.target?.result || ''
    content.value = text.slice(0, 50000)
    if (text.length > 50000) {
      ElMessage.warning('文件过长，已截取前 50000 字')
    } else {
      ElMessage.success('文件加载成功')
    }
    if (!title.value) {
      title.value = file.name.replace(/\.md$/i, '')
    }
  }
  reader.readAsText(file)
  // 重置 input，允许重复上传同一文件
  e.target.value = ''
}

// --- AI 转化 ---
const transforming = ref(false)
const aiNotes = ref('')
const aiMindmap = ref('')
const resultTab = ref('notes')

async function handleTransform() {
  if (!content.value.trim()) {
    ElMessage.warning('请先输入文档内容')
    return
  }
  transforming.value = true
  aiNotes.value = ''
  aiMindmap.value = ''

  try {
    const { data } = await aiTransform(content.value)
    aiNotes.value = data.notes
    aiMindmap.value = data.mindmap
    ElMessage.success('AI 转化完成')
  } catch (e) {
    ElMessage.error('AI 转化失败：' + (e.response?.data?.detail || e.message))
  } finally {
    transforming.value = false
  }
}

// --- 加载编辑文档 & 自动聚焦 ---
onMounted(async () => {
  const eid = route.query.edit
  if (eid) {
    editId.value = Number(eid)
    try {
      const { data } = await getDocument(editId.value)
      title.value = data.title
      tagInput.value = data.tags || ''
      content.value = (data.content || '').slice(0, 50000)
      if (data.ai_notes || data.ai_mindmap) {
        aiNotes.value = data.ai_notes || ''
        aiMindmap.value = data.ai_mindmap || ''
      }
    } catch {
      ElMessage.error('加载文档失败')
      editId.value = null
    }
  }
  await nextTick()
  editorRef.value?.focus()
})

// 监听 content 变化，自动调整 textarea 高度
const textareaStyle = computed(() => ({
  minHeight: '320px',
}))

// 清除转化结果
watch(content, () => {
  if (aiNotes.value || aiMindmap.value) {
    aiNotes.value = ''
    aiMindmap.value = ''
  }
})
</script>

<template>
  <div class="create-page">
    <!-- 页面标题 -->
    <div class="page-title-row">
      <span class="page-title">{{ isEdit ? '编辑笔记' : '新建笔记' }}</span>
      <el-button v-if="isEdit" text size="small" @click="router.push(`/knowledge/${editId}`)">返回详情</el-button>
    </div>

    <!-- 顶部：标题 & 标签 -->
    <div class="form-header">
      <el-input
        v-model="title"
        placeholder="输入笔记标题..."
        class="title-input"
        maxlength="100"
        clearable
      />
      <el-input
        v-model="tagInput"
        placeholder="标签，逗号分隔（如：AI, Python）"
        class="tag-input"
        clearable
      />
      <div class="tag-previews" v-if="tags.length">
        <el-tag v-for="t in tags" :key="t" size="small" class="preview-tag">{{ t }}</el-tag>
      </div>
      <span class="tag-hint" :class="{ full: tags.length >= 3 }">{{ tags.length }}/3 个标签</span>
    </div>

    <!-- 编辑 & 预览 左右分栏 -->
    <div class="editor-area">
      <div class="editor-panel">
        <div class="panel-label">编辑</div>
        <textarea
          ref="editorRef"
          v-model="content"
          class="markdown-editor"
          :style="textareaStyle"
          maxlength="50000"
          placeholder="# 在此编写 Markdown 文档&#10;&#10;或点击底部「上传 .md」导入文件"
        ></textarea>
        <div class="editor-footer">
          <span class="char-count" :class="{ warn: content.length > 45000 }">{{ content.length }} / 50000 字</span>
        </div>
      </div>
      <div class="preview-panel">
        <div class="panel-label">预览</div>
        <div class="markdown-preview" v-html="previewHtml"></div>
      </div>
    </div>

    <!-- 底部工具栏 -->
    <div class="action-bar">
      <input
        ref="uploadRef"
        type="file"
        accept=".md,.txt,.markdown"
        style="display:none"
        @change="onFileChange"
      />
      <el-button :icon="Upload" @click="handleUpload">上传 .md</el-button>
      <el-button
        type="primary"
        :icon="DocumentAdd"
        :loading="saving"
        @click="handleSave"
      >
        保存到知识库
      </el-button>
      <el-button
        type="success"
        :icon="MagicStick"
        :loading="transforming"
        @click="handleTransform"
      >
        AI 转化
      </el-button>
    </div>

    <!-- AI 转化结果区 -->
    <div class="result-area" v-if="aiNotes || aiMindmap || transforming">
      <div class="result-header">
        <span class="result-title">AI 转化结果</span>
        <el-radio-group v-model="resultTab" size="small" v-if="!transforming">
          <el-radio-button value="notes">知识笔记</el-radio-button>
          <el-radio-button value="mindmap">思维导图</el-radio-button>
        </el-radio-group>
      </div>

      <div class="result-body" v-if="transforming">
        <el-icon class="is-loading" :size="24"><Loading /></el-icon>
        <span style="margin-left:8px;color:#909399">AI 正在分析你的文档...</span>
      </div>

      <div class="result-body" v-else-if="resultTab === 'notes'">
        <div class="markdown-body" v-html="marked(aiNotes)"></div>
      </div>

      <div class="result-body" v-else>
        <pre class="mindmap-code">{{ aiMindmap }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.create-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 24px;
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 页面标题 */
.page-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 17px;
  font-weight: 600;
  color: #1a1a2e;
}

/* 顶部表单 */
.form-header {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.title-input {
  width: 320px;
}

.tag-input {
  width: 240px;
}

.tag-previews {
  display: flex;
  gap: 4px;
}

.preview-tag {
  cursor: default;
}

.tag-hint {
  font-size: 12px;
  color: #c0c4cc;
}

.tag-hint.full {
  color: #e6a23c;
  font-weight: 500;
}

/* 编辑 & 预览 */
.editor-area {
  flex: 1;
  display: flex;
  gap: 16px;
  min-height: 0;
}

.editor-panel,
.preview-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.panel-label {
  padding: 8px 14px;
  font-size: 13px;
  color: #909399;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

.markdown-editor {
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  padding: 16px;
  font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.7;
  color: #303133;
  background: #fff;
}

.markdown-editor::placeholder {
  color: #c0c4cc;
  line-height: 2;
}

.editor-footer {
  display: flex;
  justify-content: flex-end;
  padding: 4px 14px;
  background: #fafafa;
  border-top: 1px solid #ebeef5;
}

.char-count {
  font-size: 12px;
  color: #c0c4cc;
}

.char-count.warn {
  color: #e6a23c;
}

.markdown-preview {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: #fff;
}

/* 预览内 Markdown 样式 */
.markdown-preview :deep(h1) { font-size: 22px; margin: 12px 0 8px; }
.markdown-preview :deep(h2) { font-size: 18px; margin: 10px 0 6px; color: #409eff; }
.markdown-preview :deep(h3) { font-size: 15px; margin: 8px 0 4px; }
.markdown-preview :deep(p) { line-height: 1.8; margin: 6px 0; }
.markdown-preview :deep(strong) { color: #1a1a2e; }
.markdown-preview :deep(ul), .markdown-preview :deep(ol) { padding-left: 20px; }
.markdown-preview :deep(li) { line-height: 1.7; }
.markdown-preview :deep(code) { background: #f0f2f5; padding: 2px 6px; border-radius: 3px; font-size: 13px; }
.markdown-preview :deep(pre) { background: #f5f7fa; padding: 14px; border-radius: 6px; overflow-x: auto; }

/* 底部工具栏 */
.action-bar {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding: 4px 0;
}

/* AI 转化结果 */
.result-area {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

.result-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.result-body {
  padding: 20px;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
}

.result-body:has(.markdown-body) {
  display: block;
}

.result-body .markdown-body {
  text-align: left;
  width: 100%;
}

.result-body .markdown-body :deep(h2) { color: #409eff; }
.result-body .markdown-body :deep(strong) { color: #1a1a2e; }
.result-body .markdown-body :deep(ul) { padding-left: 20px; }
.result-body .markdown-body :deep(li) { line-height: 2; }

.mindmap-code {
  background: #f5f7fa;
  padding: 16px 20px;
  border-radius: 6px;
  font-size: 13px;
  color: #606266;
  line-height: 1.8;
  white-space: pre-wrap;
  width: 100%;
}
</style>
