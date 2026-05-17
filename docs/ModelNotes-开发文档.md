# ModelNotes — 开发文档

> AI 驱动的知识库管理平台，将文档自动转化为结构化、可交互的知识笔记与思维导图。

---

## 项目概况

| 项目 | 说明 |
|------|------|
| **网站名称** | ModelNotes |
| **主题配色** | 白 + 蓝 + 黑 |
| **核心目标** | 编写整理知识库，利用大语言模型能力，将用户上传和编写的文档自动转化为结构化、可交互的知识笔记、思维导图、流程图等 |

### 技术栈

| 层级 | 技术 |
|------|------|
| **AI 编排** | LangChain / LlamaIndex |
| **后端** | Python + FastAPI |
| **数据库** | MySQL |
| **前端框架** | Vue 3 + Vite |
| **状态管理** | Pinia |
| **路由** | Vue Router |
| **UI 组件库** | Element Plus |

---

## 项目目录结构

```
modelnotes/
├── frontend/                     # Vue 3 前端
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── api/                  # API 请求封装（按模块拆分）
│   │   │   ├── index.js          #   axios 实例 + 拦截器
│   │   │   ├── document.js       #   文档相关接口
│   │   │   └── ai.js             #   AI 转化接口
│   │   ├── assets/               # 图片、字体等静态资源
│   │   │   └── logo.png
│   │   ├── components/           # 全局可复用组件
│   │   │   ├── AppHeader.vue     #   固定头部导航
│   │   │   └── HeatmapGrid.vue   #   热力图组件
│   │   ├── views/                # 页面级组件
│   │   │   ├── HomeView.vue      #   首页
│   │   │   ├── KnowledgeView.vue #   知识库列表
│   │   │   ├── DetailView.vue    #   笔记详情（左原文 + 右AI结果）
│   │   │   ├── CreateView.vue    #   创建 / 编辑 + AI 转化
│   │   │   └── MineView.vue      #   我的（热力图 + 统计）
│   │   ├── router/
│   │   │   └── index.js          # Vue Router 路由配置
│   │   ├── stores/               # Pinia 状态管理
│   │   │   ├── user.js           #   用户信息
│   │   │   └── documents.js      #   文档列表 & 当前文档
│   │   ├── utils/                # 工具函数
│   │   │   └── format.js         #   日期格式化等
│   │   ├── App.vue               # 根组件
│   │   └── main.js               # 入口：挂载 app + router + pinia
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── .env                      # VITE_API_BASE=http://localhost:8000
│
├── backend/                      # Python FastAPI 后端
│   ├── app/
│   │   ├── api/                  # 路由 & 请求处理
│   │   │   ├── __init__.py
│   │   │   ├── documents.py      #   /api/documents
│   │   │   └── ai.py             #   /api/ai/transform
│   │   ├── models/               # SQLAlchemy 数据模型
│   │   │   ├── __init__.py
│   │   │   └── document.py
│   │   ├── schemas/              # Pydantic 请求/响应校验
│   │   │   ├── __init__.py
│   │   │   └── document.py
│   │   ├── services/             # 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   └── ai_service.py     #   LangChain/LlamaIndex 调用大模型
│   │   ├── db.py                 # 数据库连接 & session 管理
│   │   └── main.py               # FastAPI 入口：注册路由 + CORS
│   ├── requirements.txt
│   └── .env                      # DATABASE_URL + OPENAI_API_KEY
│
├── docs/                         # 开发文档
│   └── ModelNotes-开发文档.md
└── README.md
```

---

## 环境与依赖

### 系统环境

| 工具 | 版本要求 | 说明 |
|------|----------|------|
| Node.js | ≥ 18 | 前端运行时 |
| Python | ≥ 3.10 | 后端运行时 |
| MySQL | ≥ 8.0 | 数据库 |

---

### 前端依赖 (`frontend/package.json`)

