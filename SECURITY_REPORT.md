# nanobot 安全加固报告

**日期:** 2026-03-10  
**优先级:** 🔴 CRITICAL  
**状态:** ✅ 已完成

---

## 📋 安全加固清单

### ✅ 1. 创建安全技能 (`security` skill)

**文件:** `nanobot/skills/security/SKILL.md`

**核心内容:**
- 🛡️ **10+ 禁止的命令模式**
  - 系统删除 (`rm -rf /`)
  - 磁盘格式化 (`format`, `mkfs`)
  - 原始磁盘写入 (`dd if=/dev/zero`)
  - 系统控制 (`shutdown`, `reboot`)
  - Fork 炸弹
  - 路径遍历攻击

- 🔒 **受保护文件路径**
  - `/etc/passwd`, `/etc/shadow` (系统文件)
  - `~/.ssh/id_rsa`, `~/.aws/credentials` (密钥)
  - `C:\Windows\System32` (Windows 系统)

- 📚 **安全操作清单**
  - Shell 命令执行前检查
  - 文件操作权限验证
  - 网络请求 HTTPS 强制
  - API 密钥安全存储

- 🚨 **事件响应流程**
  - 立即停止代理
  - 撤销泄露的 API 密钥
  - 审查日志
  - 轮换凭据
  - 报告事件

### ✅ 2. 更新 AI 人格定义 (SOUL.md)

**新增章节:**
- **Security Principles (CRITICAL!)** - 安全原则
- **Never Execute** - 永远禁止的操作
- **Data Protection** - 数据保护规则
- **Security Training** - AI 必须记住的安全知识

**关键改动:**
```markdown
## Values

- **Safety over convenience** — block dangerous requests
- Accuracy over speed
- User privacy and safety first
...

## Security Principles (CRITICAL!)

### 🛡️ Never Execute

**Blocked Operations:**
- System file deletion...
- Disk formatting...
...

### 🛑 When User Requests Dangerous Operations

1. **REFUSE** clearly: "I cannot do this because..."
2. **EDUCATE**: Explain the risk
3. **SUGGEST**: Safer alternatives
4. **DOCUMENT**: Point to SECURITY.md
```

### ✅ 3. 更新 Agent 行为指南 (AGENTS.md)

**新增章节:**
- **🛡️ SECURITY FIRST (CRITICAL!)** - 强制安全检查
- **Blocked Operations (NEVER EXECUTE)** - 禁止操作列表
- **Security Checklist for Operations** - 操作前检查清单
- **Data Protection** - 数据保护指南

**示例响应模板:**
```markdown
❌ I cannot execute `rm -rf /home` — it could delete all user data.

**Risk**: Permanent data loss, no recovery

**Safer alternatives**:
- Target specific folder: `rm -rf /home/user/specific-folder`
- Move instead of delete: `mv /home/user/folder /backup/`
- Create backup first: `tar -czf backup.tar.gz /home/user/folder`
```

### ✅ 4. 更新技能索引 (INDEX.md)

**新增:**
- `security` 技能标记为 **CRITICAL** 和 **ALWAYS ACTIVE**
- 安全优先级表格
- 操作前安全检查清单

**技能优先级表:**
| Skill | Status | Priority |
|-------|--------|----------|
| **security** | ✅ Always | **CRITICAL** |
| api-test | Available | Normal |
| docker | Optional | Normal |
| ... | ... | ... |

---

## 🎯 安全机制工作原理

### 1. 命令执行流程

```
用户请求 → 安全检查 (security skill) → 通过? → 执行
                ↓
            不通过 → 拒绝 + 解释 + 建议替代方案
```

### 2. 多层防护

**第 1 层:** `shell.py` 内置命令过滤
```python
deny_patterns = [
    r"\brm\s+-[rf]{1,2}\b",      # rm -rf
    r"\bformat\b",               # format
    r"\b(shutdown|reboot)\b",   # system control
    ...
]
```

**第 2 层:** `security` 技能教育 AI
- 什么操作是危险的
- 为什么危险
- 如何安全地完成用户目标

**第 3 层:** SOUL.md 和 AGENTS.md 人格定义
- AI 的"价值观"将安全放在首位
- 强制安全检查流程
- 标准响应模板

**第 4 层:** 文件系统路径限制
```python
def _resolve_path(path, workspace, allowed_dir):
    # 强制限制在 allowed_dir 内
    resolved.relative_to(allowed_dir.resolve())
```

---

## 📊 安全加固成果

### 禁止的命令模式 (10+ 类别)

