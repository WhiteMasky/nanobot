# Feishu (Lark) Group Chat Configuration Template

This document describes how to configure Feishu group chat IDs for nanobot automated notifications.

## ⚠️ Security Notice

**DO NOT commit actual group IDs to version control!**

- Copy this file to `~/.nanobot/workspace/memory/GROUP_CONFIG.md` for your actual configuration
- Replace placeholder group IDs with your real ones
- This template file should remain generic

## Template Configuration

| Group Name | Group ID | Purpose | Status |
|------------|----------|---------|--------|
| **Main Group** | `oc_xxxxxxxxxxxxxxxxxxxxxxxxxx` | **Primary** - All automated notifications | ✅ Active |
| Secondary Group | `oc_yyyyyyyyyyyyyyyyyyyyyyyyyy` | Normal operations | ⚠️ Isolated |

## Notification Rules

### ✅ Push to **Main Group**

All automated tasks should push to this group:
- ✅ Financial news monitoring
- ✅ AI daily briefings
- ✅ Scheduled reminders
- ✅ Cron job notifications
- ✅ Other automated pushes

### ⚠️ **Secondary Group** Isolation Rules

- Only respond when user @mentions the bot
- Do NOT push any automated content
- Do NOT receive financial news

## Cron Job Configuration

Cron jobs are stored in `~/.nanobot/cron/jobs.json`:

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "xxxxx",
      "name": "Financial News Monitor",
      "payload": {
        "deliver": true,
        "channel": "feishu",
        "to": "oc_xxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  ]
}
```

## Script Configuration

Check script group ID:

```bash
grep "FEISHU_GROUP" ~/.nanobot/workspace/skills/finance_monitor_push.py

# Expected output:
# FEISHU_GROUP_CHAT_ID = "oc_xxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Verification Commands

```bash
# Verify cron job configuration
cat ~/.nanobot/cron/jobs.json | grep '"to"'

# Verify script configuration  
grep "FEISHU_GROUP" ~/.nanobot/workspace/skills/finance_monitor_push.py
```

## Configuration Files

| File | Location | Committed to Git? |
|------|----------|-------------------|
| Template | `docs/FEISHU_GROUP_CONFIG.md` | ✅ Yes |
| Actual Config | `~/.nanobot/workspace/memory/GROUP_CONFIG.md` | ❌ No (gitignored) |
| Cron Jobs | `~/.nanobot/cron/jobs.json` | ❌ No (gitignored) |

## Last Updated

- **Template Version**: 2026-03-10
- **Purpose**: Reference for Feishu group configuration
