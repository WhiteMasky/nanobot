# nanobot Skills Index

This index helps nanobot discover and remember available skills.

**Last Updated:** 2026-03-10

## Quick Reference

When asked "What skills do you have?" or "What can you do?", reference this list:

### Development & DevOps
- `docker` - Container management (build, run, deploy)
- `github` - GitHub CLI operations (issues, PRs, CI)
- `tmux` - Terminal multiplexer control
- `api-test` - REST API testing

### Data & Documents
- `data-analysis` - pandas CSV/Excel analysis
- `pdf-tools` - PDF extract, merge, split

### Web & Communication
- `translate` - 100+ language translation
- `weather` - Weather forecasts

### AI & Productivity
- `summarize` - Content summarization
- `memory` - Long-term memory management
- `cron` - Task scheduling
- `skill-creator` - Create new skills
- `clawhub` - Install skills from ClawHub

## Skill Files Location

All skills are in: `nanobot/skills/{skill-name}/SKILL.md`

## Requirements Status

| Skill | Status | Dependencies |
|-------|--------|--------------|
| api-test | Available | curl |
| clawhub | Available | - |
| cron | Available | - |
| data-analysis | Available | python3 |
| docker | Optional | docker CLI |
| github | Optional | gh CLI |
| memory | Available | - |
| pdf-tools | Available | python3 |
| skill-creator | Available | - |
| summarize | Optional | - |
| tmux | Optional | tmux |
| translate | Available | curl |
| weather | Available | curl |

## How to Use Skills

1. **Auto-discovery**: Skills are loaded automatically by `SkillsLoader`
2. **On-demand**: Agent reads `SKILL.md` when user requests related task
3. **Progressive**: Agent starts with summary, reads full content when needed

## Adding New Skills

```bash
mkdir nanobot/skills/my-skill
cat > nanobot/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: "What this skill does"
metadata: {"nanobot":{"emoji":"🚀","requires":{"bins":["python3"]}}}
---

# My Skill

Usage examples...
EOF
```

## Testing Skills

```bash
# List all skills
python -c "from nanobot.agent.skills import SkillsLoader; from pathlib import Path; print([s['name'] for s in SkillsLoader(Path('.')).list_skills()])"

# Test specific skill
python -c "from nanobot.agent.skills import SkillsLoader; from pathlib import Path; print(SkillsLoader(Path('.')).load_skill('translate'))"
```
