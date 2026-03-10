# -*- coding: utf-8 -*-
"""
抢票技能 (Ticket Snatcher)
自动监控余票并生成订单（不付款）

功能：
1. 监控余票状态
2. 自动下单生成订单
3. 支持多个票务平台
4. 飞书消息通知
5. 支持多账号/多场次

注意：本技能仅生成订单，不自动付款
"""

import urllib.request
import urllib.error
import json
import sys
import os
import time
import argparse
import hashlib
import random
from datetime import datetime
from typing import Optional, Dict, List

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

# 输出目录
OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\tickets"

# 日志文件
LOG_FILE = os.path.join(OUTPUT_DIR, "ticket_log.json")

# 飞书 Webhook (可选，用于通知)
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

# 默认请求头
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json',
}

# ============ 工具函数 ============

def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def log_action(action: str, details: dict):
    """记录操作日志"""
    ensure_output_dir()
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'details': details
    }
    
    # 读取现有日志
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except:
            logs = []
    
    # 添加新日志
    logs.append(log_entry)
    
    # 保存日志（保留最近 100 条）
    logs = logs[-100:]
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def send_feishu_notification(title: str, content: str, webhook: str = None):
    """发送飞书通知"""
    if not webhook and not FEISHU_WEBHOOK:
        return
    
    webhook_url = webhook or FEISHU_WEBHOOK
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": content
                            }
                        ]
                    ]
                }
            }
        }
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"📤 飞书通知已发送")
    except Exception as e:
        print(f"⚠️  飞书通知失败：{e}")

def random_delay(min_ms: int = 100, max_ms: int = 300):
    """随机延迟（模拟人类操作）"""
    delay = random.randint(min_ms, max_ms) / 1000.0
    time.sleep(delay)

# ============ 票务平台接口 ============

class TicketPlatform:
    """票务平台基类"""
    
    def __init__(self, cookies: dict = None):
        self.session = None
        self.cookies = cookies or {}
        self.base_url = ""
    
    def check_stock(self, session_id: str, sku_id: str) -> dict:
        """检查余票"""
        raise NotImplementedError
    
    def create_order(self, session_id: str, sku_id: str, buyer_info: dict) -> dict:
        """创建订单（不付款）"""
        raise NotImplementedError
    
    def get_order_status(self, order_id: str) -> dict:
        """查询订单状态"""
        raise NotImplementedError

