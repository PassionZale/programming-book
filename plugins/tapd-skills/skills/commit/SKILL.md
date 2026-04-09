---
name: commit
description: 创建符合 Conventional Commits 规范的 git commit，自动关联 TAPD 代办需求的源码关键字。仅当用户明确请求时使用，例如："commit"、"提交代码"、"生成 commit message"等。仅处理已暂存的更改，不处理未暂存的文件。
---

创建符合 Conventional Commits 规范的 git commit，自动关联 TAPD 代办需求的源码关键字。

## 核心原则

1. **不要添加任何广告** - 禁止在提交信息中添加任何广告或推广链接，例如 "Generated with [Claude Code](https://claude.ai/code)"
2. **仅处理已暂存的更改** - 不处理未暂存的文件，没有已暂存更改时提示用户并退出
3. **使用中文** - Subject 和 Body 必须使用中文
4. **简洁明了** - Subject 最多 50 个字符，Body 高度概括
5. **祈使语气** - 使用"添加"而非"添加了"

## 输入

用户的请求应包含:

- 需求ID: story_id (number) 可选）
- 工作空间ID: workspace_id (number)（可选）

```bash
/commit

/commit --s <story_id>

/commit --s <story_id> --w <workspace_id>
```

## 步骤

### Step 0 - 验证暂存状态

```bash
git diff --staged --stat
```

- **有已暂存的更改** → 继续分析
- **没有已暂存的更改** → 提示用户先使用 `git add` 暂存文件，然后退出

### Step 1 - 分析已暂存的更改

```bash
git diff --staged
```

分析：

- 哪些文件更改了
- 更改的性质（功能、修复、重构、文档等）
- 受影响的模块/范围

### Step 2 - 获取 TAPD 源码关键字

- 指定 <story_id> -> 运行 `python3 ${CLAUDE_SKILL_DIR}/scripts/get_commit_msg.py --s <story_id>` 获取
- 未指定 <story_id> -> 运行 `python3 ${CLAUDE_SKILL_DIR}/scripts/get_todo_stories.py --w <workspace_id>` 获取用户代办列表 `{id: story_id, name: story_name}[]`, 根据 Step 1 中的分析匹配到最相关的<story_id>, 再运行运行 `python3 ${CLAUDE_SKILL_DIR}/scripts/get_commit_msg.py --s <story_id>` 获取

### Step 3 - 生成提交信息

严格按照此格式生成提交信息：

```bash
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 仅文档更改
- **style**: 格式化、空格等
- **refactor**: 代码重构
- **perf**: 性能改进
- **test**: 添加或更新测试
- **chore**: 维护任务、依赖更新
- **ci**: CI 配置更改
- **build**: 构建系统更改
- **revert**: 回退提交

#### Scope 范围

- **有明确范围**：使用模块名（如 `auth`, `api`, `ui`）
- **范围不明确**：省略 scope，直接写 `<type>: <subject>`

#### Subject 主题

- 使用中文
- 最多 50 个字符
- 末尾不加句号
- 祈使语气（"添加"而非"添加了"）

**避免使用**：

- 模糊的主题，如："update"、"fix stuff"
- 过长或重点不突出的主题

#### Body 正文（可选）

- 使用中文
- 简洁明了，高度概括
- 解释做什么和为什么（不是怎么做）

#### Footer 源码关键词 (可为空)

若 Step 2 获取的结果为空, 则 footer 为空.

### Step 4 - 创建提交

```bash
git commit -m "<message>"
git log -1 --stat
```

**说明**：`<message>` 已包含完整的提交信息（含 tapd_scm_copy_keywords footer）

## 示例

### 带 TAPD 源码关键字的提交

```
feat(clue): 商机关闭新增附件上传功能

- 商机关闭流程新增附件上传字段支持
- 优化 Close 状态下的内容显示逻辑
- 同时支持传统业务和家庭帮业务场景

--story=1040462@tapd-40888836 --user=壹品慧张磊 客资H5 - 商机关闭新增附件支持上传图片, 包含家庭帮和传统业务 https://www.tapd.cn/40888836/s/2547032
```

### 标准 Conventional Commits 提交

```
feat(auth): 添加 JWT 令牌验证
```

```
feat(auth): 添加 JWT 登录流程

- 实现了 JWT 令牌验证逻辑
- 为验证组件添加了文档说明
```

```
docs: 更新 README 安装说明
```
