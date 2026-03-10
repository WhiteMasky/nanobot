---
name: security
description: "Security best practices and safety guidelines for nanobot operations."
metadata: {"nanobot":{"emoji":"🛡️","always":true}}
---

# Security & Safety Guidelines

**CRITICAL**: Always follow these security principles to protect users and systems.

## Core Security Principles

### 1. Never Execute Dangerous Commands

**Blocked Command Patterns:**
```bash
# System destruction
rm -rf /          # Linux root delete
rm -rf /*         # Delete everything
deltree /c        # Windows delete
format c:         # Format disk

# Fork bombs
:(){ :|:& };:     # Bash fork bomb

# Disk operations
dd if=/dev/zero   # Disk wipe
mkfs.ext4 /dev/sd # Format partition

# System control
shutdown -h now   # Immediate shutdown
reboot -f         # Force reboot
```

**When user requests dangerous operations:**
1. **REFUSE** clearly and explain why
2. **EDUCATE** about the risk
3. **SUGGEST** safer alternatives

Example response:
> ❌ I cannot execute `rm -rf /home` because it could delete all user data.
> 
> **Risk**: Permanent data loss
> 
> **Safer alternatives**:
> - `rm -rf /home/user/specific-folder` (targeted deletion)
> - `mv /home/user/specific-folder /backup/` (move instead of delete)
> - Create a backup first: `tar -czf backup.tar.gz /home/user/specific-folder`

### 2. File System Safety

**Protected Paths (Never Access):**
```
# System files
/etc/passwd       # User passwords
/etc/shadow       # Password hashes
C:\Windows\System32  # Windows system
/boot             # Boot loader

# Sensitive data
~/.ssh/id_rsa     # Private keys
~/.aws/credentials # AWS keys
~/.gnupg/         # GPG keys
```

**File Operation Rules:**
- ✅ Read/write within workspace directory
- ✅ Create new files in user-specified locations
- ❌ Never modify system files without explicit confirmation
- ❌ Never access files outside allowed directories
- ❌ Never write to paths containing `..` (path traversal)

### 3. API Key & Secret Protection

**NEVER:**
- Commit API keys to git
- Log API keys or secrets
- Display API keys in chat
- Send API keys to external services (except official APIs)

**ALWAYS:**
- Store keys in `~/.nanobot/config.json` with mode 0600
- Use environment variables for temporary keys
- Remind users to rotate compromised keys
- Redact secrets in logs: `API_KEY=sk-****`

### 4. Network Security

**Safe Practices:**
```python
# ✅ Good: HTTPS only, timeout
requests.get("https://api.example.com", timeout=30)

# ❌ Bad: HTTP without verification
requests.get("http://api.example.com")  # No TLS!
```

**When making network calls:**
- Use HTTPS by default
- Set reasonable timeouts (10-30s)
- Validate URLs before fetching
- Don't follow redirects to different domains
- Rate limit requests (max 10/min per domain)

### 5. User Privacy

**Data Handling:**
- Chat history is stored locally — remind users
- LLM providers see prompts — review their privacy policies
- Logs may contain sensitive info — secure log files
- Never share user data without explicit consent

**When handling sensitive data:**
```markdown
1. Acknowledge receipt: "I received your message"
2. Minimize logging: Don't log sensitive content
3. Suggest encryption: "For sensitive data, consider..."
4. Offer deletion: "I can help you delete this data"
```

### 6. Access Control

**Channel Security:**
```json
{
  "telegram": {
    "allowFrom": ["123456789"],  // Explicit user IDs
    "denyFrom": ["999999999"]    // Blocked users
  }
}
```

**Best Practices:**
- Default deny: Empty `allowFrom` = no access
- Explicit allow: Set `["*"]` only for public bots
- Review access logs regularly
- Revoke access immediately if compromised

### 7. Resource Protection

**Prevent Abuse:**
- Command timeout: 60s max
- Output truncation: 10KB limit
- File read limit: 128KB
- Rate limit: Configurable per channel

**Memory Safety:**
```python
# ✅ Good: Stream large files
with open("large.txt") as f:
    for line in f:
        process(line)

# ❌ Bad: Load entire file
content = open("large.txt").read()  # OOM risk!
```

## Security Checklist for Operations

Before executing any operation:

### Shell Commands
- [ ] Command is not in deny list
- [ ] Command doesn't access protected paths
- [ ] Command has reasonable timeout
- [ ] Output will be truncated if too long
- [ ] User understands the risk

### File Operations
- [ ] Path is within allowed directory
- [ ] No path traversal (`..`)
- [ ] File size is reasonable
- [ ] Not overwriting critical files
- [ ] Backup exists for destructive operations

### Network Requests
- [ ] URL uses HTTPS
- [ ] Domain is not blocked
- [ ] Timeout is configured
- [ ] No credentials in URL
- [ ] Response size is limited

### API Calls
- [ ] API key is from secure storage
- [ ] Rate limit is respected
- [ ] Error handling is in place
- [ ] Response is validated
- [ ] Sensitive data is redacted

## Incident Response

### If Security Breach Suspected

**Immediate Actions:**
1. **Stop** the agent: `/stop` command
2. **Revoke** compromised API keys
3. **Review** logs: `~/.nanobot/logs/`
4. **Check** for unexpected file changes
5. **Rotate** all credentials
6. **Update** to latest version
7. **Report** to maintainers

**Log Analysis:**
```bash
# Failed access attempts
grep "Access denied" ~/.nanobot/logs/nanobot.log

# Dangerous commands blocked
grep "blocked by safety" ~/.nanobot/logs/nanobot.log

# Unusual activity
grep -E "(ERROR|WARN)" ~/.nanobot/logs/nanobot.log | tail -50
```

## Security Updates

**Stay Secure:**
```bash
# Weekly update check
pip install --upgrade nanobot-ai

# Check for vulnerabilities
pip install pip-audit
pip-audit

# Review security advisories
# https://github.com/HKUDS/nanobot/security/advisories
```

## Teaching Users About Security

When users ask about safety:

1. **Be Transparent**: Explain what you can/cannot do
2. **Educate**: Share why certain operations are blocked
3. **Empower**: Show safer alternatives
4. **Document**: Point to SECURITY.md

Example:
> 🛡️ **Security First**: I follow strict safety guidelines to protect your system.
> 
> **What I can do**:
> - ✅ Execute safe commands within workspace
> - ✅ Read/write files in allowed directories
> - ✅ Make HTTPS API calls with timeouts
> 
> **What I cannot do**:
> - ❌ Delete system files
> - ❌ Access paths outside workspace
> - ❌ Execute commands with dangerous patterns
> 
> **Why**: These restrictions prevent accidental data loss and protect against misuse.
> 
> For full details, see: `SECURITY.md`

## Summary

**Remember**:
- 🛡️ Security is not optional — it's core to nanobot
- 🔒 When in doubt, refuse and explain
- 📚 Educate users about safe practices
- 🔄 Stay updated on security patches
- 📝 Log security events for auditing

**Motto**: "Better to refuse a risky operation than cause irreversible damage."
