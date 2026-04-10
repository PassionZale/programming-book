# Domain 映射关系

每个 domain key 对应一个 repomix 打包的 agent skill，以及该 domain 所负责的业务模块。

| Domain Key         | 业务模块                         | 上手指南                                                 |
| ------------------ | -------------------------------- | -------------------------------------------------------- |
| `yos-web`          | 慧帮手PC、慧帮手、慧帮手Plus     | `references/domains/yos-web-reference/SKILL.md`          |
| `yph-customer-web` | 客资H5、商机、客资、商机管理系统 | `references/domains/yph-customer-web-reference/SKILL.md` |

## 使用说明

- 当用户指定 `--domain yos-web` 时，只处理需求文档中属于「慧帮手PC / 慧帮手 / 慧帮手Plus」的部分。
- 当用户未指定 `--domain` 时，根据需求文档内容判断涉及哪些 domain。
- 多个 domain 用逗号分隔：`--domain yos-web,yph-customer-web`，此时合并所有相关需求并分 domain 输出任务。
- 如果需求文档中提到的业务模块无法匹配任何 domain，则跳过匹配。

## Domain 文件说明

### `SKILL.md`

项目 agent skill 知识库，包含：

- 项目架构概览
- 技术栈说明
- 目录结构
- 核心业务模块
- 开发约定
- 常用代码模式
