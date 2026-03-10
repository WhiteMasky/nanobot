# 🎫 抢票技能 (Ticket Snatcher)

**版本**: 1.0  
**创建时间**: 2026-03-10 01:25  
**功能**: 自动监控余票并生成订单（不付款）

---

## ⚠️ 重要说明

1. **本技能仅生成订单，不会自动付款**
2. 订单生成后需要手动付款（通常有 5-15 分钟付款时间）
3. 请确保你有合法的购票资格
4. 请遵守各票务平台的使用条款
5. 建议先测试再正式使用

---

## 🚀 快速开始

### 1️⃣ 获取必要信息

#### 大麦网
- **场次 ID (session_id)**: 演出场次 ID
- **SKU ID (sku_id)**: 票档 ID（如：2880 元档）
- **Cookie**: 登录后的 Cookie

#### 猫眼
- **场次 ID (showId)**: 演出 ID
- **SKU ID (sessionId)**: 场次 ID
- **Cookie**: 登录后的 Cookie

### 2️⃣ 获取 Cookie 方法

#### 浏览器方式
1. 打开票务平台网站并登录
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 刷新页面
5. 找到任意 API 请求
6. 复制 Request Headers 中的 Cookie

#### 手机 App 方式
1. 使用抓包工具（如 Charles、Fiddler）
2. 捕获 App 请求
3. 提取 Cookie

### 3️⃣ 基本使用

```bash
# 大麦网抢票
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --buyer-id "110101199001011234" \
  --interval 1 \
  --max-attempts 100
```

---

## 📋 参数说明

### 平台配置

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--platform` | 否 | 票务平台 | `damai` / `maoyan` |
| `--cookies` | 否 | Cookie 字符串 | 见下方示例 |

### 票务信息

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--session` | ✅ | 场次 ID | `738982` |
| `--sku` | ✅ | SKU ID（票档） | `123456789` |

### 购买人信息

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--buyer-name` | ✅ | 购买人姓名 | `张三` |
| `--buyer-phone` | ✅ | 购买人手机号 | `13800138000` |
| `--buyer-id` | 否 | 身份证号 | `110101199001011234` |
| `--seat-ids` | 否 | 座位 ID（猫眼） | `1,2,3,4` |

### 抢票配置

| 参数 | 必需 | 说明 | 默认值 |
|------|------|------|--------|
| `--interval` | 否 | 检查间隔（秒） | `1` |
| `--max-attempts` | 否 | 最大尝试次数 | `100` |
| `--no-notify` | 否 | 不发送飞书通知 | `False` |

### 其他功能

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--check-only` | 否 | 只检查余票 | - |
| `--order-status` | 否 | 查询订单状态 | `ORDER123456` |
| `--webhook` | 否 | 飞书 Webhook URL | `https://...` |

---

## 💡 使用示例

### 示例 1: 大麦网抢票

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --buyer-id "110101199001011234" \
  --interval 0.5 \
  --max-attempts 200
```

### 示例 2: 带 Cookie 的大麦网抢票

```bash
# Cookie 格式 1: JSON
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --cookies '{"_m_h5_tk":"abc123","cookie2":"def456"}'

# Cookie 格式 2: 分号分隔
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --cookies "_m_h5_tk=abc123; cookie2=def456"
```

### 示例 3: 猫眼抢票（指定座位）

```bash
python skills/ticket_snatcher.py \
  --platform maoyan \
  --session 12345 \
  --sku 67890 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --seat-ids "1001,1002,1003,1004"
```

### 示例 4: 只检查余票

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --check-only
```

输出：
```
============================================================
📊 余票信息
============================================================
有票：✅ 是
余票数量：50
价格：¥2880
============================================================
```

### 示例 5: 查询订单状态

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --order-status "ORDER123456"
```

### 示例 6: 带飞书通知

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK"
```

---

## 🎯 高级用法

### 多账号抢票

创建多个脚本实例，使用不同的 Cookie：

```bash
# 账号 1
start python skills/ticket_snatcher.py --platform damai --session 738982 --sku 123456789 --buyer-name "张三" --buyer-phone "13800138000" --cookies "账号 1 的 Cookie"

# 账号 2
start python skills/ticket_snatcher.py --platform damai --session 738982 --sku 123456789 --buyer-name "李四" --buyer-phone "13900139000" --cookies "账号 2 的 Cookie"
```

### 多场次监控

```bash
# 场次 1
start python skills/ticket_snatcher.py --platform damai --session 738982 --sku 123456789 --buyer-name "张三" --buyer-phone "13800138000"

# 场次 2
start python skills/ticket_snatcher.py --platform damai --session 738983 --sku 123456789 --buyer-name "张三" --buyer-phone "13800138000"
```

