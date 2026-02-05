# programming-book

我的编程书, 为 LLMs 提供所需要的 Agents, Skills, MCPs, Commands...

## 初始设置

Clone 仓库后，需要手动创建软链接以启用 Claude Code 功能：

```bash
# 创建 .claude 目录（如果不存在）
mkdir -p .claude

# 创建软链接（注意使用相对路径 ../）
ln -s ../commands .claude/commands
ln -s ../agents .claude/agents
ln -s ../skills .claude/skills
```

**Windows 用户**：如果使用 Git Bash 或 WSL，上述命令同样适用。否则需要使用 `mklink` 创建目录链接。