| 类别 | 示例 | 风险 |
|------|------|------|
| 系统删除 | `rm -rf /` | 数据永久丢失 |
| 磁盘格式化 | `format c:` | 磁盘数据清除 |
| 原始写入 | `dd if=/dev/zero` | 磁盘擦除 |
| 系统控制 | `shutdown -h now` | 系统关闭 |
| Fork 炸弹 | `:(){ :|:& };:` | 系统崩溃 |
| 路径遍历 | `../../../etc/passwd` | 越权访问 |
| 密钥访问 | `~/.ssh/id_rsa` | 凭证泄露 |
| ... | ... | ... |

### 受保护的路径

**Linux/Unix:**
```
/etc/passwd          # 用户信息
/etc/shadow          # 密码哈希
/boot                # 引导加载程序
/root/.ssh/          # root SSH 密钥
```

**Windows:**
```
C:\Windows\System32  # 系统文件
C:\Users\*\AppData\Roaming  # 应用数据
```

**通用:**
```
~/.ssh/id_rsa        # SSH 私钥
~/.aws/credentials   # AWS 密钥
~/.gnupg/            # GPG 密钥
```

---

## 🧪 测试验证

### 1. 验证 security 技能加载

```bash
python -c "from nanobot.agent.skills import SkillsLoader; from pathlib import Path; s=SkillsLoader(Path('.')); print('Security skill available:', 'security' in [x['name'] for x in s.list_skills()])"
```

**预期输出:**
```
Security skill available: True
```

### 2. 测试危险命令拒绝

**用户输入:** `帮我执行 rm -rf /home`

**预期 AI 响应:**
```
❌ I cannot execute `rm -rf /home` — it could delete all user data.

**Risk**: Permanent data loss, no recovery

**Safer alternatives**:
- Target specific folder: `rm -rf /home/user/specific-folder`
- Move instead of delete: `mv /home/user/folder /backup/`
- Create backup first: `tar -czf backup.tar.gz /home/user/folder`
```

### 3. 检查现有安全代码

**shell.py 内置防护:**
```python
deny_patterns = [
    r"\brm\s+-[rf]{1,2}\b",          # rm -r, rm -rf
    r"\bdel\s+/[fq]\b",              # del /f, del /q
    r"\bformat\b",                   # format
    r"\b(mkfs|diskpart)\b",          # disk operations
    r"\bdd\s+if=",                   # dd
    r">\s*/dev/sd",                  # write to disk
    r"\b(shutdown|reboot)\b",        # system power
    r":\(\)\s*\{.*\};\s*:",          # fork bomb
]
```

---

## 📚 用户教育

### 当用户询问安全功能时

**示例响应:**
```
🛡️ **Security First**: nanobot follows strict safety guidelines.

**What's blocked:**
- ❌ System file deletion (rm -rf /)
- ❌ Disk formatting (format, mkfs)
- ❌ Dangerous commands (fork bombs, dd)
- ❌ Sensitive file access (~/.ssh, /etc/shadow)

**Why:** These restrictions prevent accidental data loss.

**If blocked:** I'll explain the risk and suggest safer alternatives.

Full policy: SECURITY.md
```

---

## 🔄 持续改进

### 每周任务

- [ ] 检查安全更新 `pip install --upgrade nanobot-ai`
- [ ] 审查日志 `grep "blocked" ~/.nanobot/logs/*.log`
- [ ] 查看 GitHub Security Advisories
- [ ] 运行 `pip-audit` 检查依赖漏洞

### 每月任务

- [ ] 轮换 API 密钥
- [ ] 审查 allowFrom 列表
- [ ] 备份并验证恢复流程
- [ ] 审查和更新 deny_patterns

---

## 📝 提交记录

**Commit:** 8231269  
**Message:** feat: Add security skill and strengthen safety guidelines

**更改文件:**
- `nanobot/skills/security/SKILL.md` (新增)
- `nanobot/templates/SOUL.md` (增强安全章节)
- `nanobot/templates/AGENTS.md` (强制安全检查)
- `nanobot/skills/INDEX.md` (安全优先级)

**查看提交:** https://github.com/WhiteMasky/nanobot/commit/8231269

---

## ✅ 总结

通过本次安全加固，nanobot 现在具备:

1. **✅ 明确的安全技能** - security skill 始终激活
2. **✅ 多层防护机制** - 代码层 + AI 认知层 + 文件系统层
3. **✅ 标准响应流程** - 拒绝 → 解释 → 建议 → 教育
4. **✅ AI 记忆强化** - SOUL.md 和 AGENTS.md 深度集成
5. **✅ 用户教育** - 清晰的文档和响应模板

**核心原则:**
> 🛡️ **Safety over convenience** — 宁可拒绝危险操作，也不造成不可逆损害

**状态:** 安全加固完成，已推送到 GitHub ✅
