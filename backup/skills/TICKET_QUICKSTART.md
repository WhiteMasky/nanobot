# 🎫 抢票技能快速配置指南

**5 分钟快速上手！**

---

## 📋 准备工作

### 1️⃣ 获取 Cookie（2 分钟）

#### 方法 A: 电脑浏览器（推荐）

1. 打开 [大麦网](https://www.damai.cn) 或 [猫眼](https://www.maoyan.com)
2. 登录你的账号
3. 按 `F12` 打开开发者工具
4. 切换到 **Network** 标签
5. 刷新页面
6. 找到任意 API 请求（通常包含 `mtop` 或 `api`）
7. 点击请求，查看 **Request Headers**
8. 复制 **Cookie** 字段的全部内容

#### 方法 B: 手机 App（需要抓包工具）

1. 安装 Charles 或 Fiddler
2. 配置手机代理
3. 打开票务 App
4. 捕获请求
5. 提取 Cookie

---

## 🚀 第一次使用

### 步骤 1: 找到想看的演出

以周杰伦演唱会为例：
- 打开大麦网
- 找到周杰伦演唱会页面
- 选择场次（如：北京站）
- 选择票档（如：¥2880）

### 步骤 2: 获取场次 ID 和 SKU ID

1. 按 `F12` 打开开发者工具
2. 点击"立即购买"或"选座购买"
3. 在 Network 标签找到 API 请求
4. 查看请求参数：
   ```
   itemId: 738982      ← 这是场次 ID
   skuId: 123456789    ← 这是 SKU ID
   ```

### 步骤 3: 运行抢票脚本

```bash
# 替换下面的参数为你的实际信息
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --buyer-name "你的姓名" \
  --buyer-phone "你的手机号" \
  --buyer-id "你的身份证号" \
  --interval 1 \
  --max-attempts 100
```

### 步骤 4: 等待出票

脚本会显示：
```
[01:25:30] 第 1 次检查... ❌ 无票
[01:25:31] 第 2 次检查... ❌ 无票
[01:25:32] 第 3 次检查... ✅ 有票！
🚀 正在创建订单...

============================================================
✅ 订单创建成功！
============================================================
订单 ID: 1234567890
订单链接：https://order.damai.cn/orderDetail.htm?orderId=1234567890
付款截止：2026-03-10 01:35:00
订单金额：¥2880
============================================================
```

### 步骤 5: 手动付款

1. 复制订单链接
2. 在浏览器打开
3. 完成付款
4. ⚠️ **注意**: 通常只有 5-15 分钟付款时间！

---

## 💡 进阶配置

### 配置飞书通知（可选）

抢票成功时自动通知你：

1. 在飞书群添加机器人
2. 复制 Webhook 地址
3. 运行时添加参数：
   ```bash
   --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
   ```

### 多账号抢票（提高成功率）

```bash
# 账号 1
start python skills/ticket_snatcher.py --session 738982 --sku 123456789 --buyer-name "张三" --buyer-phone "13800138000" --cookies "账号 1 的 Cookie"

# 账号 2
start python skills/ticket_snatcher.py --session 738982 --sku 123456789 --buyer-name "李四" --buyer-phone "13900139000" --cookies "账号 2 的 Cookie"
```

### 只检查余票（测试用）

```bash
python skills/ticket_snatcher.py \
  --platform damai \
  --session 738982 \
  --sku 123456789 \
  --check-only
```

---

## ⚡ 参数速查表

| 参数 | 说明 | 示例 | 必需 |
|------|------|------|------|
| `--platform` | 平台 | `damai` / `maoyan` | 否 (默认 damai) |
| `--session` | 场次 ID | `738982` | ✅ |
| `--sku` | 票档 ID | `123456789` | ✅ |
| `--buyer-name` | 姓名 | `张三` | ✅ |
| `--buyer-phone` | 手机号 | `13800138000` | ✅ |
| `--buyer-id` | 身份证号 | `110101199001011234` | 推荐 |
| `--cookies` | Cookie | `"_m_h5_tk=abc..."` | 推荐 |
| `--interval` | 检查间隔 | `1` (秒) | 否 |
| `--max-attempts` | 最大尝试 | `100` (次) | 否 |
| `--check-only` | 只检查余票 | - | 否 |
| `--webhook` | 飞书通知 | `https://...` | 否 |

---

## 🎯 完整示例

### 周杰伦演唱会抢票

```bash
python skills/ticket_snatcher.py ^
  --platform damai ^
  --session 738982 ^
  --sku 123456789 ^
  --buyer-name "周杰伦" ^
  --buyer-phone "13800138000" ^
  --buyer-id "110101199001011234" ^
  --cookies "_m_h5_tk=abc123; cookie2=def456" ^
  --interval 0.5 ^
  --max-attempts 200 ^
  --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
```

**Windows CMD 注意**: 使用 `^` 换行，或使用单行：

```bash
python skills/ticket_snatcher.py --platform damai --session 738982 --sku 123456789 --buyer-name "周杰伦" --buyer-phone "13800138000" --buyer-id "110101199001011234" --cookies "_m_h5_tk=abc123; cookie2=def456" --interval 0.5 --max-attempts 200
```

---

## 🐛 常见问题

### Q: 提示"无票"怎么办？
**A**: 
- 继续等待，脚本会自动重试
- 增加 `--max-attempts` 参数
- 减小 `--interval` 参数（但不要太快）

### Q: Cookie 无效？
**A**:
- 重新登录票务平台
- 重新复制 Cookie
- 确保 Cookie 格式正确

### Q: 订单创建失败？
**A**:
- 检查票是否已售罄
- 检查购买人信息是否正确
- 检查 Cookie 是否有效

### Q: 如何停止脚本？
**A**: 按 `Ctrl+C`

---

## 📱 手机抢票 vs 脚本抢票

| 对比项 | 手机手动抢 | 脚本抢 |
|--------|-----------|--------|
| 速度 | 慢（需要手动操作） | 快（自动监控） |
| 成功率 | 低 | 高 |
| 便利性 | 需要一直盯着 | 可以离开 |
| 付款 | 自动跳转 | 需要手动 |

**建议**: 脚本监控 + 手动付款 = 最佳组合

---

## ⚠️ 重要提醒

1. **本脚本只生成订单，不自动付款**
2. 订单生成后需要**手动付款**（5-15 分钟内）
3. 请确保购买人信息正确
4. 请遵守票务平台规则
5. 建议先用小号测试

---

## 📞 需要帮助？

1. 查看完整文档：`skills/TICKET_SNATCHER.md`
2. 查看日志：`output/tickets/ticket_log.json`
3. 测试命令：`python skills/ticket_snatcher.py --check-only --session 你的场次 --sku 你的票档`

---

*Good Luck! 🎫 祝你抢票成功！*
