<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDocumentsStore } from '@/stores/documents'

const store = useDocumentsStore()

// --- 当前选中的月份 ---
const now = new Date()
const selectedMonth = ref(`${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`)

const monthOptions = [
  '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06',
  '2026-07', '2026-08', '2026-09', '2026-10', '2026-11', '2026-12',
]

// --- 按日期统计文档数 ---
const dateCountMap = computed(() => {
  const map = {}
  store.documents.forEach((doc) => {
    const d = doc.created_at?.slice(0, 10)
    map[d] = (map[d] || 0) + 1
  })
  return map
})

// --- 热力图数据 ---
const weekHeaders = ['一', '二', '三', '四', '五', '六', '日']

const heatmapCells = computed(() => {
  const [year, month] = selectedMonth.value.split('-').map(Number)
  const firstDay = new Date(year, month - 1, 1).getDay() // 0=周日
  // 转为周一=0
  const startOffset = firstDay === 0 ? 6 : firstDay - 1
  const daysInMonth = new Date(year, month, 0).getDate()

  const cells = []
  // 前置空白格
  for (let i = 0; i < startOffset; i++) {
    cells.push({ date: '', count: 0, empty: true })
  }
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`
    cells.push({
      date: dateStr,
      count: dateCountMap.value[dateStr] || 0,
      empty: false,
    })
  }
  return cells
})

// --- 颜色映射 ---
function heatColor(count) {
  if (count === 0) return '#e8e8e8'
  if (count === 1) return '#a0d2f0'
  if (count === 2) return '#f0be70'
  return '#e08840'
}

// --- 点击格子弹窗 ---
const dialogVisible = ref(false)
const dialogDate = ref('')
const dialogDocs = computed(() =>
  store.documents.filter((d) => (d.created_at || '').slice(0, 10) === dialogDate.value),
)

function openDialog(date) {
  dialogDate.value = date
  dialogVisible.value = true
}

// --- 统计指标 ---
const stats = computed(() => {
  const today = now.toISOString().slice(0, 10)
  const thisMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`

  // 总知识资产数
  const totalAssets = store.documents.length

  // 本月 AI 转化次数
  const monthDocs = store.documents.filter((d) => (d.created_at || '').startsWith(thisMonth))
  const monthAiCount = monthDocs.filter((d) => d.ai_notes).length

  // 连续打卡天数：从今天往前数，有 count > 0 的连续天数
  let streak = 0
  const check = new Date(now)
  while (true) {
    const ds = check.toISOString().slice(0, 10)
    if (dateCountMap.value[ds] && dateCountMap.value[ds] > 0) {
      streak++
      check.setDate(check.getDate() - 1)
    } else {
      break
    }
  }

  // 被关联引用次数（暂 mock）
  const refCount = 0

  return { totalAssets, monthAiCount, streak, refCount }
})

onMounted(() => {
  store.fetchDocuments()
})
</script>

<template>
  <div class="mine-page">
    <!-- 统计仪表盘 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-num">{{ stats.streak }}</div>
        <div class="stat-label">连续打卡天数</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ stats.totalAssets }}</div>
        <div class="stat-label">总知识资产数</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ stats.monthAiCount }}</div>
        <div class="stat-label">本月 AI 转化</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ stats.refCount }}</div>
        <div class="stat-label">关联引用次数</div>
      </div>
    </div>

    <!-- 热力图 -->
    <div class="heatmap-section">
      <div class="heatmap-header">
        <span class="heatmap-title">每日记录热力图</span>
        <el-select v-model="selectedMonth" size="small" style="width:140px">
          <el-option v-for="m in monthOptions" :key="m" :label="m" :value="m" />
        </el-select>
      </div>

      <div class="heatmap-grid">
        <!-- 星期头 -->
        <div class="heatmap-weekday" v-for="w in weekHeaders" :key="w">{{ w }}</div>
        <!-- 格子 -->
        <template v-for="cell in heatmapCells" :key="cell.date || cell.empty">
          <div v-if="cell.empty" class="heatmap-cell empty"></div>
          <el-tooltip
            v-else
            :content="`${cell.date} — ${cell.count} 篇`"
            placement="top"
            :show-after="200"
          >
            <div
              class="heatmap-cell"
              :style="{ background: heatColor(cell.count) }"
              @click="cell.count > 0 && openDialog(cell.date)"
            >
              <span class="cell-num">{{ cell.date.slice(-2).replace(/^0/, '') }}</span>
            </div>
          </el-tooltip>
        </template>
      </div>

      <!-- 图例 -->
      <div class="heatmap-legend">
        <span class="legend-label">少</span>
        <span class="legend-block" style="background:#e8e8e8"></span>
        <span class="legend-block" style="background:#a0d2f0"></span>
        <span class="legend-block" style="background:#f0be70"></span>
        <span class="legend-block" style="background:#e08840"></span>
        <span class="legend-label">多</span>
      </div>
    </div>

    <!-- 弹窗：当天文件列表 -->
    <el-dialog v-model="dialogVisible" :title="`${dialogDate} 记录`" width="480px">
      <el-table :data="dialogDocs" stripe size="small" v-if="dialogDocs.length">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="createdAt" label="日期" width="110" />
        <el-table-column width="80">
          <template #default="{ row }">
            <el-tag v-if="row.ai_notes" size="small" type="success">已转化</el-tag>
            <el-tag v-else size="small" type="info">未转化</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无记录" />
    </el-dialog>
  </div>
</template>

<style scoped>
.mine-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 28px 24px;
  min-height: calc(100vh - 60px);
}

/* 统计卡片 */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}

.stat-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.stat-num {
  font-size: 30px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

/* 热力图 */
.heatmap-section {
  background: #fff;
  border-radius: 10px;
  padding: 20px 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.heatmap-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.heatmap-weekday {
  text-align: center;
  font-size: 12px;
  color: #909399;
  padding-bottom: 4px;
}

.heatmap-cell {
  aspect-ratio: 1;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
}

.heatmap-cell:not(.empty) {
  cursor: pointer;
}

.heatmap-cell:not(.empty):hover {
  outline: 2px solid #409eff;
  outline-offset: -1px;
}

.heatmap-cell.empty {
  background: transparent;
}

.cell-num {
  font-size: 11px;
  color: rgba(0, 0, 0, 0.35);
  font-weight: 500;
}

/* 图例 */
.heatmap-legend {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 5px;
  margin-top: 12px;
}

.legend-label {
  font-size: 11px;
  color: #909399;
}

.legend-block {
  width: 14px;
  height: 14px;
  border-radius: 3px;
}
</style>
