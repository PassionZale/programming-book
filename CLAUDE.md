# Project Instructions

## 项目概述

programming-book 是 Claude Code 插件市场仓库，由 Lei Zhang 维护，包含 TAPD 集成和 DevOps 自动化插件。

## 技术栈

- **脚本语言**: Python 3.x (使用 uv 包管理)
- **配置格式**: JSON
- **文档格式**: Markdown

## 代码规范

- **文件命名**: kebab-case (如 `get_user_todo_story.py`)
- **技能定义**: SKILL.md 使用 YAML frontmatter
- **Python 代码**: 遵循 PEP 8，使用 type hints

## Git 工作流

- **提交格式**: Conventional Commits
- **类型**: feat, fix, chore, refactor, docs, style, perf, test, ci, build, revert
- **Subject**: 中文祈使句，≤50 字符，末尾无标点
- **Scope**: 明确模块时保留，如 `refactor(tapd-skills): ...`

## 项目结构

```
.claude-plugin/marketplace.json    # 市场清单（插件注册表）
plugins/tapd/                      # TAPD 插件（内部维护）
  └─ skills/
      ├─ commit/                  # Git commit 技能
      │   └─ scripts/             # Python 脚本
      └─ story-to-tasks/          # 任务拆分技能
          └─ scripts/             # Python 脚本
external_plugins/routine/          # 外部 MCP 服务器（submodule）
docs/                              # 项目文档
```

## 开发命令

```bash
# 运行 Python 脚本
uv run plugins/tapd/skills/commit/scripts/get_user_todo_story.py -w <workspace_id>

# 安装依赖
uv add <package>

# 同步环境
uv sync
```

## 插件开发

### 技能定义

每个技能目录包含 `SKILL.md`，使用 frontmatter 定义元数据：

```yaml
---
name: skill-name
description: 技能描述
---
```

### Python 脚本

脚本位于 `scripts/` 子目录，使用 `${CLAUDE_SKILL_DIR}` 环境变量引用路径。

### TAPD 集成

- **API 基础地址**: `https://api.tapd.cn/`
- **认证方式**: Bearer Token
- **工作空间 ID**: 通过环境变量配置

## 环境变量

通过 Claude Code 的 `userConfig` 配置：

- `TAPD_WORKSPACE_ID`: TAPD 工作空间 ID
- `TAPD_ACCESS_TOKEN`: TAPD 访问令牌
- `ZAI_CODING_PLAN_KEY`: 智谱编码套餐令牌

## 技能说明

### commit 技能

创建符合 Conventional Commits 规范的 git commit，自动关联 TAPD 需求。

**触发**: 用户明确请求 commit 时

**步骤**:
1. 验证暂存状态
2. 分析代码变更
3. 获取 TAPD 源码关键字（可选）
4. 生成并执行 commit

### story-to-tasks 技能

根据 TAPD 需求拆分前端开发任务并评估工时。

**触发**: 提供 story_id 并要求拆分任务时

**步骤**:
1. 获取需求详情
2. 确定目标 domain
3. 加载项目上下文
4. 拆分任务并评估工时
5. 输出结果到 `tasks/<story_id>.md`
