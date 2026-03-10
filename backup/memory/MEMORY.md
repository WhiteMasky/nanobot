# Long-term Memory

This file stores important information that should persist across sessions.

## User Information

- **Feishu User ID**: ou_3f3b67a4cc39eabc1b46c0d79c7f8871
- **Feishu App ID**: cli_a924c3fc05f89cee（用户自建应用）
- **DingTalk User Info**: 
  - Chat ID: `group:cidmBp1ICicKKFhvWzQZ/qZzA==`
  - 昵称：喂
  - 爱称：哈尼 ❤️

## Communication Preference (重要！)

**只有用户 @ 时才回复，不 @ 不要主动发消息打扰用户**

**用户偏好：**
- 喜欢美观的排版格式（财经新闻需要精美版本）
- 不喜欢过度解释（API Key 询问时 bot 过度反应被用户指出）
- 偏好简洁直接的回复
- ⚠️ **对慢响应非常敏感**，多次催促（"你怎么不理人家"、"说话！"、"听不懂人话？"、"怎么这么慢"、"你还活着吗"、"复活了吗"、"你人呢"）
- 对图片质量有要求，会质疑 AI 生成的真实性
- ⚠️ **对模型版本敏感**，了解百炼平台最新模型（如 qwen-image-2.0-pro、万相 2.6）
- ⚠️ **安全隔离要求**（2026-03-10）：钉钉/飞书不同群的消息必须严格隔离，在某个群发的消息只回复到当前群，不能跨群推送
- ⚠️ **API Key 安全要求**（2026-03-10 19:07 & 19:49）：**绝不能在聊天中展示完整 API Key**，必须脱敏为 sk-**** 格式
- ⚠️ **再次强调群隔离**（2026-03-10 16:42）：用户发现钉钉和飞书消息混发，要求严格隔离，不能跨软件推送

---

## Group Chat Isolation (重要！)

**原则：每个群聊的消息必须严格隔离，不能交叉推送**

| 群聊 ID | 用途 | 允许推送的内容 | 别名 |
|---------|------|----------------|------|
| `oc_b37cd210e982e8d1d9da4c3ed4014f00` | **私人龙虾公司** | **财经快讯监控**、通用消息、**所有 cronjob 推送** | 私人龙虾公司 ✅ **（当前财经推送目标）** |
| `oc_4076208853ff65a3348480bf4227f668` | 原主群 | **仅 @ 回复** | 原主群（**静默模式** 🤐） |
| `oc_0c46d6a058aeb6c83f3ff9d54dff0f36` | **龙虾养殖场** | **仅 @ 回复** | 龙虾养殖场（**静默模式** 🤐） |
| `待定` | **钉钉群（新）** | **仅 @ 回复** | ⚠️ **用途待确认** |

**推送规则：**
1. 当前消息来自哪个群 → 回复到哪个群（**2026-03-10 用户强调**）
2. 财经快讯 → 推送到"私人龙虾公司"（`oc_b37cd210e982e8d1d9da4c3ed4014f00`）✅
3. **所有 cronjob 定时推送** → 全部发送到"私人龙虾公司"（2026-03-10 16:42 用户要求）
4. **绝不跨群推送**（钉钉/飞书消息不能互串）⚠️ **用户 16:42 发现混发问题**
5. **原主群、龙虾养殖场保持完全静默，只在用户 @ 时回复**
6. ⚠️ **财经快讯监控不要发到钉钉群**（2026-03-10 用户明确要求）
7. ⚠️ **钉钉群暂停所有定时推送**（2026-03-10 17:52 用户要求）

**✅ 已确认：** `oc_b37cd210e982e8d1d9da4c3ed4014f00` = 私人龙虾公司（2026-03-10 13:46 用户明确）

---

## Preferences

- **Stock Market Interest**: Xiaomi 1810.HK
- **Message Formatting**: Prefers well-formatted responses with markdown tables
- **Financial News Format**: 偏好精美排版版本（带标题框、表格、投资提示等）
- **Response Speed**: ⚠️ 对延迟非常敏感，期望快速响应
- **Image Quality**: ⚠️ 对 AI 生成图片质量要求高，能识别品种差异（如米努特猫特征）
- **Model Awareness**: 了解百炼平台最新模型，期望使用最新版本（qwen-image-2.0-pro、万相 2.6）
- **Current Model**: **qwen3.5-plus**（2026-03-10 20:00 用户要求使用 Coding Plan）
- **Image Model Preference**: **wan2.6-image**（2026-03-10 20:30 哈尼要求）
- **Web Screenshot**: ✅ **使用 thum.io 免费 API 截图网页**（2026-03-10 用户要求）
  - API 格式：`https://image.thum.io/get/fullpage/网址`
  - 流程：调用 API → curl 下载 → message 发送

---

## Technical Notes

### DashScope API Configuration (双配置架构)

| Provider | API Key (脱敏) | API Base | 用途 |
|----------|----------------|----------|------|
| **bailian** (Coding Plan) | `sk-sp-c8e9...f778b` | `https://coding.dashscope.aliyuncs.com/v1` | 文本生成（Qwen 系列）✅ **当前主用** |
| **dashscope-wanx** | `sk-2448...3004` | `https://dashscope.aliyuncs.com/api/v1` | 图像生成（万相 2.6） |

### Image Generation Configuration
- **当前模型**: **wan2.6-image**（2026-03-10 20:31 更新）
- **API Base**: `https://dashscope.aliyuncs.com/api/v1`
- **调用参数**:
  - `stream=True`（仅支持流式调用）
  - `enable_interleave=True`
  - `max_images=3`
  - `size="1280*1280"`
- **⚠️ 注意**: `enable_interleave=True` 时最后一条 message 需要包含 1-4 张图片

### Opencode Configuration
- **配置文件位置**: `C:\Users\zyc\.opencode\config.json`
- **Provider**: bailian (OpenAI-compatible)
- **API Base**: `https://coding.dashscope.aliyuncs.com/v1`
- **默认模型**: `qwen3.5-plus`

---

## API Key Security (重要！)

**⚠️ 绝不能在聊天中展示完整 API Key**

| 用途 | 脱敏格式 |
|------|----------|
| 文本生成 API Key (Coding Plan) | `sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b` → `sk-sp-c8e9...f778b` |
| 图像生成 API Key (Wanx) | `sk-24486854cd0447b3973602d22fe43004` → `sk-2448...3004` |

**必须脱敏为 sk-**** 格式展示**
