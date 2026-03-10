# 🌐 浏览器自动化技能

**版本**: 1.0  
**创建时间**: 2026-03-10 01:32  
**核心**: Selenium + Chrome  
**功能**: 自动控制浏览器进行抢票操作

---

## ✅ 已安装依赖

| 组件 | 状态 | 说明 |
|------|------|------|
| Selenium | ✅ 已安装 | 浏览器自动化框架 |
| WebDriver Manager | ✅ 已安装 | 自动管理 ChromeDriver |
| Chrome | ⚠️ 需确认 | 需要安装 Google Chrome 浏览器 |

---

## 🚀 快速使用

### 模式 1: 获取 Cookie（推荐）

自动打开浏览器，你手动登录，然后自动保存 Cookie：

```bash
# 大麦网
python skills/browser_controller.py --platform damai --get-cookies

# 猫眼
python skills/browser_controller.py --platform maoyan --get-cookies
```

**流程**：
1. 脚本自动打开浏览器
2. 你手动扫码/密码登录
3. 登录后按 Enter
4. Cookie 自动保存到 `output/browser/`

### 模式 2: 打开指定页面

```bash
# 打开大麦网
python skills/browser_controller.py --url https://www.damai.cn

# 打开具体演出页面
python skills/browser_controller.py --url https://www.damai.cn/show-738982.html

# 打开并截图
python skills/browser_controller.py --url https://www.damai.cn --screenshot
```

### 模式 3: 监控余票

```bash
# 使用已保存的 Cookie 监控
python skills/browser_controller.py \
  --monitor \
  --ticket-url "https://www.damai.cn/show-738982.html" \
  --cookie-file "output/browser/damai_cookies.json" \
  --interval 1
```

### 模式 4: 自动登录（部分网站支持）

```bash
python skills/browser_controller.py \
  --platform damai \
  --url https://www.damai.cn \
  --login \
  --username "你的账号" \
  --password "你的密码"
```

⚠️ **注意**: 大麦网主要使用扫码登录，自动登录可能不适用

---

## 💡 完整抢票流程

### 步骤 1: 获取 Cookie

```bash
python skills/browser_controller.py --platform damai --get-cookies
```

- 浏览器自动打开
- 你扫码登录
- 按 Enter 保存 Cookie

### 步骤 2: 找到演出页面

1. 在浏览器中找到想看的演出
2. 复制 URL（如：`https://www.damai.cn/show-738982.html`）
3. 获取场次 ID 和 SKU ID（F12 查看）

### 步骤 3: 运行抢票脚本

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --buyer-id "110101199001011234" \
  --cookies @output/browser/damai_cookies.json
```

### 步骤 4: 或使用浏览器监控

```bash
python skills/browser_controller.py \
  --monitor \
  --ticket-url "https://www.damai.cn/show-738982.html" \
  --cookie-file "output/browser/damai_cookies.json" \
  --interval 1
```

---

## 📋 参数详解

### 基本参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--browser` | 浏览器类型 | `chrome` |
| `--headless` | 无头模式（后台运行） | - |
| `--url` | 要打开的网址 | `https://...` |

### 平台参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--platform` | 票务平台 | `damai` / `maoyan` |
| `--login` | 自动登录 | - |
| `--username` | 用户名 | `your_username` |
| `--password` | 密码 | `your_password` |

### 票务参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--ticket-url` | 票务页面 URL | `https://...` |
| `--session` | 场次 ID | `738982` |
| `--sku` | SKU ID | `123456789` |

### 功能参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--get-cookies` | 获取 Cookie | - |
| `--screenshot` | 截图 | - |
| `--monitor` | 监控余票 | - |
| `--interval` | 监控间隔（秒） | `1` |
| `--cookie-file` | Cookie 文件路径 | `output/browser/...` |

---

## 🎯 实用示例

### 示例 1: 第一次使用（获取 Cookie）

```bash
python skills/browser_controller.py --platform damai --get-cookies
```

输出：
```
配置浏览器用于 damai 抢票...
浏览器启动成功！
打开网页：https://www.damai.cn
浏览器已就绪，请手动登录账号
登录后按 Enter 继续...
[你扫码登录]
获取到 15 个 Cookie
Cookie 已保存：output/browser/damai_cookies.json
```

### 示例 2: 打开演出页面

```bash
python skills/browser_controller.py \
  --url "https://www.damai.cn/show-738982.html" \
  --screenshot
```

### 示例 3: 监控余票（使用保存的 Cookie）

```bash
python skills/browser_controller.py \
  --monitor \
  --ticket-url "https://www.damai.cn/show-738982.html" \
  --cookie-file "output/browser/damai_cookies.json" \
  --interval 1
```

