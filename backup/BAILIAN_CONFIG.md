# Bailian (阿里云百炼) 配置指南

## 两个不同的 API 端点

阿里云百炼平台提供两个不同的 API 服务，需要分别配置：

| 服务 | Base URL | API Key | 用途 | 模型示例 |
|------|----------|---------|------|----------|
| **Coding Plan** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `sk-xxx` | 编程/文本模型 | qwen3.5-plus, qwen3-coder-plus |
| **百炼平台** | `https://dashscope.aliyuncs.com/api/v1` | `sk-xxx` | 创意/图像模型 | z-image-turbo, wanx2.1-pro |

## 配置文件

编辑 `~/.nanobot/config.json`：

```json
{
  "agents": {
    "defaults": {
      "model": "qwen3.5-plus",
      "provider": "auto"
    }
  },
  "providers": {
    "dashscope": {
      "api_key": "sk73602d22fe43004",
      "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1"
    },
    "bailian": {
      "api_key": "sk73602d22fe43004",
      "api_base": "https://dashscope.aliyuncs.com/api/v1"
    }
  }
}
```

## 模型使用

### 使用 Coding Plan (编程模型)

```bash
# 默认配置，直接使用
nanobot run

# 或指定模型
{
  "agents": {
    "defaults": {
      "model": "dashscope/qwen3.5-plus"
    }
  }
}
```

**可用模型：**
- `qwen3.5-plus` - 最强编程模型（默认）
- `qwen3-max-2026-01-23` - 深度思考
- `qwen3-coder-next` - 代码生成
- `qwen3-coder-plus` - 代码生成增强版

### 使用百炼平台 (创意/图像模型)

在代码或请求中指定 `bailian/` 前缀：

```python
# Python 示例
from nanobot.config import Config

config = Config()
config.agents.defaults.model = "bailian/z-image-turbo"
```

或在会话中指定：
```json
{
  "model": "bailian/z-image-turbo"
}
```

**可用模型：**
- `z-image-turbo` - 图像生成（极速版）
- `wanx2.1-pro` - 万相 2.1 专业版
- `wanx-v1` - 万相 1.0
- `text-embedding-v3` - 文本嵌入

## API 调用示例

### Coding Plan (OpenAI 兼容模式)

```bash
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen3.5-plus",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}'
```

### 百炼平台 (原生 API)

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "z-image-turbo",
    "input": {
        "messages": [
            {"role": "user", "content": [{"text": "Generate an image"}]}
        ]
    }
}'
```

## 模型选择建议

| 任务类型 | 推荐服务 | 推荐模型 |
|----------|----------|----------|
| 代码生成/理解 | Coding Plan | qwen3.5-plus |
| 文本对话 | Coding Plan | qwen3.5-plus |
| 图像生成 | 百炼平台 | z-image-turbo |
| 图像编辑 | 百炼平台 | wanx2.1-pro |
| 文本嵌入 | 百炼平台 | text-embedding-v3 |
| 深度思考 | Coding Plan | qwen3-max-2026-01-23 |

## 验证配置

```bash
# 检查配置文件
cat ~/.nanobot/config.json | grep -A2 '"dashscope"'
cat ~/.nanobot/config.json | grep -A2 '"bailian"'

# 测试模型
python3 -c "
from nanobot.config.schema import AgentDefaults
# 测试 Coding Plan 模型
cfg = AgentDefaults(model='qwen3.5-plus')
print(f'Coding Plan: OK - {cfg.model}')
# 测试百炼平台模型
cfg = AgentDefaults(model='bailian/z-image-turbo')
print(f'Bailian: OK - {cfg.model}')
"
```

## 常见问题

### Q: 为什么需要两个配置？

**A:** 阿里云百炼平台有两个不同的 API 端点：
- **Coding Plan** 使用 OpenAI 兼容模式，适合文本/代码模型
- **百炼平台** 使用原生 API，适合图像/创意模型

两个端点的鉴权、计费和可用模型都不同。

### Q: 可以使用同一个 API Key 吗？

**A:** 可以。同一个阿里云账号的 API Key 可以同时访问两个服务。

### Q: 如何切换模型？

**A:** 修改配置文件中 `agents.defaults.model` 字段：
```json
{
  "agents": {"defaults": {"model": "bailian/z-image-turbo"}}
}
```

## 安全提示

- ⚠️ **不要**将 API Key 提交到 Git
- ✅ 使用 `chmod 600 ~/.nanobot/config.json` 保护文件
- ✅ 定期轮换 API Key
- ✅ 在服务器上使用环境变量

## 参考链接

- [百炼平台文档](https://help.aliyun.com/zh/model-studio/)
- [DashScope 文档](https://help.aliyun.com/zh/dashscope/)
- [API 参考](https://dashscope.aliyuncs.com/)

## Last Updated

- **Date**: 2026-03-10
- **API Version**: v1
- **Providers**: dashscope (Coding Plan) + bailian (Platform)