class DamaiPlatform(TicketPlatform):
    """大麦网票务平台"""
    
    def __init__(self, cookies: dict = None):
        super().__init__(cookies)
        self.base_url = "https://mtop.damai.cn"
        self.headers = DEFAULT_HEADERS.copy()
        if cookies:
            self.headers['Cookie'] = '; '.join([f"{k}={v}" for k, v in cookies.items()])
    
    def check_stock(self, session_id: str, sku_id: str) -> dict:
        """检查大麦余票"""
        url = f"{self.base_url}/gw/mtop.trade.order.init.h5/4.0/"
        
        params = {
            'data': json.dumps({
                'buyNow': True,
                'exParams': {
                    'itemId': session_id,
                    'skuId': sku_id
                }
            })
        }
        
        try:
            req_url = f"{url}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(req_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('data', {}).get('buyCart'):
                    stock_info = result['data']
                    return {
                        'success': True,
                        'has_stock': True,
                        'price': stock_info.get('price', 'N/A'),
                        'stock_quantity': stock_info.get('stockQuantity', 0),
                        'raw': stock_info
                    }
                else:
                    return {
                        'success': True,
                        'has_stock': False,
                        'message': '无票'
                    }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_order(self, session_id: str, sku_id: str, buyer_info: dict) -> dict:
        """创建大麦订单（不付款）"""
        url = f"{self.base_url}/gw/mtop.trade.order.create.h5/4.0/"
        
        order_data = {
            'buyNow': True,
            'exParams': {
                'itemId': session_id,
                'skuId': sku_id
            },
            'buyerInfo': buyer_info
        }
        
        params = {
            'data': json.dumps(order_data)
        }
        
        try:
            req_url = f"{url}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(req_url, headers=self.headers, method='POST')
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('data', {}).get('orderId'):
                    order_info = result['data']
                    order_id = order_info['orderId']
                    
                    # 记录日志
                    log_action('order_created', {
                        'platform': 'damai',
                        'order_id': order_id,
                        'session_id': session_id,
                        'sku_id': sku_id,
                        'buyer': buyer_info.get('name', 'N/A')
                    })
                    
                    return {
                        'success': True,
                        'order_id': order_id,
                        'order_url': f"https://order.damai.cn/orderDetail.htm?orderId={order_id}",
                        'expire_time': order_info.get('expireTime', 'N/A'),
                        'total_fee': order_info.get('totalFee', 'N/A'),
                        'message': '订单创建成功，请尽快付款！'
                    }
                else:
                    return {
                        'success': False,
                        'message': result.get('ret', ['创建失败'])[0]
                    }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_order_status(self, order_id: str) -> dict:
        """查询大麦订单状态"""
        url = f"{self.base_url}/gw/mtop.trade.order.detail.h5/4.0/"
        
        params = {
            'data': json.dumps({
                'orderId': order_id
            })
        }
        
        try:
            req_url = f"{url}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(req_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('data'):
                    order_info = result['data']
                    return {
                        'success': True,
                        'order_id': order_id,
                        'status': order_info.get('status', 'N/A'),
                        'pay_status': order_info.get('payStatus', 'N/A'),
                        'total_fee': order_info.get('totalFee', 'N/A'),
                        'expire_time': order_info.get('expireTime', 'N/A')
                    }
                else:
                    return {
                        'success': False,
                        'message': '订单不存在'
                    }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class MaoyanPlatform(TicketPlatform):
    """猫眼票务平台"""
    
    def __init__(self, cookies: dict = None):
        super().__init__(cookies)
        self.base_url = "https://ticket.maoyan.com"
        self.headers = DEFAULT_HEADERS.copy()
        if cookies:
            self.headers['Cookie'] = '; '.join([f"{k}={v}" for k, v in cookies.items()])
    
    def check_stock(self, session_id: str, sku_id: str) -> dict:
        """检查猫眼余票"""
        url = f"{self.base_url}/shows/{session_id}/seats"
        
        params = {
            'showId': session_id,
            'sessionId': sku_id
        }
        
        try:
            req_url = f"{url}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(req_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('seats'):
                    seats = result['seats']
                    available = [s for s in seats if s.get('status') == 1]
                    
                    return {
                        'success': True,
                        'has_stock': len(available) > 0,
                        'available_count': len(available),
                        'seats': available[:5]  # 返回前 5 个座位
                    }
                else:
                    return {
                        'success': True,
                        'has_stock': False
                    }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_order(self, session_id: str, sku_id: str, buyer_info: dict) -> dict:
        """创建猫眼订单（不付款）"""
        url = f"{self.base_url}/orders"
        
        order_data = {
            'showId': session_id,
            'sessionId': sku_id,
            'seatIds': buyer_info.get('seat_ids', []),
            'buyer': buyer_info
        }
        
        try:
            data = json.dumps(order_data).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=self.headers, method='POST')
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('orderId'):
                    order_id = result['orderId']
                    
                    log_action('order_created', {
                        'platform': 'maoyan',
                        'order_id': order_id,
                        'session_id': session_id
                    })
                    
                    return {
                        'success': True,
                        'order_id': order_id,
                        'order_url': f"{self.base_url}/order/{order_id}",
                        'expire_time': result.get('expireTime', 'N/A'),
                        'total_fee': result.get('totalPrice', 'N/A'),
                        'message': '订单创建成功，请尽快付款！'
                    }
                else:
                    return {
                        'success': False,
                        'message': result.get('msg', '创建失败')
                    }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# ============ 抢票主逻辑 ============

