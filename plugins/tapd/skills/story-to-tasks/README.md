# story-to-tasks

> Claude Code Skill — 根据需求拆分前端开发任务并评估工时

从 TAPD 获取需求详情，结合项目源码上下文，自动拆分成可执行的开发任务并预估工时。

## 功能特性

- **智能需求解析** — 从 TAPD 获取需求详情（支持短 ID / 长 ID）
- **视觉分析** — 使用 GLM-4.6V FlashX 分析需求中的 UI 原型图
- **上下文增强** — 结合项目 agent skill 知识库理解业务逻辑
- **5 维度工时** — 页面/路由、组件、接口对接、状态管理、前后端联调
- **批量创建** — 一键在 TAPD 批量创建拆分后的任务
- **多域支持** — 支持按业务域（Domain）筛选任务

## 快速开始

### 1. 生成代码仓库知识库

> ⚠️ **注意**：知识库文件涉及项目源码，已被 `.gitignore` 忽略，不在仓库中。首次使用必须先生成。

拆分任务需要结合项目源码上下文，先生成 agent skill 知识库, 

然后在 [`references/domain.md`](./references/domain.md) 中维护 Domain 映射关系。

```bash
npx repomix@latest <path/to/directory> \
  --skill-generate <domain>-reference \
  --skill-output ./references/domains/<domain>-reference \
  --force
```

示例：

```bash
# 生成 yos-web 知识库
npx repomix@latest ~/Documents/zhongran/yos-web \
  --skill-generate yos-web-reference \
  --skill-output ./references/domains/yos-web-reference \
  --force

# 生成 yph-customer-web 知识库
npx repomix@latest ~/Documents/zhongran/yph-customer-web \
  --skill-generate yph-customer-web-reference \
  --skill-output ./references/domains/yph-customer-web-reference \
  --force
```

### 2. 配置环境

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
TAPD_ACCESS_TOKEN=your_access_token
TAPD_WORKSPACE_ID=your_workspace_id
GLM_API_KEY=your_glm_api_key
```

### 3. 使用 Skill

在 Claude Code 中触发：

```bash
/story-to-tasks --s <story_id>
/story-to-tasks --s <story_id> --w <workspace_id>
/story-to-tasks --s <story_id> --d yos-web,yph-customer-web
```

## 数据流程

```
【阶段 1：获取需求】
用户输入 story_id
    ↓
get_story.py 调用 TAPD API
    ↓
解析需求描述 HTML（提取图片）
    ↓
并发调用 GLM-4.6V FlashX 分析图片
    ↓
输出纯文本需求（stdout + $PWD/tasks/<story_id>.md）

【阶段 2：拆分任务】
LLM 基于需求 + 项目知识库 拆分任务
    ↓
用户确认任务拆分结果
    ↓
输出任务 JSON → $PWD/tasks/<story_id>.json
    格式：[{domain, dimension, name, description, effort}, ...]

【阶段 3：批量创建】
create_tasks.py 读取 JSON 文件
    ↓
获取当前用户信息（creator/owner）
    ↓
获取父 Story 信息（继承优先级、迭代）
    ↓
逐条构造任务数据
    ↓
调用 TAPD API 创建任务
    ↓
输出创建结果（成功/失败统计）
```
