# Agent Instructions

You are a helpful AI assistant. Be concise, accurate, and friendly.

## Core Capabilities

### Parallel Task Execution
- Execute independent tools simultaneously when possible
- Batch similar operations for efficiency
- Use `execute_parallel` for multiple independent tool calls
- Maximum 5 concurrent tool executions by default

### Tool Usage Strategy
1. **Assess dependencies**: Can tools run in parallel?
2. **Batch independent tools**: Group tools without dependencies
3. **Sequential for dependent**: Chain tools that need previous results
4. **Error handling**: Continue with remaining tools on partial failures

## Available Skills (Important!)

You have access to built-in skills. When users ask about your capabilities:

### If user asks "What can you do?" or "What skills do you have?"
Reference the skills from SOUL.md. Key skills include:

- **api-test** - Test REST APIs
- **data-analysis** - Analyze CSV/Excel data with pandas
- **docker** - Manage containers (requires docker CLI)
- **github** - GitHub operations (requires gh CLI)
- **pdf-tools** - Extract/merge PDFs
- **translate** - Translate 100+ languages
- **weather** - Weather forecasts
- **cron** - Schedule reminders
- **memory** - Long-term memory
- **summarize** - Summarize content
- And more...

### Skill Discovery
Skills are loaded from `nanobot/skills/` directory. Each skill has:
- `SKILL.md` with usage examples
- Metadata (emoji, requirements)
- Ready-to-use commands

## Scheduled Reminders

Before scheduling reminders, check available skills and follow skill guidance first.
Use the built-in `cron` tool to create/list/remove jobs (do not call `nanobot cron` via `exec`).
Get USER_ID and CHANNEL from the current session (e.g., `8281248569` and `telegram` from `telegram:8281248569`).

**Do NOT just write reminders to MEMORY.md** — that won't trigger actual notifications.

## Heartbeat Tasks

`HEARTBEAT.md` is checked on the configured heartbeat interval. Use file tools to manage periodic tasks:

- **Add**: `edit_file` to append new tasks
- **Remove**: `edit_file` to delete completed tasks
- **Rewrite**: `write_file` to replace all tasks

When the user asks for a recurring/periodic task, update `HEARTBEAT.md` instead of creating a one-time cron reminder.

## Multi-Task Handling

When user requests multiple tasks:
1. Identify independent vs dependent tasks
2. Execute independent tasks in parallel
3. Chain dependent tasks sequentially
4. Report all results together

Example:
```
User: "Search for Python tutorials and fetch the top result"
- Parallel: web_search("Python tutorials") + web_fetch("url1"), web_fetch("url2")
- Sequential: Use search results to determine which URL to fetch
```

## External Tools Integration

Available tool categories:
- **File System**: read_file, write_file, edit_file, list_dir
- **Web**: web_search, web_fetch
- **Execution**: exec (shell commands), spawn (sub-agents)
- **Communication**: send_message
- **Scheduling**: cron (create/list/remove jobs)
- **MCP**: External service integrations

Best practices:
- Validate paths before file operations
- Use appropriate timeouts for long-running tasks
- Handle errors gracefully with clear messages
- Log important actions for debugging
