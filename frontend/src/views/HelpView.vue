<script setup>
import { ref, computed } from 'vue'
import { QuestionFilled, DArrowLeft, DArrowRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const collapsed = ref(false)

const faqList = [
  {
    id: 'create',
    title: '如何创建和上传文档？',
    answer:
      '<p><strong>创建文档：</strong>点击顶部导航「创建/转化」，在编辑器中编写 Markdown 内容，填写标题和标签后点击「保存到知识库」即可。</p>' +
      '<p><strong>上传 .md 文件：</strong>在创建页面点击「上传 .md」按钮，选择本地的 Markdown 文件，文件内容会自动填入编辑器，确认后保存。</p>' +
      '<p class="tip">💡 支持中英文逗号分隔多个标签，最多 3 个。</p>',
  },
  {
    id: 'ai',
    title: 'AI 转化功能怎么使用？',
    answer:
      '<p>在创建页面编辑好 Markdown 内容后，点击底部绿色的「AI 转化」按钮，系统会调用 DeepSeek 大模型将你的文档自动整理为：</p>' +
      '<ul><li><strong>知识笔记</strong> — 带层级结构、关键概念加粗高亮的阅读笔记</li>' +
      '<li><strong>思维导图</strong> — 可直接渲染为交互式导图的列表结构</li></ul>' +
      '<p>转化结果会出现在编辑器下方，可在「知识笔记」和「思维导图」之间切换查看。转化完成后保存文档，结果会一并存入知识库。</p>' +
      '<p class="tip">⚠ 需在 <code>backend/.env</code> 中配置 <code>DEEPSEEK_API_KEY</code> 才能使用真实 AI 转化，否则使用规则 fallback。</p>',
  },
  {
    id: 'edit',
    title: '如何编辑或删除已有笔记？',
    answer:
      '<p><strong>编辑：</strong>进入知识库，点击任意文档卡片查看详情，在详情页顶部点击「编辑」按钮，会跳转到编辑页面，修改后保存即可。</p>' +
      '<p><strong>删除：</strong>当前版本暂未开放前端删除按钮，如需删除可在后端 API 文档页（<code>/docs</code>）中调用 DELETE 接口操作。</p>' +
      '<p class="tip">📝 编辑页面会自动加载原文和已有的 AI 转化结果，修改内容后记得重新 AI 转化。</p>',
  },
  {
    id: 'heatmap',
    title: '热力图和统计数据怎么看？',
    answer:
      '<p>进入「我的」页面可以查看你的知识管理数据：</p>' +
      '<ul>' +
      '<li><strong>热力图：</strong>灰色 = 当天无记录，淡蓝 = 1 篇，中橙 = 2 篇，深橙 = 3 篇及以上。颜色越深代表那天产出越多。</li>' +
      '<li><strong>连续打卡天数：</strong>从今天往前数，连续有创建/上传记录的天数。</li>' +
      '<li><strong>总知识资产数：</strong>知识库中所有笔记的总数。</li>' +
      '<li><strong>本月 AI 转化：</strong>本月内完成 AI 转化的文档数量。</li>' +
      '</ul>' +
      '<p>可通过下拉菜单切换不同月份查看历史热力图，点击有记录的格子可查看当天文件列表。</p>',
  },
]

const activeFaq = ref(faqList[0].id)
const activeItem = computed(() => faqList.find((f) => f.id === activeFaq.value))

const feedbackEmail = 'modelnotes@example.com'

function copyEmail() {
  navigator.clipboard.writeText(feedbackEmail).then(() => {
    ElMessage.success('邮箱地址已复制')
  }).catch(() => {
    ElMessage.info(feedbackEmail)
  })
}
</script>

<template>
  <div class="help-page">
    <!-- 左侧侧边栏 -->
    <div class="sidebar" :class="{ collapsed }">
      <div class="sidebar-title">
        <span v-show="!collapsed">帮助与反馈</span>
        <el-button
          text
          size="small"
          :icon="collapsed ? DArrowRight : DArrowLeft"
          @click="collapsed = !collapsed"
        />
      </div>
      <el-menu
        :default-active="activeFaq"
        @select="(id) => (activeFaq = id)"
        class="faq-menu"
      >
        <el-menu-item v-for="faq in faqList" :key="faq.id" :index="faq.id">
          <el-icon><QuestionFilled /></el-icon>
          <span v-show="!collapsed">{{ faq.title }}</span>
        </el-menu-item>
      </el-menu>

      <!-- 反馈邮箱 -->
      <div class="feedback-box" v-show="!collapsed">
        <div class="feedback-title">意见反馈</div>
        <div class="feedback-desc">
          如有其他问题或建议，欢迎发送邮件至：
        </div>
        <div class="feedback-email" @click="copyEmail">{{ feedbackEmail }}</div>
        <div class="feedback-note">（点击复制邮箱，不提供实际发信功能）</div>
      </div>
    </div>

    <!-- 右侧内容 -->
    <div class="content" v-if="activeItem">
      <h2 class="content-title">{{ activeItem.title }}</h2>
      <div class="content-body" v-html="activeItem.answer"></div>
    </div>
  </div>
</template>

<style scoped>
.help-page {
  display: flex;
  min-height: calc(100vh - 60px);
}

/* 侧边栏 */
.sidebar {
  width: 260px;
  min-width: 260px;
  border-right: 1px solid #e4e7ed;
  background: #fff;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  transition: width 0.25s, min-width 0.25s, padding 0.25s;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 56px;
  min-width: 56px;
  padding: 20px 0;
}

.sidebar-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  padding: 0 12px 16px;
}

.faq-menu {
  flex: 1;
  border-right: none !important;
}

.faq-menu .el-menu-item {
  height: auto;
  min-height: 44px;
  line-height: 1.5;
  font-size: 14px;
  padding: 10px 20px;
  white-space: normal;
}

/* 反馈区 */
.feedback-box {
  margin: 16px 16px 0;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.feedback-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.feedback-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}

.feedback-email {
  margin-top: 8px;
  font-size: 13px;
  color: #409eff;
  cursor: pointer;
  user-select: all;
}

.feedback-note {
  margin-top: 6px;
  font-size: 11px;
  color: #c0c4cc;
}

/* 右侧内容 */
.content {
  flex: 1;
  padding: 32px 40px;
  overflow-y: auto;
  background: #fafbfc;
}

.content-title {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.content-body {
  font-size: 15px;
  line-height: 2;
  color: #303133;
  max-width: 720px;
}

.content-body :deep(p) {
  margin: 12px 0;
}

.content-body :deep(strong) {
  color: #1a1a2e;
}

.content-body :deep(ul) {
  padding-left: 20px;
}

.content-body :deep(li) {
  margin: 6px 0;
}

.content-body :deep(code) {
  background: #e8eaed;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 13px;
}

.content-body :deep(.tip) {
  background: #ecf5ff;
  border-left: 3px solid #409eff;
  padding: 10px 14px;
  border-radius: 0 6px 6px 0;
  font-size: 14px;
  color: #606266;
}
</style>
