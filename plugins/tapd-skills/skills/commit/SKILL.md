---
name: commit
description: 创建符合 Conventional Commits 规范的 git commit，自动关联 TAPD 源码关键字。仅当用户明确请求时使用，例如："commit"、"提交代码"、"生成 commit message"等。仅处理已暂存的更改，不处理未暂存的文件。
---

创建符合 Conventional Commits 规范的 git commit，自动关联 TAPD 源码关键字。

## 核心原则

1. **不要添加任何广告** - 禁止在提交信息中添加任何广告或推广链接，例如 "Generated with [Claude Code](https://claude.ai/code)"
2. **仅处理已暂存的更改** - 不处理未暂存的文件，没有已暂存更改时提示用户并退出
3. **使用中文** - Subject 和 Body 必须使用中文
4. **简洁明了** - Subject 最多 50 个字符，Body 高度概括
5. **祈使语气** - 使用"添加"而非"添加了"

## 步骤

### 1. ya