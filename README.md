# codesugar

> Claude Code 插件市场仓库 — 由 Lei Zhang 维护的效率提升工具集合

## 概述

codesugar 是一个 Claude Code 插件市场（Marketplace），包含提高日常开发工作效率的技能和工具。通过 Claude Code 的插件系统安装后，可以使用 TAPD 集成和 DevOps 自动化功能。

## 插件列表

### tapd

TAPD（Tencent Agile Product Development）集成插件，包含以下技能：

| 技能 | 描述 |
|------|------|
| **commit** | 创建符合 Conventional Commits 规范的 git commit，自动关联 TAPD 需求源码关键字 |
| **story-to-tasks** | 根据 TAPD 需求拆分前端开发任务并评估工时 |

### routine

MCP 服务器，用于管理 GitLab Merge Request 和 Jenkins Job。

## 安装

### 添加市场

```bash
claude plugin marketplace add https://github.com/PassionZale/codesugar.git
```

### 安装插件

```bash
# 安装 TAPD 插件
claude plugin install tapd@codesugar

# 安装 Routine 插件
claude plugin install routine@codesugar
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
codesugar/
├── .claude-plugin/
│   └── marketplace.json          # 市场清单
├── plugins/
│   └── tapd/                     # TAPD 插件
│       └── skills/
│           ├── commit/           # Commit 技能
│           └── story-to-tasks/   # 任务拆分技能
├── external_plugins/
│   └── routine/                  # Routine MCP 服务器
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
