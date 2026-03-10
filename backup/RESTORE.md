# Nanobot 配置还原指南

## 快速还原

### Windows PowerShell

```powershell
# 1. 复制配置文件到 ~/.nanobot
$nanobotDir = "$env:USERPROFILE\.nanobot"
New-Item -ItemType Directory -Force -Path $nanobotDir | Out-Null
Copy-Item config.json "$nanobotDir\config.json" -Force

# 2. 复制 skills
New-Item -ItemType Directory -Force -Path "$nanobotDir\workspace\skills" | Out-Null
Copy-Item -Recurse skills\* "$nanobotDir\workspace\skills\" -Force

# 3. 复制 markdown 文档
Copy-Item *.md "$nanobotDir\workspace\" -Force -Exclude RESTORE.md

# 4. 复制 memory
New-Item -ItemType Directory -Force -Path "$nanobotDir\workspace\memory" | Out-Null
Copy-Item -Recurse memory\* "$nanobotDir\workspace\memory\" -Force

# 5. 复制 sessions
New-Item -ItemType Directory -Force -Path "$nanobotDir\workspace\sessions" | Out-Null
Copy-Item -Recurse sessions\* "$nanobotDir\workspace\sessions\" -Force

echo "还原完成！运行 'nanobot status' 验证"
```

### Linux / macOS

```bash
# 1. 复制配置文件到 ~/.nanobot
mkdir -p ~/.nanobot
cp config.json ~/.nanobot/config.json

# 2. 复制 skills
mkdir -p ~/.nanobot/workspace/skills
cp -r skills/* ~/.nanobot/workspace/skills/

# 3. 复制 markdown 文档
cp *.md ~/.nanobot/workspace/

# 4. 复制 memory
mkdir -p ~/.nanobot/workspace/memory
cp -r memory/* ~/.nanobot/workspace/memory/

# 5. 复制 sessions
mkdir -p ~/.nanobot/workspace/sessions
cp -r sessions/* ~/.nanobot/workspace/sessions/

echo "还原完成！运行 'nanobot status' 验证"
```

## 验证还原

```bash
# 检查配置
nanobot status

# 测试 agent
nanobot agent -m "你好，测试连接"
```

## 注意事项

1. **API Key 安全**: 配置文件包含 API Key，请确保仓库是私有的
2. **敏感信息**: 如果仓库是公开的，请在使用前删除或替换 API Key
3. **Python 依赖**: 确保已安装 nanobot 和相关依赖:
   ```bash
   pip install nanobot selenium playwright
   playwright install chromium
   ```
