# nanobot Skills Index

This index helps nanobot discover and remember available skills.

**Last Updated:** 2026-03-10

## Quick Reference

When asked "What skills do you have?" or "What can you do?", reference this list:

### 🛡️ Safety & Security (ALWAYS ACTIVE)
- `security` - **CRITICAL** - Safety guidelines, blocked operations, incident response

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

| Skill | Status | Dependencies | Priority |
|-------|--------|--------------|----------|
| **security** | ✅ Always | - | **CRITICAL** |
| api-test | Available | curl | Normal |
| clawhub | Available | - | Normal |
| cron | Available | - | Normal |
| data-analysis | Available | python3 | Normal |
| docker | Optional | docker CLI | Normal |
| github | Optional | gh CLI | Normal |
| memory | Available | - | Normal |
| pdf-tools | Available | python3 | Normal |
| skill-creator | Available | - | Normal |
| summarize | Optional | - | Normal |
| tmux | Optional | tmux | Normal |
| translate | Available | curl | Normal |
| weather | Available | curl | Normal |

## Security Priority

**The `security` skill is ALWAYS ACTIVE:**
- Loaded before any operation
- Referenced when user requests dangerous operations
- Used to block unsafe commands
- Educates users about safety

## How to Use Skills

1. **Auto-discovery**: Skills are loaded automatically by `SkillsLoader`
2. **On-demand**: Agent reads `SKILL.md` when user requests related task
3. **Progressive**: Agent starts with summary, reads full content when needed
4. **Security first**: Check `security` skill before any risky operation

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

# Verify security skill is available
python -c "from nanobot.agent.skills import SkillsLoader; from pathlib import Path; s=SkillsLoader(Path('.')); print('security' in [x['name'] for x in s.list_skills()])"
```

## Safety Checklist

Before any operation, nanobot checks:

- [ ] Is this operation safe?
- [ ] Does it violate security guidelines?
- [ ] Are there blocked command patterns?
- [ ] Is the path within allowed directory?
- [ ] Are API keys handled securely?
- [ ] Is network call using HTTPS?
- [ ] Are timeouts configured?

**If any answer is NO: REFUSE and explain why.**
