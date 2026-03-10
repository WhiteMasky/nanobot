# nanobot Model Configuration Guide

## Coding Plan Subscription - Allowed Models

nanobot is now configured to work with **Coding Plan** subscription. Only the following models are allowed:

| Brand | Model | Capabilities |
|-------|-------|--------------|
| 千问 (Qwen) | `qwen3.5-plus` | Text generation, Deep thinking, Visual understanding |
| | `qwen3-max-2026-01-23` | Text generation, Deep thinking |
| | `qwen3-coder-next` | Text generation |
| | `qwen3-coder-plus` | Text generation |
| 智谱 (Zhipu) | `glm-5` | Text generation, Deep thinking |
| | `glm-4.7` | Text generation, Deep thinking |
| Kimi | `kimi-k2.5` | Text generation, Deep thinking, Visual understanding |
| MiniMax | `minimax-m2.5` | Text generation, Deep thinking |

## Configuration

### Default Model

The default model is set to `qwen3.5-plus` (most capable for coding tasks).

```json
{
  "agents": {
    "defaults": {
      "model": "qwen3.5-plus"
    }
  }
}
```

### Provider Configuration

For Qwen models, configure DashScope (阿里云通义千问):

```json
{
  "providers": {
    "dashscope": {
      "api_key": "sk-your-api-key-here"
    }
  }
}
```

## Model Validation

nanobot will **reject** any model not in the allowed list:

```bash
# Valid models
✅ qwen3.5-plus
✅ dashscope/qwen3.5-plus  # With provider prefix
✅ glm-5
✅ kimi-k2.5

# Invalid models (will be blocked)
❌ claude-opus-4-5
❌ gpt-4-turbo
❌ gemini-pro
```

## Error Message

If an invalid model is configured:

```
Value error: Model 'claude-opus-4-5' is not allowed. 
Allowed models: qwen3.5-plus, qwen3-max-2026-01-23, qwen3-coder-next, 
qwen3-coder-plus, glm-5, glm-4.7, kimi-k2.5, minimax-m2.5. 
Current subscription: Coding Plan
```

## Changing Models

To switch to a different allowed model:

1. Edit `~/.nanobot/config.json`
2. Update the `model` field:
   ```json
   {
     "agents": {
       "defaults": {
         "model": "glm-5"
       }
     }
   }
   ```
3. Restart nanobot: `nanobot gateway`

## API Keys

Get your API keys from:

- **DashScope (Qwen)**: https://dashscope.console.aliyun.com/
- **Zhipu (GLM)**: https://open.bigmodel.cn/
- **Kimi**: https://platform.moonshot.cn/
- **MiniMax**: https://platform.minimaxi.com/

Store them securely in `~/.nanobot/config.json`:

```json
{
  "providers": {
    "dashscope": {
      "api_key": "sk-xxx"
    },
    "zhipu": {
      "api_key": "xxx"
    }
  }
}
```

## Security

- **Never commit** `config.json` to version control
- Set file permissions: `chmod 600 ~/.nanobot/config.json`
- Rotate API keys regularly

## Last Updated

- **Date**: 2026-03-10
- **Subscription**: Coding Plan
- **Models**: 8 allowed
