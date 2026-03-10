# nanobot Skills

This directory contains built-in skills that extend nanobot's capabilities.

## Skill Format

Each skill is a directory containing a `SKILL.md` file with:
- YAML frontmatter (name, description, metadata)
- Markdown instructions for the agent

## Attribution

These skills are adapted from [OpenClaw](https://github.com/openclaw/openclaw)'s skill system.
The skill format and metadata structure follow OpenClaw's conventions to maintain compatibility.

## Available Skills

| Skill | Description | Emoji |
|-------|-------------|-------|
| `github` | Interact with GitHub using the `gh` CLI | 🐙 |
| `weather` | Get weather info using wttr.in and Open-Meteo | 🌤️ |
| `summarize` | Summarize URLs, files, and YouTube videos | 📝 |
| `tmux` | Remote-control tmux sessions | 💻 |
| `clawhub` | Search and install skills from ClawHub registry | 🦞 |
| `skill-creator` | Create new skills | ✨ |
| `cron` | Schedule recurring tasks and reminders | ⏰ |
| `memory` | Long-term memory management | 🧠 |
| `api-test` | Test REST APIs with curl/httpie | 🔌 |
| `translate` | Translate text between 100+ languages | 🌐 |
| `docker` | Manage Docker containers and images | 🐳 |
| `data-analysis` | Analyze CSV/Excel with pandas | 📊 |
| `pdf-tools` | Extract, merge, split PDFs | 📄 |

## Skill Categories

### 🔧 Development Tools
- `github` - GitHub operations
- `docker` - Container management
- `tmux` - Terminal multiplexer
- `api-test` - API testing

### 📊 Data & Analysis
- `data-analysis` - Data analysis with pandas
- `pdf-tools` - PDF manipulation

### 🌐 Web & Communication
- `translate` - Translation services
- `weather` - Weather forecasts

### 🤖 AI & Automation
- `summarize` - Content summarization
- `memory` - Memory management
- `cron` - Task scheduling
- `skill-creator` - Skill creation

## Creating Custom Skills

1. Create a new directory: `mkdir nanobot/skills/my-skill`
2. Add `SKILL.md` with YAML frontmatter
3. Include usage examples and documentation
4. Test with nanobot

Example `SKILL.md`:
```markdown
---
name: my-skill
description: "Description of what this skill does"
metadata: {"nanobot":{"emoji":"🚀","requires":{"bins":["python3"]}}}
---

# My Skill

Instructions and examples...
```