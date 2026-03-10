# nanobot 安全隔离配置指南

## 当前安全状态 (2026-03-09)

### ✅ 已启用的安全措施
- [x] 命令执行超时限制 (60s)
- [x] 危险命令自动阻止 (rm -rf, format, dd, shutdown 等)
- [x] API Key 存储在 config.json (不暴露)
- [x] Feishu 渠道已配置

### ✅ 当前配置（用户确认）

```json
// config.json
{
  "tools": {
    "restrictToWorkspace": false  // 用户确认保持宽松
  },
  "channels": {
    "feishu": {
      "allowFrom": ["*"]  // 允许所有飞书用户
    }
  }
}
```

**说明**：用户已确认保持宽松配置，方便多用户协作使用。

#### 3. 输出长度限制 (中优先级)
```json
// config.json
{
  "tools": {
    "exec": {
      "timeout": 60,
      "maxOutputChars": 10000  // 添加输出截断限制
    }
  }
}
```

#### 4. 敏感文件保护 (高优先级)
```bash
# Windows PowerShell
icacls "$env:USERPROFILE\.nanobot\config.json" /grant:r "$($env:USERNAME):(R)"
# 仅当前用户可读
```

---

## 安全隔离检查清单

### 每次启动前检查
- [ ] config.json 文件权限正确
- [ ] 没有 API key 泄露到日志
- [ ] workspace 外文件访问被阻止

### 定期审计 (每月)
- [ ] 检查 allowFrom 用户列表
- [ ] 审查 HISTORY.md 中的敏感操作
- [ ] 更新危险命令黑名单
- [ ] 检查 API key 使用记录

---

## 应急响应

### 如果怀疑安全泄露
1. 立即停止 nanobot 服务
2. 轮换所有 API key
3. 检查 HISTORY.md 异常操作
4. 审查 allowFrom 配置
5. 重置 config.json 权限

### 联系人
- 用户 ID: `ou_3f3b67a4cc39eabc1b46c0d79c7f8871`
- 群聊 ID: `oc_4076208853ff65a3348480bf4227f668`

---

## 参考资料

- [AI Sandbox Security Best Practices](https://blaxel.ai/blog/ai-sandbox)
- [NVIDIA Agentic Workflows Security](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows/)
- [Anthropic Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)

---
*最后更新：2026-03-09*
*下次审计：2026-04-09*