```jsonc
{
  "dependencies": {
    "vue": "^3.4",
    "vue-router": "^4.3",
    "pinia": "^2.1",
    "element-plus": "^2.7",
    "axios": "^1.7",
    "@element-plus/icons-vue": "^2.3",
    "marked": "^12.0",
    "markmap-view": "^0.15",
    "markmap-toolbar": "^0.15"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0",
    "vite": "^5.4",
    "unplugin-auto-import": "^0.17",
    "unplugin-vue-components": "^0.26"
  }
}
```

| 包名 | 用途 |
|------|------|
| `vue` | Vue 3 框架 |
| `vue-router` | 前端路由 |
| `pinia` | 全局状态管理 |
| `element-plus` | UI 组件库（el-select、卡片、表单等） |
| `axios` | HTTP 请求，对接后端 API |
| `@element-plus/icons-vue` | Element Plus 图标集 |
| `marked` | Markdown 文本转 HTML，渲染 AI 笔记 |
| `markmap-view` | 思维导图渲染（交互式） |
| `markmap-toolbar` | 思维导图工具栏（缩放/拖拽） |
| `unplugin-auto-import` | 自动导入 Vue/Element Plus API，省去手写 import |
| `unplugin-vue-components` | 自动按需引入 Element Plus 组件，减小打包体积 |

> **安装命令**：`cd frontend && npm install`

---

### 后端依赖 (`backend/requirements.txt`)

```txt
# Web 框架
fastapi==0.115.0
uvicorn[standard]==0.30.0

# 数据库
sqlalchemy==2.0.35
pymysql==1.1.1
alembic==1.13.0

# 数据校验
pydantic==2.9.0

# AI 编排 (二选一，推荐 LangChain)
langchain==0.3.0
langchain-openai==0.2.0

# CORS 跨域
# (仅本地开发需要，前端 localhost:5173 → 后端 localhost:8000)

# 环境变量
python-dotenv==1.0.1
```

| 包名 | 用途 |
|------|------|
| `fastapi` | Web 框架，路由 + 中间件 |
| `uvicorn` | ASGI 服务器，运行 FastAPI |
| `sqlalchemy` | ORM，操作 MySQL（不写原生 SQL） |
| `pymysql` | MySQL 驱动，SQLAlchemy 底层依赖 |
| `alembic` | 数据库迁移工具（建表/改表不用手写 SQL） |
| `pydantic` | 请求/响应数据校验，FastAPI 内置依赖 |
| `langchain` | LLM 调用编排（Prompt 模板 + 链式调用） |
| `langchain-openai` | LangChain 的 OpenAI 适配器 |
| `python-dotenv` | 从 `.env` 文件加载环境变量 |

> **安装命令**：`cd backend && pip install -r requirements.txt`

---

## 全局布局 & 路由

### 固定头部 (Header)

所有页面共享的全局组件：

```
┌──────────────────────────────────────────────────────┐
│  [Logo + 名称]   首页  知识库  创建  AI转化  我的   [帮助与反馈] │
└──────────────────────────────────────────────────────┘
```

- **左侧**：网站 Logo + 网站名称
- **中间**：五个导航分栏（`首页` / `知识库` / `创建` / `AI转化` / `我的`）
- **右侧**：帮助与反馈入口

### 路由设计

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | 首页 | 项目简介 + 跳转创建 |
| `/knowledge` | 知识库 | 宫格 / 列表展示 |
| `/create` | 创建 | 编辑器 + AI 转化入口 |
| `/mine` | 我的 | 热力图 + 统计仪表盘 |

> **注意**："AI 转化"导航点击后直接跳转到 `/create` 页面并自动聚焦输入框，不设独立页面。

---

## 一、首页

- **网站介绍与初心**：展示产品理念和核心价值
- **快速入口**：在介绍旁边放置箭头按钮，点击直接跳转到 `/create` 新建知识库

---

## 二、知识库

### 展示模式

