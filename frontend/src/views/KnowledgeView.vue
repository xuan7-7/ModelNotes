<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Grid, List, Upload, Checked, Delete, Share, Close, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useDocumentsStore } from '@/stores/documents'
import { batchDeleteDocuments } from '@/api/document'

const router = useRouter()
const store = useDocumentsStore()
const viewMode = ref('grid')
const searchKeyword = ref('')

function onSearch() {
  store.fetchDocuments(searchKeyword.value ? { search: searchKeyword.value } : {})
}

function onClearSearch() {
  searchKeyword.value = ''
  store.fetchDocuments()
}

// 多选模式
const selectMode = ref(false)
const selectedIds = ref(new Set())

const isEmpty = computed(() => !store.loading && store.documents.length === 0)

const isAllSelected = computed(
  () => store.documents.length > 0 && selectedIds.value.size === store.documents.length,
)

onMounted(() => {
  store.fetchDocuments()
})

function goDetail(id) {
  if (selectMode.value) return
  router.push(`/knowledge/${id}`)
}

function goCreate() {
  router.push('/create')
}

// 切换选择
function toggleSelect(id) {
  const s = new Set(selectedIds.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  selectedIds.value = s
}

function toggleSelectAll() {
  if (isAllSelected.value) {
    selectedIds.value = new Set()
  } else {
    selectedIds.value = new Set(store.documents.map((d) => d.id))
  }
}

function enterSelectMode() {
  selectMode.value = true
  selectedIds.value = new Set()
}

function exitSelectMode() {
  selectMode.value = false
  selectedIds.value = new Set()
}

// 批量删除
async function handleBatchDelete() {
  if (!selectedIds.value.size) {
    ElMessage.warning('请先选择文档')
    return
  }
  try {
    await ElMessageBox.confirm(
      `确定删除选中的 ${selectedIds.value.size} 篇文档？删除后不可恢复。`,
      '确认删除',
      { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' },
    )
    const ids = [...selectedIds.value]
    await batchDeleteDocuments(ids)
    await store.fetchDocuments()
    ElMessage.success(`已删除 ${ids.length} 篇文档`)
    exitSelectMode()
  } catch { /* 取消 */ }
}

// 批量分享（合并为 Markdown 复制到剪贴板）
async function handleBatchShare() {
  if (!selectedIds.value.size) {
    ElMessage.warning('请先选择文档')
    return
  }
  const docs = store.documents.filter((d) => selectedIds.value.has(d.id))
  const text = docs
    .map((d) => {
      const tags = (d.tags || '').split(',').filter(Boolean).map((t) => `#${t}`).join(' ')
      return `# ${d.title}\n\n> ${d.created_at?.slice(0, 10)}  ${tags}\n\n${d.content || ''}\n\n---\n`
    })
    .join('\n')

  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success(`已复制 ${docs.length} 篇文档到剪贴板`)
    exitSelectMode()
  } catch {
    ElMessage.error('复制失败，请手动复制')
  }
}
</script>

<template>
  <div class="knowledge-page">
    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <span v-if="!selectMode" class="doc-count">共 {{ store.documents.length }} 篇笔记</span>
        <el-input
          v-if="!selectMode && !isEmpty"
          v-model="searchKeyword"
          placeholder="搜索标题或标签..."
          :prefix-icon="Search"
          clearable
          size="small"
          style="padding-left:15px; width:220px"
          @keyup.enter="onSearch"
          @clear="onClearSearch"
        />
        <el-checkbox
          v-if="selectMode"
          :model-value="isAllSelected"
          :indeterminate="selectedIds.size > 0 && !isAllSelected"
          @change="toggleSelectAll"
        >
          全选（{{ selectedIds.size }}/{{ store.documents.length }}）
        </el-checkbox>
      </div>
      <div class="toolbar-right">
        <template v-if="!selectMode && !isEmpty">
          <el-button text size="small" :icon="Checked" @click="enterSelectMode">多选</el-button>
          <el-radio-group v-model="viewMode" size="small">
            <el-radio-button value="grid"><el-icon><Grid /></el-icon>&nbsp;宫格</el-radio-button>
            <el-radio-button value="list"><el-icon><List /></el-icon>&nbsp;列表</el-radio-button>
          </el-radio-group>
        </template>
        <template v-if="selectMode">
          <el-button size="small" type="danger" :icon="Delete" @click="handleBatchDelete">删除</el-button>
          <el-button size="small" type="primary" :icon="Share" @click="handleBatchShare">分享</el-button>
          <el-button size="small" text :icon="Close" @click="exitSelectMode">取消</el-button>
        </template>
      </div>
    </div>

    <!-- 加载中 -->
    <div class="loading-area" v-if="store.loading">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- 空状态 -->
    <div class="empty-area" v-else-if="isEmpty">
      <el-empty description="还没有笔记，开始你的第一篇吧">
        <el-button type="primary" @click="goCreate"><el-icon><Plus /></el-icon>创建第一篇笔记</el-button>
        <el-button @click="goCreate"><el-icon><Upload /></el-icon>上传文档试试</el-button>
      </el-empty>
    </div>

    <!-- 宫格视图 -->
    <div class="grid-view" v-else-if="viewMode === 'grid'">
      <el-card
        v-for="doc in store.documents"
        :key="doc.id"
        class="doc-card"
        :class="{ selected: selectedIds.has(doc.id) }"
        shadow="hover"
        @click="selectMode ? toggleSelect(doc.id) : goDetail(doc.id)"
      >
        <el-checkbox
          v-if="selectMode"
          :model-value="selectedIds.has(doc.id)"
          class="card-check"
          @click.stop
          @change="toggleSelect(doc.id)"
        />
        <div class="card-title">{{ doc.title }}</div>
        <div class="card-tags">
          <el-tag
            v-for="tag in (doc.tags || '').split(',').filter(Boolean)"
            :key="tag"
            size="small"
            class="tag-item"
          >{{ tag }}</el-tag>
          <el-tag v-if="!(doc.tags || '').split(',').filter(Boolean).length" size="small" type="info">无标签</el-tag>
        </div>
        <div class="card-footer">
          <span class="card-date">{{ doc.created_at?.slice(0, 10) }}</span>
          <el-tag v-if="doc.ai_notes" size="small" type="success" effect="plain">已AI转化</el-tag>
        </div>
      </el-card>
    </div>

    <!-- 列表视图 -->
    <div class="list-view" v-else>
      <div
        v-for="doc in store.documents"
        :key="doc.id"
        class="doc-row"
        :class="{ selected: selectedIds.has(doc.id) }"
        @click="selectMode ? toggleSelect(doc.id) : goDetail(doc.id)"
      >
        <el-checkbox
          v-if="selectMode"
          :model-value="selectedIds.has(doc.id)"
          @click.stop
          @change="toggleSelect(doc.id)"
        />
        <div class="row-title">{{ doc.title }}</div>
        <div class="row-tags">
          <el-tag v-for="tag in (doc.tags || '').split(',').filter(Boolean)" :key="tag" size="small">{{ tag }}</el-tag>
        </div>
        <div class="row-date">{{ doc.created_at?.slice(0, 10) }}</div>
        <el-tag v-if="doc.ai_notes" size="small" type="success" effect="plain">已转化</el-tag>
      </div>
    </div>
  </div>
</template>

<style scoped>
.knowledge-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
  min-height: calc(100vh - 60px);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.doc-count {
  color: #909399;
  font-size: 14px;
}

.loading-area,
.empty-area {
  margin-top: 80px;
}

/* 宫格 */
.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.doc-card {
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  position: relative;
}

.doc-card:hover {
  transform: translateY(-2px);
}

.doc-card.selected {
  box-shadow: 0 0 0 2px #409eff;
}

.card-check {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-tags {
  margin-bottom: 12px;
  min-height: 24px;
}

.tag-item {
  margin-right: 4px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-date {
  font-size: 12px;
  color: #c0c4cc;
}

/* 列表 */
.list-view {
  background: #fff;
  border-radius: 8px;
}

.doc-row {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.15s;
  gap: 16px;
}

.doc-row:hover {
  background: #f5f7fa;
}

.doc-row:last-child {
  border-bottom: none;
}

.doc-row.selected {
  background: #ecf5ff;
}

.row-title {
  flex: 1;
  font-size: 15px;
  font-weight: 500;
  color: #1a1a2e;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-tags {
  display: flex;
  gap: 4px;
  min-width: 120px;
}

.row-date {
  font-size: 13px;
  color: #c0c4cc;
  min-width: 90px;
  text-align: right;
}
</style>
