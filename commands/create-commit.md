---
allowed-tools:
  - Bash(git diff:*)
  - Bash(git commit:*)
  - Bash(git log:*)
description: 创建符合 Conventional Commits 规范的 git commit
---

# 创建 Git 提交

创建符合 Conventional Commits 规范的 git commit。

## 步骤

### 1. 验证暂存状态

运行以下命令检查是否有已暂存的更改：

```bash
git diff --staged --stat
```

- **有已暂存的更改** → 继续分析
- **没有已暂存的更改** → 提示用户后退出

### 2. 分析已暂存的更改

收集以下信息：

```bash
# 已暂存的更改详情
git diff --staged
```

分析：
- 哪些文件更改了
- 更改的性质（功能、修复、重构、文档等）
- 受影响的模块/范围

### 3. 生成提交信息

提交信息格式：

```
<type>(<scope>): <subject>

<body>
```

#### Type 类型

选择最合适的类型：
- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 仅文档更改
- **style**: 格式化、空格等不影响代码含义的更改
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
- 应清晰明了，最多 50 个字符
- 末尾不加句号
- 祈使语气（"添加"而非"添加了"）

**避免使用**：
- 模糊的主题，如："update"、"fix stuff"
- 过长或重点不突出的主题

#### Body 正文（可选）

- 使用中文
- 简洁明了，高度概括
- 解释做什么和为什么（不是怎么做）

#### 示例


1. 标题示例

```
feat(auth): 添加 JWT 令牌验证
```

2. 包含标题和正文的示例

```
feat(auth): 添加 JWT 登录流程

- 实现了 JWT 令牌验证逻辑
- 为验证组件添加了文档说明
```

## 最终步骤

1. 创建提交：`git commit -m "<message>"`
2. 显示确认：`git log -1 --stat`