| 模式 | 说明 |
|------|------|
| **宫格视图** | 卡片式展示，显示标题、日期、标签 |
| **列表视图** | 紧凑列表展示 |

### 卡片信息

- 标题
- 创建 / 修改日期
- 标签（手动添加）

### 空状态设计

知识库为空时，引导用户：
- "创建第一篇笔记"
- "上传文档试试"

### 详情页

点击卡片进入详情页，采用 **左右分栏** 布局：

```
┌──────────────────┬──────────────────┐
│                  │  [笔记] [导图]    │
│  Markdown 原文   │                  │
│                  │  AI 转化结果      │
│                  │                  │
└──────────────────┴──────────────────┘
```

- **左侧**：Markdown 原文展示
- **右侧**：AI 转化的笔记 / 思维导图切换栏
- **操作**：删除、编辑标题等，通过 Pinia + API 实现

---

## 三、创建

### 支持的文件类型

- Markdown 文档（`.md`）
- 思维导图
- XLS / XLSX（规划中）

### 编辑器

- 基于 **textarea** 或 **Monaco Editor** 的 Markdown 编辑模式
- 支持保存到 MySQL
- 支持上传 `.md` 文件直接读取内容入库

### 数据流

```
编辑器输入 → API 保存 → MySQL 存储 → 知识库展示
    │
    └─→ "AI 转化" 按钮 → 调用大模型 → 生成笔记 + 导图 → 入库 → 详情页展示
```

---

## 四、AI 转化

### 输入

- 用户粘贴文本
- 上传 `.md` 文件（限纯文本）

### 输出

#### 1. 知识笔记

- 带层级的结构化文本
- 关键概念 **加粗** / 高亮
- 可折叠段落

#### 2. 思维导图 JSON

- 生成 Markdown 列表格式
- 使用 [markmap](https://markmap.js.org/) 库渲染
- 支持交互：缩放、拖拽

### 实现方案

```
用户输入
  │
  ▼
调用 OpenAI / ChatGLM 等 API
  │  Prompt 要求输出两部分：
  │  ① 结构化 Markdown 笔记（含分级标题、要点列表）
  │  ② 思维导图纯列表结构
  ▼
前端:
  - marked 解析 Markdown 笔记
  - markmap 渲染思维导图（可交互）
```

> **成本控制**：思维导图仅需生成 Markdown 列表格式，AI token 成本极低。

---

## 五、我的

### 1. 热力图

展示每个月份每天编写 / 上传知识库文件的数量。

#### 交互细节

- **下拉选择月份**：使用 `el-select` 切换月份
- **颜色梯度**：

  | 文档数 | 颜色 |
  |--------|------|
  | 0 | 灰色 |
  | 1 | 淡蓝 |
  | 2 | 中橙 |
  | 3+ | 深橙 |

- **Tooltip**：hover 显示当日数量
- **点击格子**：弹窗显示当天创建 / 上传的文件列表（可选）

#### 数据格式

```json
{ "date": "2026-05-01", "count": 3 }
```

#### 实现

- **后端**：用户每次创建 / 上传文件时记录 `user_id` + `date`，按日期 `GROUP BY` 统计
- **前端**：CSS Grid 手写或使用 `v-calendar` 热力图组件

---

### 2. 统计仪表盘

位于热力图上方或侧边，展示以下指标：

| 指标 | 说明 |
|------|------|
| **连续打卡天数** | 激励习惯养成 |
| **总知识资产数** | 笔记 + 导图 + 卡片总数 |
| **本月 AI 转化次数** | 本月调用大模型转化的次数 |
| **被关联引用次数** | 笔记之间的关联引用统计 |

---

## 页面流程总览

```
首页 ──→ 创建页 ──→ AI 转化 ──→ 知识库详情页
  │                                  │
  └── 知识库列表 ←──────────────────┘
  │
  └── 我的（热力图 + 统计）
```
