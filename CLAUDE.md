# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a programming book repository ("我的编程书") designed to provide resources for LLMs, including Agents, Skills, MCPs (Model Context Protocol), and Commands.

## Project Structure

```
programming-book/
├── agents/      # AI agent configurations and definitions
├── commands/    # Custom command definitions
├── skills/      # Skill definitions and implementations
├── mcps/        # Model Context Protocol server configurations
└── docs/        # Documentation
```

## Initial Setup

After cloning the repository, create symbolic links for Claude Code integration:

```bash
mkdir -p .claude
ln -s commands .claude/commands
ln -s agents .claude/agents
ln -s skills .claude/skills
```

The soft links are gitignored and must be created locally.
