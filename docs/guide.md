I'm a bit of a skill junkie and have been trying to use the `plugin-dev:` stuff and my own skill building tree to help stay organized/follow best practices building plugins - I know this is fast moving target... I've come to the conclusion that trying to do a "local" folder will cause nothing but pain/wasted effort because of how skills/plugins get cached - I've had much better success publishing my skills to git and syncing across computers using the "marketplace" paradigm. This however is way less documented atm (understandable cause iirc this is like totally new). It also seems like Claude Desktop is lagging a bit here - "Capabilities" only takes standalone skills and there is some tensions maintaining skills that can be used in claude code and Claude Desktop. So I've kind of taken a the approach of periodically using an agent to crawl/infer some things about the evolving json schema and it found this issue which seems relevant to my interests. So for anyone that finds this as well - until "real" schema gets published and things better documented I had muh boy write this up to help people out...

This information might be totally out of date next week (spoilers it was). Welcome to the bleeding edge ya'll!

---

# The Marketplace & Plugin Schema Saga

A chronicle of discoveries about Claude Code plugin distribution, schemas, and the official patterns that emerged from investigating Anthropic's own implementations.

**Last Updated**: 2026-01-13 (synced with official docs at code.claude.com)

## The Schema Mystery

### What the Docs Say

Every official `marketplace.json` file references a schema:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  ...
}
```

### What Actually Exists

**Nothing.** The URL returns 404.

```bash
$ curl -sI https://anthropic.com/claude-code/marketplace.schema.json
HTTP/2 302 → https://www.anthropic.com/claude-code/marketplace.schema.json → 404
```

This is a **known bug**: [GitHub Issue #9686](https://github.com/anthropics/claude-code/issues/9686) (opened October 2025, still open as of January 2026).

### Our Solution

We maintain local schemas inferred from actual usage:

- `schemas/marketplace.schema.json`
- `schemas/plugin.schema.json`

Run `/sync-schemas` to re-analyze official sources and update local schemas.

---

## Distribution Paths

Claude Code plugins can be distributed via two completely different mechanisms.

### Path 1: Marketplace (Claude Code CLI)

For Claude Code (the CLI tool), plugins are distributed via **marketplaces**:

```
marketplace-repo/
├── .claude-plugin/
│   └── marketplace.json    # Lists all plugins
└── plugins/
    ├── plugin-a/
    └── plugin-b/
```

**Installation**: Users add the marketplace, then install individual plugins via `/plugin install <name>@<marketplace>`.

**Key file**: `marketplace.json` in `.claude-plugin/` directory, containing plugin entries with `source` paths.

### Path 2: .skill Files (Claude Desktop)

Claude Desktop (the macOS/Windows app) doesn't support marketplaces. Instead, skills are loaded individually via `.skill` files:

- `.skill` file = zip archive containing a skill directory
- Loaded in Claude Desktop → Preferences → Skills
- Each skill is standalone (no plugin grouping concept)

**Key difference**: Desktop loads individual skills; CLI loads plugins (which contain multiple skills).

---

## Official Marketplace Structure

Analyzed from `~/.claude/plugins/marketplaces/claude-plugins-official/`:

### Root Level

```
claude-plugins-official/
├── .claude-plugin/
│   └── marketplace.json      # The source of truth for plugin discovery
├── plugins/                  # Anthropic-maintained plugins
│   ├── plugin-dev/
│   ├── feature-dev/
│   ├── agent-sdk-dev/
│   └── ...
└── external_plugins/         # Community/partner plugins
    ├── github/
    ├── stripe/
    └── ...
```

### marketplace.json Structure

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "claude-plugins-official",
  "description": "Directory of popular Claude Code extensions...",
  "owner": {
    "name": "Anthropic",
    "email": "support@anthropic.com"
  },
  "metadata": {
    "description": "Brief marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-dev",
      "description": "Comprehensive toolkit for developing Claude Code plugins...",
      "author": { "name": "Anthropic", "email": "support@anthropic.com" },
      "source": "./plugins/plugin-dev",
      "category": "development",
      "homepage": "https://github.com/..."
    }
  ]
}
```

### Root-Level Keys

