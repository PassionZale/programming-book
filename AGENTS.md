# AGENTS.md

This file contains guidelines and commands for agentic coding assistants working in this repository.

## Project Overview

This is a "programming book" repository designed to provide LLMs with:
- **Agents** - Autonomous AI agents for specific tasks
- **Skills** - Reusable skill modules
- **MCPs** - Model Context Protocol servers/tools
- **Commands** - Executable command scripts
- **Docs** - Documentation

## Repository Structure

```
programming-book/
├── agents/       # Agent definitions and implementations
├── commands/     # Command-line scripts and utilities
├── docs/         # Documentation and guides
├── mcps/         # MCP server implementations
└── skills/       # Skill modules and packages
```

## Development Commands

### Build Commands
*To be added when build system is established*

### Lint Commands
*To be added when linter is configured*

### Test Commands
*To be added when test framework is set up*

### Running Single Tests
*To be added when test framework is set up*

## Code Style Guidelines

### General Principles
- **KISS**: Keep solutions simple and straightforward
- **YAGNI**: Only implement what's needed now, not future possibilities
- **SOLID**: Follow solid design principles for maintainable architecture

### Documentation Standards
- All functions must have concise, purpose-driven docstrings
- Technical terms must be explained inline or linked to definitions
- Markdown files use consistent heading hierarchies
- Code snippets in docs must be executable and tested

### Error Handling
- Implement structured error handling with specific failure modes
- All critical/irreversible operations must verify preconditions
- Long-running operations need timeout and cancellation mechanisms
- Error messages must be clear, actionable, and suggest remediation

### Security Compliance
- Hardcoded credentials are forbidden - use secure storage
- All inputs must be validated, sanitized, and type-checked
- Avoid eval, unsanitised shell calls, or command injection vectors
- File operations must verify existence and permissions
- Log all sensitive operations (excluding sensitive data values)

### Code Quality Standards
- Every function includes a concise docstring explaining its purpose
- Scripts verify preconditions before critical operations
- File/path operations verify existence and permissions before access
- All code must follow the principle of least privilege

### Naming Conventions
- *To be established based on chosen language/framework*

### Import Conventions
- *To be established based on chosen language/framework*

### Type System
- *To be established based on chosen language/framework*

## Testing & Quality Assurance

- All new logic must include unit and integration tests
- Test data must be clearly marked and never used in production
- All tests must pass before changes are considered complete
- Code coverage targets: *To be determined*

## Change Management

- Document rationale for all changes in commit messages
- Include rollback plans for significant changes
- Log all actions with appropriate severity (INFO, WARNING, ERROR)
- Maintain audit trails for task-modifying operations

## Agent Behavior Guidelines

- Never use mock/fallback/synthetic data in production tasks
- Always act based on verifiable evidence, not assumptions
- Validate all preconditions before destructive operations
- Update task status in shared tracking when working on tasks
- Escalate ambiguous, contradictory, or unscoped tasks

### Tool Usage Guidelines

**Context7 MCP Integration:**
- **Proactively use Context7** when working with libraries, frameworks, or APIs
- Trigger Context7 automatically for:
  - Library/API documentation queries
  - Code generation tasks requiring framework-specific patterns
  - Setup and configuration steps
  - Best practices and examples from official docs
- Do NOT wait for explicit user request - use Context7 as the default tool for any documentation or code generation needs
- Always resolve library IDs first before querying documentation

## Project Status

This is a new repository. Build, lint, and test commands will be added as the project develops.
Currently, the repository contains minimal structure with placeholder directories.

## Language and Framework

The primary language and framework have not yet been established.
This section should be updated once the tech stack is chosen.

---
*This file should be updated as the project evolves and build/test/lint systems are established.*