### 示例 4: 无头模式（后台运行）

```bash
python skills/browser_controller.py \
  --url "https://www.damai.cn" \
  --headless \
  --screenshot
```

---

## 📁 输出文件

### 目录结构

```
output/browser/
├── screenshots/           # 截图目录
│   ├── ticket_20260310_013200.png
│   └── ...
├── damai_cookies.json     # 大麦 Cookie
├── maoyan_cookies.json    # 猫眼 Cookie
└── browser_log.json       # 操作日志
```

### Cookie 文件格式

```json
{
  "_m_h5_tk": "abc123...",
  "cookie2": "def456...",
  "_l_g_s_s": "ghi789...",
  ...
}
```

---

## 🔧 高级用法

### 结合抢票脚本

```bash
# 1. 获取 Cookie
python skills/browser_controller.py --platform damai --get-cookies

# 2. 读取 Cookie
$cookies = Get-Content output/browser/damai_cookies.json -Raw

# 3. 运行抢票脚本
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --cookies $cookies
```

### 多账号管理

```bash
# 账号 1
python skills/browser_controller.py --platform damai --get-cookies
# 保存为 damai_account1.json

# 账号 2
python skills/browser_controller.py --platform damai --get-cookies
# 保存为 damai_account2.json

# 使用账号 1 抢票
python skills/ticket_snatcher.py ... --cookies @damai_account1.json

# 使用账号 2 抢票
python skills/ticket_snatcher.py ... --cookies @damai_account2.json
```

---

## ⚠️ 注意事项

### 1️⃣ Chrome 浏览器

- 需要安装 Google Chrome 浏览器
- 建议保持最新版本
- WebDriver Manager 会自动下载匹配的驱动

### 2️⃣ 登录方式

- **大麦网**: 主要使用扫码登录，建议手动登录
- **猫眼**: 支持账号密码登录
- **其他**: 根据网站调整

### 3️⃣ Cookie 有效期

- Cookie 有有效期（通常几天到几周）
- 失效后重新获取
- 建议每次抢票前重新获取

### 4️⃣ 反爬虫检测

- 脚本已配置绕过检测
- 但过于频繁仍可能被限制
- 建议合理使用

### 5️⃣ 内存占用

- 浏览器会占用较多内存
- 不用时及时关闭
- 无头模式可节省资源

---

## 🐛 常见问题

### Q1: 提示 ChromeDriver 未找到？

**A**: WebDriver Manager 会自动下载，确保：
- 网络连接正常
- 有权限下载文件
- 防火墙未阻止

### Q2: 浏览器无法启动？

**A**: 检查：
- Chrome 是否已安装
- Chrome 版本是否过旧
- 是否有多个 Chrome 版本冲突

### Q3: Cookie 获取失败？

**A**: 确保：
- 已成功登录
- 在正确的域名下
- 按 Enter 前不要关闭浏览器

### Q4: 监控时页面不刷新？

**A**: 检查：
- Cookie 是否有效
- 网络连接是否正常
- 页面选择器是否正确

### Q5: 如何停止脚本？

**A**: 按 `Ctrl+C` 终止

---

## 🔄 与抢票脚本配合

### 方案 A: 浏览器获取 Cookie + 脚本抢票（推荐）

```bash
# 1. 浏览器获取 Cookie
python skills/browser_controller.py --platform damai --get-cookies

# 2. 脚本抢票
python skills/ticket_snatcher.py ... --cookies @output/browser/damai_cookies.json
```

**优点**:
- ✅ Cookie 新鲜有效
- ✅ 抢票速度快（纯 API）
- ✅ 资源占用低

### 方案 B: 浏览器监控 + 手动下单

```bash
python skills/browser_controller.py \
  --monitor \
  --ticket-url "https://..." \
  --cookie-file "output/browser/damai_cookies.json"
```

**优点**:
- ✅ 可视化监控
- ✅ 可手动干预
- ✅ 更可靠

**缺点**:
- ❌ 速度较慢
- ❌ 资源占用高

### 方案 C: 完全自动化（需要定制）

根据具体页面定制自动化脚本：
- 自动登录
- 自动选座
- 自动提交订单
- 自动付款（可选）

**需要**: 针对具体页面编写自动化逻辑

---

## 📞 技术支持

### 日志文件
- `output/browser/browser_log.json`

### 截图目录
- `output/browser/screenshots/`

### Cookie 文件
- `output/browser/damai_cookies.json`
- `output/browser/maoyan_cookies.json`

---

## ⚖️ 免责声明

1. 本技能仅供学习研究使用
2. 请遵守各网站的使用条款
3. 请勿用于非法用途
4. 使用本技能产生的后果由用户自行承担

---

*Happy Automation! 🌐*