### 超快速抢票（慎用）

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --interval 0.1 \
  --max-attempts 500
```

⚠️ **注意**: 过快可能被平台限制

---

## 📊 输出说明

### 成功订单

```
============================================================
✅ 订单创建成功！
============================================================
订单 ID: 1234567890
订单链接：https://order.damai.cn/orderDetail.htm?orderId=1234567890
付款截止：2026-03-10 01:35:00
订单金额：¥2880
============================================================
```

### 无票

```
[01:25:30] 第 1 次检查... ❌ 无票
[01:25:31] 第 2 次检查... ❌ 无票
...
```

### 抢票超时

```
============================================================
⏰ 抢票超时，共尝试 100 次
============================================================
```

---

## 📁 文件说明

### 输出目录
```
output/tickets/
├── ticket_log.json    # 操作日志
└── (未来可能添加订单截图等)
```

### 日志格式
```json
{
  "timestamp": "2026-03-10T01:25:30",
  "action": "order_created",
  "details": {
    "platform": "damai",
    "order_id": "1234567890",
    "session_id": "738982",
    "buyer": "张三"
  }
}
```

---

## 🔧 配置飞书通知

### 1️⃣ 创建飞书机器人
1. 打开飞书群聊
2. 点击右上角设置
3. 添加机器人
4. 选择自定义机器人
5. 复制 Webhook 地址

### 2️⃣ 使用 Webhook

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "张三" \
  --buyer-phone "13800138000" \
  --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
```

### 3️⃣ 或设置环境变量

```bash
set FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx
```

---

## ⚠️ 注意事项

### 1️⃣ 合法使用
- 仅用于个人购票
- 不要用于黄牛倒票
- 遵守平台规则

### 2️⃣ 账号安全
- 妥善保管 Cookie
- 不要频繁请求（可能被限制）
- 建议使用小号测试

### 3️⃣ 付款时间
- 订单生成后通常有 5-15 分钟付款时间
- 超时订单会自动取消
- 请及时手动付款

### 4️⃣ 网络延迟
- 建议使用稳定的网络
- 可以提前测试脚本
- 考虑服务器延迟

### 5️⃣ 平台更新
- 票务平台 API 可能更新
- 如失效请及时反馈
- 可能需要更新脚本

---

## 🐛 常见问题

### Q1: 提示"无票"但官网显示有票？
**A**: 可能是缓存问题，尝试：
- 增加检查间隔
- 更新 Cookie
- 检查 session_id 和 sku_id 是否正确

### Q2: 提示"Cookie 无效"？
**A**: Cookie 可能过期，重新获取：
- 重新登录票务平台
- 重新复制 Cookie
- 检查 Cookie 格式

### Q3: 订单创建失败？
**A**: 可能原因：
- 票已售罄
- Cookie 无效
- 购买人信息错误
- 平台限制

### Q4: 如何同时抢多个场次？
**A**: 运行多个脚本实例：
```bash
start python skills/ticket_snatcher.py --session 场次 1 ...
start python skills/ticket_snatcher.py --session 场次 2 ...
```

### Q5: 如何停止抢票？
**A**: 按 `Ctrl+C` 终止脚本

---

## 📝 获取场次 ID 和 SKU ID

### 大麦网

1. 打开演出页面
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 选择票档
5. 找到 API 请求
6. 查看请求参数：
   - `itemId` = session_id
   - `skuId` = sku_id

### 猫眼

1. 打开演出页面
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 选择座位
5. 找到 API 请求
6. 查看请求参数：
   - `showId` = session_id
   - `sessionId` = sku_id

---

## 🔄 更新日志

### v1.0 (2026-03-10)
- ✅ 支持大麦网
- ✅ 支持猫眼
- ✅ 自动监控余票
- ✅ 自动创建订单
- ✅ 飞书通知
- ✅ 操作日志
- ✅ 订单状态查询

---

## 📞 支持

遇到问题？
1. 检查日志文件：`output/tickets/ticket_log.json`
2. 查看控制台输出
3. 检查 Cookie 是否有效
4. 确认场次 ID 和 SKU ID 正确

---

## ⚖️ 免责声明

1. 本技能仅供学习研究使用
2. 请遵守各票务平台的使用条款
3. 请勿用于非法用途
4. 使用本技能产生的后果由用户自行承担
5. 开发者不对使用结果负责

---

*Happy Snatching! 🎫*
