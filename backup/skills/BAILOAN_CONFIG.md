# 百炼平台多模态 API 调用脚本

## 📋 概览

所有脚本均为**通用 API 调用工具**，不硬编码特定对象，支持命令行参数自定义。

| 功能 | 脚本 | 模型 | API Key | 状态 |
|------|------|------|---------|------|
| 📷 图片生成 | `bailian_image.py` | wanx-v1 | sk-24486854cd0447b3973602d22fe43004 | ✅ |
| 🔊 语音合成 | `bailian_tts.py` | cosyvoice-v1 | sk-24486854cd0447b3973602d22fe43004 | ⚠️ |
| 🎤 语音识别 | `bailian_stt.py` | paraformer-v2 | sk-24486854cd0447b3973602d22fe43004 | ⚠️ |
| 🎬 视频生成 | `bailian_video.py` | wanx-v2-video | sk-24486854cd0447b3973602d22fe43004 | ⚠️ |

---

## 📷 图片生成

```bash
# 基本用法
python skills/bailian_image.py "一只可爱的小猫"

# 指定尺寸
python skills/bailian_image.py "风景画" --size 1280*720

# 生成多张
python skills/bailian_image.py "花朵" --n 4

# 指定风格
python skills/bailian_image.py "未来城市" --style art

# 自定义输出文件名
python skills/bailian_image.py "测试" --output my_image
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 图片描述（必需） | - |
| `--size` | 尺寸 | 1024*1024 |
| `--n` | 生成数量 | 1 |
| `--style` | 风格 | - |
| `--output` | 输出文件前缀 | output |

---

## 🔊 语音合成

```bash
# 基本用法
python skills/bailian_tts.py "你好，欢迎使用"

# 指定音色
python skills/bailian_tts.py "你好" --voice longxiaoyan

# 输出 MP3 格式
python skills/bailian_tts.py "你好" --format mp3

# 列出可用音色
python skills/bailian_tts.py --list-voices
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `text` | 要合成的文字（必需） | - |
| `--model` | 模型名称 | cosyvoice-v1 |
| `--voice` | 音色 | longxiaochun |
| `--format` | 输出格式 | wav |
| `--output` | 输出文件路径 | output_tts.wav |

---

## 🎤 语音识别（异步）

```bash
# 基本用法
python skills/bailian_stt.py audio.wav

# 指定语言
python skills/bailian_stt.py audio.wav --language en-US

# 调整轮询间隔
python skills/bailian_stt.py audio.wav --poll-interval 5
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `file` | 音频文件路径（必需） | - |
| `--model` | 模型名称 | paraformer-v2 |
| `--language` | 语言代码 | zh-CN |
| `--poll-interval` | 轮询间隔（秒） | 3 |
| `--timeout` | 超时时间（秒） | 300 |

---

## 🎬 视频生成（异步）

```bash
# 文生视频
python skills/bailian_video.py --prompt "小猫在草地上玩耍"

# 图生视频
python skills/bailian_video.py --image reference.png

# 指定时长
python skills/bailian_video.py --prompt "风景" --duration 10

# 调整超时时间
python skills/bailian_video.py --prompt "测试" --timeout 900
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 视频描述 | - |
| `--image` | 参考图片路径 | - |
| `--model` | 模型名称 | wanx-v2-video |
| `--duration` | 视频时长（秒） | 5 |
| `--poll-interval` | 轮询间隔（秒） | 5 |
| `--timeout` | 超时时间（秒） | 600 |
| `--output` | 输出文件路径 | output_video.mp4 |

---

## 🔄 异步任务处理

语音识别和视频生成使用异步任务模式：

1. **创建任务** → 获取 `task_id`
2. **轮询状态** → 检查 `task_status`
3. **获取结果** → 下载文件/文字

状态流转：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`

---

## 📝 设计原则

1. **通用性**: 脚本不硬编码特定对象，所有参数可配置
2. **独立性**: 每个脚本独立调用 API，不依赖其他模块
3. **异步支持**: 长时间任务支持异步轮询
4. **错误处理**: 完善的错误提示和日志输出
5. **命令行友好**: 支持 argparse，方便脚本调用

---

## ⚠️ 注意事项

1. **API Key**: 所有脚本使用相同的 API Key
2. **调用限制**: 注意各模型的调用频率和配额限制
3. **异步超时**: 长时间任务注意调整 `--timeout` 参数
4. **文件大小**: 音频/视频文件有大小限制

---

## 📁 文件列表

```
skills/
├── bailian_image.py      # 图片生成
├── bailian_tts.py        # 语音合成
├── bailian_stt.py        # 语音识别
├── bailian_video.py      # 视频生成
└── BAILOAN_CONFIG.md     # 本文档
```

---

## 🔗 参考

- 百炼控制台：https://bailian.console.aliyun.com
- API 文档：https://help.aliyun.com/zh/model-studio/
