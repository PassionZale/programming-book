---
name: story-to-tasks
description: 根据需求拆分前端开发任务并评估工时。当用户提供 story_id 并要求拆分任务、评估工时、任务分解时触发。支持筛选特定业务域。即使用户只说"帮我拆一下这个需求"、"评估一下工时"，也应触发。
---

根据 story_id，结合领域的源码，将前端需求拆分成可执行的开发任务，并按小时评估工时。

## 输入

用户的请求应包含:

- 需求ID: story_id (number)
- 工作空间ID: workspace_id (number)（可选）
- 领域: domain (domain1,domain2,...)（可选）

```
/story-to-tasks --s <story_id>
/story-to-tasks --s <story_id> --w <workspace_id>
/story-to-tasks --s <story_id> --w <workspace_id> --d <domain1,domain2,...>
```

## 运行时初始化

每个会话开始时执行一次，检测可用的 Python 运行时：

```bash
# 检测 Python 运行时
if command -v uv &>/dev/null; then PY="uv run"
elif command -v python3 &>/dev/null; then PY="python3"
elif command -v python &>/dev/null; then PY="python"
else echo "Error: 请安装 Python 或 uv"; exit 1; fi
```

后续所有脚本调用统一使用 `${PY}` 变量。

## 步骤

### Step 0 — 确认输入

如果用户没有提供 story_id，**先询问**，不得继续执行。必须明确知道要处理哪个需求才能继续。

### Step 1 — 获取需求详情

运行 `${PY} scripts/get_story.py` 获取需求详情, 示例:

```bash
## 使用默认工作空间
${PY} scripts/get_story.py --s <story_id>

## 若需要指定工作空间
${PY} scripts/get_story.py --s <story_id> --w <workspace_id>
```

### Step 2 — 确定目标 Domain

1. 读取 `references/domain.md`，了解 domain key → 业务模块的映射关系
2. 确定需要处理的 domain：
   - 用户指定了 `--d`：直接使用指定的 domain key 列表
   - 用户未指定：根据需求文档中出现的业务模块名称，自动匹配对应 domain
   - 若业务模块和 domain 匹配不上, 则直接基于需求内容拆解

### Step 3 — 加载项目上下文

对每个目标 domain，按以下顺序加载上下文, 读取 `references/domains/<domain>-reference/SKILL.md`：

- 理解项目结构和文件组织方式
- 查找特定功能的实现位置
- 阅读任何文件的源代码
- 搜索代码模式或关键字

### Step 4 — 拆分任务 & 评估工时

读取 `references/effort_rules.md` 作为工时评估依据, 从以下五个维度拆分任务：

1. **页面 / 路由维度** — 需要新增或改动哪些页面、路由
2. **组件维度** — 需要新增或改动哪些组件（含弹窗、抽屉、表单等）
3. **接口对接维度** — 需要对接哪些后端接口
4. **状态管理维度** — 是否涉及新增/修改 Store，跨页面共享状态等
5. **前后端联调维度** — 根据接口数量和复杂度估算联调工时

**根据检索结果调整工时：**

- ✅ 找到可直接复用的实现 → 工时 ×0.7，依据中注明参考文件路径
- 🔄 找到可参考的相似实现 → 工时 ×0.8，依据中注明参考文件路径
- ❌ 未找到任何相关实现 → 按基准工时，依据中注明"无现成参考"

**每个任务包含：**

- 任务名称（简洁，动词开头，如「新增订单列表页」）
- 所属维度
- 详细描述（1-3句，说明做什么、注意什么）
- 工时估算（小时，如 `4h`、`6h`）
- 工时依据（1句话，说明估算理由 + 是否有可复用代码）

**其他工时评估要求：**

- 参考 `references/effort_rules.md` 的基准区间和调整系数
- 单任务超过 8h 考虑拆分
- 不确定时取区间上限

### Step 5 — 输出结果

先以分层列表展示，再附上汇总表格，最后给出总工时, 完成任务拆分后，将结果保存为：`$PWD/tasks/<story_id>.md`。

**格式示例：**

```markdown
## 任务拆分 — <需求名称> (<domain>)

### 页面 / 路由

- **[P1] 新增「订单管理」页面**
  - 描述：在 `/order/list` 路由下新增列表页，含分页、筛选栏、操作列。
  - 工时：`6h`
  - 依据：全新列表页，src/pages/customer/CustomerList.tsx 有相似结构可参考，下调至 6h。

### 组件

- **[C1] 封装 OrderStatusTag 组件**
  - 描述：根据订单状态展示对应颜色标签，复用 AntD Tag，封装业务语义。
  - 工时：`1h`
  - 依据：基于 UI 库简单封装，0.5~1h 取上限，无现成参考。

### 接口对接

- **[A1] 对接订单列表接口**
  - 描述：GET /api/orders，支持分页+筛选参数，URL 参数同步。
  - 工时：`2h`
  - 依据：分页筛选接口基准 2~3h，src/services/customer.ts 有同类封装模式，下调至 2h。

### 状态管理

- **[S1] 扩展 orderStore 模块**
  - 描述：在现有 orderStore 中新增查询条件和分页 state，供列表页和详情页共享。
  - 工时：`1.5h`
  - 依据：扩展已有 Store 基准 0.5~2h，src/stores/order.ts 已存在模块，取中间值 1.5h。

### 前后端联调

- **[L1] 订单管理模块联调**
  - 描述：与后端对齐订单列表、详情共 2 个接口的参数格式、异常情况和边界处理。
  - 工时：`3h`
  - 依据：2 个接口，复杂度一般，参考基准 2~4h，取中间值 3h。

### 汇总表格

| #                   | 任务名称                 | 维度       | 工时      |
| ------------------- | ------------------------ | ---------- | --------- |
| P1                  | 新增「订单管理」页面     | 页面/路由  | 6h        |
| C1                  | 封装 OrderStatusTag 组件 | 组件       | 1h        |
| A1                  | 对接订单列表接口         | 接口对接   | 2h        |
| S1                  | 扩展 orderStore 模块     | 状态管理   | 1.5h      |
| L1                  | 订单管理模块联调         | 前后端联调 | 3h        |
| **开发 + 自测小计** |                          |            | **10.5h** |
| **联调小计**        |                          |            | **3h**    |
| **总计**            |                          |            | **13.5h** |
```

## 输出

将结果保存至 `$PWD/tasks/<story_id>.md` 后:

- Prompt: "需要基于拆分结果在 TAPD 上创建任务吗?"

## 参考文件

| 文件                                             | 用途                      | 何时读取           |
| ------------------------------------------------ | ------------------------- | ------------------ |
| `scripts/get_story.py`                           | 从 TAPD 拉取需求详情      | Step 1             |
| `references/domain.md`                           | Domain key → 业务模块映射 | Step 2，每次必读   |
| `references/domains/<domain>-reference/SKILL.md` | 领域的项目架构与开发约定  | Step 3，完整读取   |
| `references/effort_rules.md`                     | 工时评估基准规则          | Step 4，每次必读   |
| `references/create_tasks.md`                      | 在 TAPD 创建任务          | 当用户要求创建任务时 |

## 注意事项

- **不要跳过 Step 0**：没有明确的 story_id 就不要开始处理
- **源码优先**：工时依据中必须说明是否找到可复用代码，找到则下调，找不到则注明
- **任务粒度**：单个任务以半天（3.75h）到一天（7.5h）为宜，超过 8h 应考虑拆分
- **接口联调**：接口数量多时可拆分为多个联调任务按模块输出
- **多 domain**：按 domain 分组输出，各自有独立的任务列表、汇总表和总工时
