---
name: creating-tapd-scm-copy-keywords
description: 获取 TAPD 源码关键字，并生成 Markdown 文件。
---

# Creating TAPD SCM Copy Keywords

从 TAPD 获取源码关键字，并生成 Markdown 文件。

## 核心原则

- **必须指定迭代** - 通过 $ARGUMENTS[0] 传入迭代名称，未提供时提示用户
- **需求处理人** - 通过 $ARGUMENTS[1] 传入处理人, 为提供时提示用户
- **需求名称** - 通过 $ARGUMENTS[2] 传入过滤条件, 可选
- **使用 TAPD MCP 工具** - 依赖 TAPD MCP 服务器提供的工具
- **生成日期文件** - 输出文件名格式为 `{迭代结束日期的前一天}.md`

## 步骤

### 1. 验证参数和 MCP 工具

首先确认：

- **$ARGUMENTS[0] 是否提供** - 未提供时提示用户：`请提供迭代名称(支持模糊搜索)，例如：/creating-tapd-scm-copy-keywords 0326 张三`
- **$ARGUMENTS[1] 是否提供** - 未提供时提示用户：`请提供需求处理人(支持模糊搜索)，例如：/creating-tapd-scm-copy-keywords 0326 张三`
- **TAPD MCP 工具是否可用** - 尝试列出可用工具确认

### 2. 获取迭代信息

使用 `mcp__tapd__get_iterations` 获取迭代信息：

```
workspace_id: <从配置或参数获取>
options: {
  "name": "$ARGUMENTS[0]",
  "order": "startdate%20desc",
  "fields": "id,name,startdate,enddate",
  "limit": 5
}
```

### 3. 获取需求列表

使用 `mcp__tapd__get_stories_or_tasks` 获取该迭代当前用户的需求列表：

```
workspace_id: <同上>
options: {
  "iteration_id": "<迭代ID>",
  "owner": "<$ARGUMENTS[1]>",
  "name": "<$ARGUMENTS[2]> 存在则使用, 否则传入空字符串",
  "entity_type": "story"
  "fields": "id,name",
  "limit": 200
}
```

### 4. 获取每个需求的源码关键字

对每个需求，使用 `mcp__tapd__get_commit_msg` 获取源码提交信息：

```
workspace_id: <同上>
options: {
  "object_id": "<需求ID>",
  "type": "story"
}
```

### 5. 生成输出文件

生成文件名：`{YYYYMMDD}.md`, 文件内容模板参考 [template.md](template.md).

## 注意事项

- 如果迭代不存在或无法访问，提示用户检查迭代 ID 和 workspace 权限
- 输出文件保存在当前工作目录
- 若文件已存在, 则提示用户是否允许覆盖
