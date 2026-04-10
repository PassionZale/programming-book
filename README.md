# programming-book

> Claude Code 插件市场仓库 — 由 Lei Zhang 维护的效率提升工具集合

## 概述

programming-book 是一个 Claude Code 插件市场（Marketplace），包含提高日常开发工作效率的技能和工具。通过 Claude Code 的插件系统安装后，可以使用 TAPD 集成和 DevOps 自动化功能。

## 插件列表

### tapd

TAPD（Tencent Agile Product Development）集成插件，包含以下技能：

| 技能 | 描述 |
|------|------|
| **commit** | 创建符合 Conventional Commits 规范的 git commit，自动关联 TAPD 需求源码关键字 |
| **story-to-tasks** | 根据 TAPD 需求拆分前端开发任务并评估工时 |

### routine

MCP 服务器，用于管理 GitLab Merge Request 和 Jenkins Job。

### zai

智谱视觉理解 MCP 服务器，提供图像分析和视频理解功能。

### tavily

MCP 服务器，提供实时网络搜索、网页提取、网站地图和爬取功能。

### context7

MCP 服务器，为 LLM 和 AI 代码编辑器提供最新的代码文档查询。

### fetch

MCP 服务器，用于获取和处理网页内容，将 HTML 转换为 Markdown 格式。

## 安装

### 添加市场

```bash
claude plugin marketplace add https://github.com/PassionZale/programming-book.git
```

### 安装插件

```bash
# 安装 TAPD 插件
claude plugin install tapd@programming-book

# 安装 Routine 插件
claude plugin install routine@programming-book

# 安装 Zai 插件
claude plugin install zai@programming-book

# 安装 Tavily 插件
claude plugin install tavily@programming-book

# 安装 Context7 插件
claude plugin install context7@programming-book

# 安装 Fetch 插件
claude plugin install fetch@programming-book
```

## 配置

### TAPD 插件

在 Claude Code 设置中配置以下环境变量：

| 变量名 | 描述 |
|--------|------|
| `TAPD_WORKSPACE_ID` | TAPD 工作空间 ID |
| `TAPD_ACCESS_TOKEN` | TAPD 访问令牌 |
| `ZAI_CODING_PLAN_KEY` | 智谱编码套餐令牌（可选） |

### Routine 插件

| 变量名 | 描述 |
|--------|------|
| `JENKINS_BASE_URL` | Jenkins 服务器基础地址 |
| `JENKINS_USERNAME` | Jenkins 用户名 |
| `JENKINS_ACCESS_TOKEN` | Jenkins API 访问令牌 |
| `GITLAB_BASE_URL` | GitLab API 基础地址 |
| `GITLAB_ACCESS_TOKEN` | GitLab API 访问令牌 |

### Zai 插件

| 变量名 | 描述 |
|--------|--------|
| `Z_AI_MODE` | 智谱模式 |
| `Z_AI_BASE_URL` | 智谱 API 基础地址 |
| `Z_AI_API_KEY` | 智谱 API 密钥 |
| `Z_AI_VISION_MODEL` | 视觉模型名称 |

### Tavily 插件

| 变量名 | 描述 |
|--------|--------|
| `TAVILY_API_KEY` | Tavily API 密钥 |

### Context7 插件

| 变量名 | 描述 |
|--------|--------|
| `CONTEXT7_API_KEY` | Context7 API 密钥 |

### Fetch 插件

无需配置，开箱即用。支持代理（默认 `http://127.0.0.1:7897`）。

## 使用示例

### commit 技能

```
/commit
```

自动分析暂存区变更，生成符合规范的 commit 信息，并关联相关的 TAPD 需求。

### story-to-tasks 技能

```
/story-to-tasks --s <story_id>
```

根据 TAPD 需求 ID，结合项目源码分析，拆分前端开发任务并评估工时。

## 开发

### 技术栈

- **脚本语言**: Python 3.x
- **包管理**: uv
- **配置格式**: JSON
- **文档格式**: Markdown

### 项目结构

```
programming-book/
├── .claude-plugin/
│   └── marketplace.json          # 市场清单
├── plugins/
│   └── tapd/                     # TAPD 插件
│       └── skills/
│           ├── commit/           # Commit 技能
│           └── story-to-tasks/   # 任务拆分技能
├── external_plugins/
│   ├── routine/                  # GitLab MR + Jenkins Job 管理
│   ├── zai/                      # 智谱视觉理解
│   ├── tavily/                   # 实时搜索、网页提取
│   ├── context7/                 # 代码文档查询
│   └── fetch/                    # 网页内容获取
└── docs/                         # 文档
```

### 运行脚本

```bash
# 使用 uv 运行 Python 脚本
uv run plugins/tapd/skills/commit/scripts/get_user_todo_story.py -w <workspace_id>
```

## 文档

- [插件市场架构说明](docs/guide.md) — Claude Code 插件分发机制详解
- [CLAUDE.md](CLAUDE.md) — 项目开发规范和约定

## 许可证

MIT

## 作者

Lei Zhang — [@PassionZale](https://github.com/PassionZale)