class TicketSnatcher:
    """抢票器"""
    
    def __init__(self, platform: str = 'damai', cookies: dict = None):
        self.platform_name = platform
        if platform == 'damai':
            self.platform = DamaiPlatform(cookies)
        elif platform == 'maoyan':
            self.platform = MaoyanPlatform(cookies)
        else:
            raise ValueError(f"不支持的平台：{platform}")
        
        self.monitoring = False
        self.orders_created = []
    
    def monitor_and_snatch(self, session_id: str, sku_id: str, buyer_info: dict,
                          interval: int = 1, max_attempts: int = 100,
                          notify: bool = True) -> dict:
        """监控并抢票"""
        print(f"\n{'='*60}")
        print(f"🎫 开始抢票")
        print(f"{'='*60}")
        print(f"平台：{self.platform_name}")
        print(f"场次 ID: {session_id}")
        print(f"SKU ID: {sku_id}")
        print(f"间隔：{interval}秒")
        print(f"最大尝试：{max_attempts}次")
        print(f"{'='*60}\n")
        
        self.monitoring = True
        attempt = 0
        
        while attempt < max_attempts and self.monitoring:
            attempt += 1
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # 检查余票
            print(f"[{timestamp}] 第 {attempt} 次检查...", end=' ')
            stock_result = self.platform.check_stock(session_id, sku_id)
            
            if stock_result.get('success') and stock_result.get('has_stock'):
                print(f"✅ 有票！")
                
                # 创建订单
                print(f"🚀 正在创建订单...")
                random_delay(100, 300)  # 随机延迟
                
                order_result = self.platform.create_order(session_id, sku_id, buyer_info)
                
                if order_result.get('success'):
                    order_id = order_result['order_id']
                    self.orders_created.append(order_id)
                    
                    print(f"\n{'='*60}")
                    print(f"✅ 订单创建成功！")
                    print(f"{'='*60}")
                    print(f"订单 ID: {order_id}")
                    print(f"订单链接：{order_result.get('order_url', 'N/A')}")
                    print(f"付款截止：{order_result.get('expire_time', 'N/A')}")
                    print(f"订单金额：{order_result.get('total_fee', 'N/A')}")
                    print(f"{'='*60}")
                    
                    # 发送通知
                    if notify:
                        send_feishu_notification(
                            "🎫 抢票成功！",
                            f"订单创建成功！\n"
                            f"订单 ID: {order_id}\n"
                            f"平台：{self.platform_name}\n"
                            f"请尽快付款！"
                        )
                    
                    # 记录日志
                    log_action('snatch_success', {
                        'platform': self.platform_name,
                        'order_id': order_id,
                        'session_id': session_id,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    return {
                        'success': True,
                        'order_id': order_id,
                        'order_info': order_result
                    }
                else:
                    print(f"❌ 订单创建失败：{order_result.get('message', '未知错误')}")
                    
                    log_action('order_failed', {
                        'platform': self.platform_name,
                        'session_id': session_id,
                        'error': order_result.get('message', '未知错误')
                    })
            else:
                print(f"❌ 无票")
            
            # 延迟
            if attempt < max_attempts:
                time.sleep(interval)
        
        # 超时
        print(f"\n{'='*60}")
        print(f"⏰ 抢票超时，共尝试 {max_attempts} 次")
        print(f"{'='*60}")
        
        log_action('snatch_timeout', {
            'platform': self.platform_name,
            'session_id': session_id,
            'attempts': max_attempts
        })
        
        return {
            'success': False,
            'message': '抢票超时',
            'attempts': max_attempts
        }
    
    def stop(self):
        """停止监控"""
        self.monitoring = False
        print("\n⏹️  已停止抢票")

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='抢票技能（仅生成订单，不付款）')
    
    # 平台配置
    parser.add_argument('--platform', type=str, choices=['damai', 'maoyan'], default='damai',
                       help='票务平台')
    parser.add_argument('--cookies', type=str, help='Cookie 字符串（JSON 格式或分号分隔）')
    
    # 票务信息
    parser.add_argument('--session', type=str, required=True, help='场次 ID')
    parser.add_argument('--sku', type=str, required=True, help='SKU ID（票档）')
    
    # 购买人信息
    parser.add_argument('--buyer-name', type=str, required=True, help='购买人姓名')
    parser.add_argument('--buyer-phone', type=str, required=True, help='购买人手机号')
    parser.add_argument('--buyer-id', type=str, help='购买人身份证号')
    parser.add_argument('--seat-ids', type=str, help='座位 ID 列表（逗号分隔，猫眼用）')
    
    # 抢票配置
    parser.add_argument('--interval', type=int, default=1, help='检查间隔（秒）')
    parser.add_argument('--max-attempts', type=int, default=100, help='最大尝试次数')
    parser.add_argument('--no-notify', action='store_true', help='不发送飞书通知')
    
    # 其他功能
    parser.add_argument('--check-only', action='store_true', help='只检查余票，不下单')
    parser.add_argument('--order-status', type=str, help='查询订单状态（订单 ID）')
    parser.add_argument('--webhook', type=str, help='飞书 Webhook URL')
    
    args = parser.parse_args()
    
    # 解析 Cookie
    cookies = {}
    if args.cookies:
        try:
            cookies = json.loads(args.cookies)
        except:
            # 尝试分号分隔格式
            for item in args.cookies.split(';'):
                if '=' in item:
                    k, v = item.split('=', 1)
                    cookies[k.strip()] = v.strip()
    
    # 创建抢票器
    try:
        snatcher = TicketSnatcher(args.platform, cookies)
    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        sys.exit(1)
    
    # 查询订单状态
    if args.order_status:
        result = snatcher.platform.get_order_status(args.order_status)
        if result.get('success'):
            print(f"\n{'='*60}")
            print(f"📋 订单状态")
            print(f"{'='*60}")
            for key, value in result.items():
                if key not in ['success', 'raw']:
                    print(f"{key}: {value}")
            print(f"{'='*60}")
        else:
            print(f"❌ 查询失败：{result.get('message', '未知错误')}")
        sys.exit(0)
    
    # 只检查余票
    if args.check_only:
        result = snatcher.platform.check_stock(args.session, args.sku)
        if result.get('success'):
            print(f"\n{'='*60}")
            print(f"📊 余票信息")
            print(f"{'='*60}")
            print(f"有票：{'✅ 是' if result.get('has_stock') else '❌ 否'}")
            if result.get('stock_quantity') is not None:
                print(f"余票数量：{result.get('stock_quantity')}")
            if result.get('available_count') is not None:
                print(f"可用座位：{result.get('available_count')}")
            if result.get('price'):
                print(f"价格：{result.get('price')}")
            print(f"{'='*60}")
        else:
            print(f"❌ 查询失败：{result.get('error', '未知错误')}")
        sys.exit(0)
    
    # 购买人信息
    buyer_info = {
        'name': args.buyer_name,
        'phone': args.buyer_phone,
        'idCard': args.buyer_id or ''
    }
    
    if args.seat_ids:
        buyer_info['seat_ids'] = args.seat_ids.split(',')
    
    # 设置飞书 Webhook
    if args.webhook:
        global FEISHU_WEBHOOK
        FEISHU_WEBHOOK = args.webhook
    
    # 开始抢票
    result = snatcher.monitor_and_snatch(
        session_id=args.session,
        sku_id=args.sku,
        buyer_info=buyer_info,
        interval=args.interval,
        max_attempts=args.max_attempts,
        notify=not args.no_notify
    )
    
    # 退出码
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    main()