| Key | Required | Description |
|-----|----------|-------------|
| `$schema` | No | Schema URL (returns 404) |
| `name` | Yes | Marketplace identifier (kebab-case) |
| `owner` | Yes | Owner object with `name` (required), `email` (optional) |
| `plugins` | Yes | Array of plugin entries |
| `metadata.description` | No | Brief marketplace description |
| `metadata.version` | No | Marketplace version |
| `metadata.pluginRoot` | No | Base directory prepended to relative source paths |

### Reserved Marketplace Names

The following names are reserved for official Anthropic use:

- `claude-code-marketplace`
- `claude-code-plugins`
- `claude-plugins-official`
- `anthropic-marketplace`
- `anthropic-plugins`
- `agent-skills`
- `life-sciences`

Names that impersonate official marketplaces (like `official-claude-plugins`) are also blocked.

### Plugin Entry Keys

| Key | Required | Description |
|-----|----------|-------------|
| `name` | Yes | Plugin identifier (kebab-case) |
| `source` | Yes | Relative path or URL object |
| `description` | No | Human-readable description |
| `author` | No | Author object with `name`, `email` |
| `category` | No | One of: development, productivity, testing, database, deployment, design, monitoring, security, learning |
| `homepage` | No | Documentation URL |
| `version` | No | Semver string |
| `tags` | No | Array of strings |
| `strict` | No | Boolean (default: true) - see below |
| `keywords` | No | Tags for discovery |
| `license` | No | SPDX identifier |
| `repository` | No | Source code URL |
| `commands` | No | Custom command paths |
| `agents` | No | Custom agent paths |
| `skills` | No | Custom skill paths |
| `hooks` | No | Hook config or path |
| `mcpServers` | No | MCP config or path |
| `lspServers` | No | LSP config or path |
| `outputStyles` | No | Output style paths |

### Source Field Variants

**Simple path**:

```json
"source": "./plugins/plugin-dev"
```

**GitHub object**:

```json
"source": {
  "source": "github",
  "repo": "owner/plugin-repo"
}
```

**URL object** (for external repos):

```json
"source": {
  "source": "url",
  "url": "https://github.com/org/repo.git"
}
```

---

## The `strict` Field (RESOLVED)

### When Does a Plugin Need plugin.json?

**Answer: It depends on the `strict` field.**

| `strict` Value | Behavior |
|----------------|----------|
| `true` (default) | Plugin source MUST contain `.claude-plugin/plugin.json`. Marketplace entry fields are MERGED with plugin.json |
| `false` | Plugin does NOT need its own `plugin.json`. Marketplace entry defines everything |

### Examples

