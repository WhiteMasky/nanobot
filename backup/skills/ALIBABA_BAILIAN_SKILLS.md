# 阿里云百炼 Skills 配置指南

## 📦 待安装的 Skills

| Skill | 评分 | 用途 | 状态 |
|-------|------|------|------|
| bailian-web-search | 3.382⭐ | 百炼网页搜索 | ⏳ 待安装 |
| bailian-search | 3.188⭐ | 百炼搜索 | ⏳ 待安装 |
| bailian-knowledge-retrieve | 3.262⭐ | 知识库检索 | ⏳ 待安装 |
| qwen-image | 3.471⭐ | 通义万相图片生成 | ⏳ 待安装 |
| qwen-audio | 3.207⭐ | 通义千问音频处理 | ⏳ 待安装 |
| qwen-asr | 3.083⭐ | 语音转文字 (STT) | ⏳ 待安装 |
| qwen-tts | 2.962⭐ | 文字转语音 (TTS) | ⏳ 待安装 |
| qwen3-tts-feishu | 2.043⭐ | 飞书语音集成 | ⏳ 待安装 |
| alibaba-cloud-model-setup | 0.808⭐ | 阿里云模型配置 | ⏳ 待安装 |

---

## 🔑 需要的 API Keys

### 1. 阿里云百炼 API Key

获取方式：
1. 访问 https://bailian.console.aliyun.com/
2. 登录阿里云账号
3. 进入「API-KEY 管理」
4. 创建新的 API Key
5. 复制保存

### 2. 配置位置

将 API Key 填入 `~/.nanobot/config.json`：

```json
{
  "tools": {
    "bailian": {
      "apiKey": "你的百炼 API Key"
    },
    "qwen": {
      "apiKey": "你的百炼 API Key"
    }
  }
}
```

---

## 🚀 安装命令

```bash
# 一个一个安装，每个间隔 2-3 分钟
npx clawhub@latest install bailian-web-search --force
npx clawhub@latest install bailian-search --force
npx clawhub@latest install bailian-knowledge-retrieve --force
npx clawhub@latest install qwen-image --force
npx clawhub@latest install qwen-audio --force
npx clawhub@latest install qwen-asr --force
npx clawhub@latest install qwen-tts --force
npx clawhub@latest install qwen3-tts-feishu --force
npx clawhub@latest install alibaba-cloud-model-setup --force
```

---

## 📝 安装进度

- [ ] bailian-web-search
- [ ] bailian-search
- [ ] bailian-knowledge-retrieve
- [ ] qwen-image
- [ ] qwen-audio
- [ ] qwen-asr
- [ ] qwen-tts
- [ ] qwen3-tts-feishu
- [ ] alibaba-cloud-model-setup

---

## ⚠️ 注意事项

1. **ClawHub 限流**：每次安装间隔至少 2-3 分钟
2. **API Key 配置**：安装完成后需要配置 API Key 才能使用
3. **依赖安装**：部分 skills 可能需要额外的 Python/Node.js 依赖

---

*最后更新：2026-03-09 22:45*
