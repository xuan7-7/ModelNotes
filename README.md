<h1 align="center">🧠 ModelNotes</h1>
<p align="center">AI 驱动的知识库 — 将文档自动转化为结构化笔记与思维导图</p>

<p align="center">
  <img alt="Vue" src="https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vuedotjs&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" />
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white" />
  <img alt="DeepSeek" src="https://img.shields.io/badge/DeepSeek-API-536DFE" />
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green" />
</p>

---

## ✨ 为什么用 ModelNotes

写 Markdown 做笔记很简单，但让笔记变得**结构化、可视化、可回顾**就很花时间。ModelNotes 把这件事交给了 AI：

- 写完文档，点一下按钮，AI 自动提炼出**层级分明的知识笔记**和**可拖拽的思维导图**
- 每天产出自动汇成**热力图**，像 GitHub 贡献图一样记录你的学习轨迹
- 标签、搜索、批量操作，像管理代码一样管理你的知识资产

## 🎯 功能

| 模块 | 说明 |
|------|------|
| **Markdown 编辑器** | 实时预览，支持上传 .md 文件，字数统计 |
| **AI 转化** | 调用 DeepSeek 自动生成结构化笔记 + mindmap 列表，markmap 渲染为交互式导图 |
| **知识库** | 宫格 / 列表双视图，标签分类，多选批量删除 / 批量导出 |
| **热力图** | 按天统计产出，颜色梯度显示，点击格子查看当天文件 |
| **统计仪表盘** | 连续打卡天数、总资产数、本月 AI 转化次数 |
| **帮助中心** | 可折叠侧边栏，内置 FAQ，一键复制反馈邮箱 |

## 🛠 技术栈

```
前端：Vue 3  +  Vite  +  Pinia  +  Vue Router  +  Element Plus
后端：Python  +  FastAPI  +  SQLAlchemy  +  PyMySQL
AI  ：DeepSeek API（httpx 直调，兼容 OpenAI 协议）
渲染：marked  +  markmap
数据库：MySQL 8.0
```text

## 📁 目录结构

```text
modelnotes/
├── frontend/                 # Vue 3 SPA
│   ├── src/
│   │   ├── api/              # axios 封装 & 接口定义
│   │   ├── components/       # 全局组件
│   │   ├── views/            # 页面组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态
│   │   └── utils/            # 工具函数
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── backend/                  # RESTful API
│   ├── app/
│   │   ├── api/              # 路由处理
│   │   ├── models/           # ORM 模型
│   │   ├── schemas/          # Pydantic 校验
│   │   ├── services/         # 业务逻辑（AI 调用）
│   │   ├── db.py             # 数据库连接 & 建表
│   │   └── main.py           # 应用入口 & CORS
│   ├── requirements.txt
│   ├── .env.example          # 环境变量模板
│   └── .env                  # 本地配置（不入库）
├── docs/                     # 开发文档
├── .gitignore
└── README.md
```

## 🚀 本地运行

### 前置条件

- **Node.js** ≥ 18
- **Python** ≥ 3.10
- **MySQL** ≥ 8.0（需提前创建空数据库）

### 1. 克隆项目

```bash
git clone https://github.com/yourname/modelnotes.git
cd modelnotes
```

### 2. 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 MySQL 密码和 DeepSeek API Key

# 启动服务（首次运行自动建表）
uvicorn app.main:app --port 8000
```

访问 [http://localhost:8000/docs](http://localhost:8000/docs) 查看 Swagger 文档。

### 3. 启动前端

```bash
cd frontend

npm install
npm run dev
```

浏览器打开 [http://localhost:5173](http://localhost:5173)。

### 环境变量

| 变量 | 示例值 | 说明 |
|------|--------|------|
| `DATABASE_URL` | `mysql+pymysql://root:password@localhost:3306/modelnotes` | MySQL 连接串 |
| `DEEPSEEK_API_KEY` | `sk-xxxxxxxx` | DeepSeek API Key，不填使用规则 fallback |

## 📡 API

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/api/documents` | 文档列表（分页） |
| `POST` | `/api/documents` | 创建文档 |
| `GET` | `/api/documents/:id` | 文档详情（含全文） |
| `PUT` | `/api/documents/:id` | 更新文档 |
| `DELETE` | `/api/documents/:id` | 删除文档 |
| `POST` | `/api/documents/batch-delete` | 批量删除 |
| `POST` | `/api/ai/transform` | AI 转化（返回 notes + mindmap） |
| `POST` | `/api/ai/transform/:id` | AI 转化并写入数据库 |
| `GET` | `/api/stats/overview` | 统计概览 + 热力图数据 |

## 🤝 贡献

欢迎提 Issue 和 PR。Clone 后按上方步骤跑起来即可开始开发。

## 📄 License

MIT © ModelNotes