**strict: true (default)** - Plugin has its own manifest:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "Overwrites plugin.json description"
}
```

The plugin at `./plugins/my-plugin/.claude-plugin/plugin.json` must exist.

**strict: false** - Marketplace defines everything:

```json
{
  "name": "simple-plugin",
  "source": "./plugins/simple-plugin",
  "description": "No plugin.json needed",
  "strict": false,
  "commands": ["./plugins/simple-plugin/commands/"]
}
```

### In Official Marketplace

| Plugin | Has plugin.json? | strict value |
|--------|-----------------|--------------|
| plugin-dev | NO | false (implied) |
| agent-sdk-dev | YES | true (default) |
| feature-dev | YES | true (default) |
| LSP plugins | NO | false (explicit) |
| github (external) | YES | true (default) |

### Our Approach

We include plugin.json for maximum flexibility (standalone distribution, local development).

---

## Plugin Components

### Commands

**Location**: `commands/` directory in plugin root

**Format**: Markdown files with frontmatter

Commands are namespaced: `plugin-name:command-name`

### Agents

**Location**: `agents/` directory in plugin root

**Format**: Markdown files describing agent capabilities

### Skills

**Location**: `skills/` directory in plugin root

**Format**: Directories containing `SKILL.md` files with frontmatter

### Hooks

**Location**: `hooks/hooks.json` in plugin root, or inline in plugin.json

**Hook Events** (as of 2026-01):

| Event | Trigger |
|-------|---------|
| `PreToolUse` | Before tool execution |
| `PostToolUse` | After successful tool execution |
| `PostToolUseFailure` | After failed tool execution |
| `PermissionRequest` | When permission dialog shown |
| `UserPromptSubmit` | When user submits prompt |
| `Notification` | When Claude sends notification |
| `Stop` | When Claude attempts to stop |
| `SubagentStart` | When subagent starts |
| `SubagentStop` | When subagent stops |
| `SessionStart` | At session beginning |
| `SessionEnd` | At session end |
| `PreCompact` | Before context compaction |

**Hook Types**:

| Type | Description |
|------|-------------|
| `command` | Execute shell command/script |
| `prompt` | Evaluate prompt with LLM |
| `agent` | Run agentic verifier with tools |

### MCP Servers

**Location**: `.mcp.json` in plugin root, or inline in plugin.json

### LSP Servers

**Location**: `.lsp.json` in plugin root, or inline in plugin.json

LSP plugins provide code intelligence (go to definition, find references, diagnostics).

### Output Styles

**Location**: `outputStyles/` directory or custom path

Customize Claude's response formatting.

---

## Plugin Caching

**Important**: Plugins are COPIED to a cache directory, not used in-place.

Implications:

- Paths like `../shared-utils` won't work (files not copied)
- Symlinks ARE followed during copying
- Use `${CLAUDE_PLUGIN_ROOT}` for all paths in hooks/MCP configs

---

## Categories

Official categories:

- `development` - Dev tools, language servers, SDKs
- `productivity` - Workflow tools, integrations
- `testing` - Test frameworks, automation
- `database` - Database integrations
- `deployment` - CI/CD, hosting platforms
- `design` - Design tool integrations
- `monitoring` - Error tracking, observability
- `security` - Security tools
- `learning` - Educational content, learning modes

---

## Installation Scopes

| Scope | Settings File | Use Case |
|-------|---------------|----------|
| `user` | `~/.claude/settings.json` | Personal, all projects (default) |
| `project` | `.claude/settings.json` | Team, shared via git |
| `local` | `.claude/settings.local.json` | Personal, project-specific, gitignored |
| `managed` | `managed-settings.json` | Admin-controlled, read-only |

---

## CLI Commands

```bash
# Marketplace management
claude plugin marketplace add owner/repo
claude plugin marketplace add https://gitlab.com/org/repo.git
claude plugin marketplace add ./local-path
claude plugin marketplace list
claude plugin marketplace update marketplace-name
claude plugin marketplace remove marketplace-name

# Plugin management
claude plugin install plugin-name@marketplace-name
claude plugin install plugin-name@marketplace-name --scope project
claude plugin uninstall plugin-name@marketplace-name
claude plugin enable plugin-name@marketplace-name
claude plugin disable plugin-name@marketplace-name
claude plugin update plugin-name@marketplace-name

# Validation
claude plugin validate .
```

---

## Reference Sources

### Documentation (Most Current)

- [Plugins](https://code.claude.com/docs/en/plugins.md) - Creating plugins
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md) - Full technical spec
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md) - Distribution
- [Discover Plugins](https://code.claude.com/docs/en/discover-plugins.md) - Installation

### Local (After Installing Official Marketplace)

```bash
# Marketplace structure
ls ~/.claude/plugins/marketplaces/claude-plugins-official/

# marketplace.json
cat ~/.claude/plugins/marketplaces/claude-plugins-official/.claude-plugin/marketplace.json

# Individual plugins
ls ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/
```

### GitHub

- [anthropics/claude-code](https://github.com/anthropics/claude-code) - Main Claude Code repo
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) - Official plugins

### Known Issues

- [#9686: JSON schema URL doesn't exist](https://github.com/anthropics/claude-code/issues/9686)

---

## Key Takeaways

1. **Schema URLs are broken** - Maintain local schemas, sync from observed patterns
2. **Two distribution paths** - Marketplace (CLI) vs .skill files (Desktop)
3. **`strict` field controls plugin.json requirement** - false = marketplace defines everything
4. **marketplace.json is the source of truth** for plugin discovery
5. **Plugins are cached** - Use `${CLAUDE_PLUGIN_ROOT}`, symlinks work
6. **Reserved names exist** - Don't use official-sounding marketplace names
7. **New hook events** - PostToolUseFailure, SubagentStart
8. **New hook type** - `agent` for agentic verification

---

## Changelog

- **2026-01-13**: Major update - synced with official docs, added `strict` field explanation, new hook events, reserved names, caching behavior
- **2026-01-08**: Initial documentation based on analysis of claude-plugins-official

```