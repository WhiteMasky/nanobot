# -*- coding: utf-8 -*-
"""
浏览器自动化技能 (Browser Controller)
使用 Selenium 控制浏览器进行自动化操作

功能：
1. 自动打开网页
2. 自动登录
3. 自动点击/填写表单
4. 自动获取 Cookie
5. 自动截图
6. 支持抢票场景
"""

import sys
import os
import time
import json
import argparse
from datetime import datetime
from typing import Optional, Dict, List

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Selenium 导入
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    print("Selenium 模块加载成功")
except ImportError as e:
    print(f"错误：Selenium 未安装，请运行：pip install selenium")
    sys.exit(1)

# WebDriver Manager 导入
try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("WebDriver Manager 模块加载成功")
except ImportError:
    print("警告：webdriver_manager 未安装，可能需要手动配置 ChromeDriver")
    ChromeDriverManager = None

# ============ 配置区域 ============

# 输出目录
OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\browser"

# 截图目录
SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "screenshots")

# 日志文件
LOG_FILE = os.path.join(OUTPUT_DIR, "browser_log.json")

# 默认配置
DEFAULT_CONFIG = {
    'headless': False,  # 是否无头模式
    'window_width': 1920,
    'window_height': 1080,
    'implicit_wait': 10,  # 隐式等待时间（秒）
    'page_load_timeout': 30,  # 页面加载超时（秒）
}

# ============ 工具函数 ============

def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

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

def save_screenshot(driver, filename: str = None):
    """保存截图"""
    ensure_output_dir()
    
    if not filename:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"截图已保存：{filepath}")
    return filepath

# ============ 浏览器控制器 ============

class BrowserController:
    """浏览器控制器"""
    
    def __init__(self, config: dict = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.driver = None
        self.wait = None
        self.logged_in = False
        self.cookies = {}
    
    def start(self, browser: str = 'chrome'):
        """启动浏览器"""
        print(f"\n正在启动 {browser} 浏览器...")
        
        if browser == 'chrome':
            options = Options()
            
            # 配置选项
            if self.config['headless']:
                options.add_argument('--headless')
            
            options.add_argument(f'--window-size={self.config["window_width"]},{self.config["window_height"]}')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # 启动浏览器
            if ChromeDriverManager:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
            
            # 设置等待
            self.driver.implicitly_wait(self.config['implicit_wait'])
            self.driver.set_page_load_timeout(self.config['page_load_timeout'])
            self.wait = WebDriverWait(self.driver, self.config['implicit_wait'])
            
            # 执行 CDP 命令绕过检测
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            
            print("浏览器启动成功！")
            log_action('browser_started', {'browser': browser})
            
            return True
        else:
            print(f"不支持的浏览器：{browser}")
            return False
    
    def quit(self):
        """关闭浏览器"""
        if self.driver:
            print("\n关闭浏览器...")
            self.driver.quit()
            self.driver = None
            self.wait = None
            log_action('browser_closed', {})
    
    def open_url(self, url: str):
        """打开网页"""
        if not self.driver:
            print("错误：浏览器未启动")
            return False
        
        print(f"打开网页：{url}")
        try:
            self.driver.get(url)
            log_action('url_opened', {'url': url})
            return True
        except Exception as e:
            print(f"打开网页失败：{e}")
            return False
    
    def find_element(self, by: str, value: str, wait: bool = True):
        """查找元素"""
        if not self.driver:
            return None
        
        try:
            if wait and self.wait:
                element = self.wait.until(EC.presence_of_element_located((getattr(By, by.upper()), value)))
            else:
                element = self.driver.find_element(getattr(By, by.upper()), value)
            return element
        except TimeoutException:
            print(f"查找元素超时：{by}={value}")
            return None
        except NoSuchElementException:
            print(f"未找到元素：{by}={value}")
            return None
        except Exception as e:
            print(f"查找元素失败：{e}")
            return None
    
    def find_elements(self, by: str, value: str):
        """查找多个元素"""
        if not self.driver:
            return []
        
        try:
            elements = self.driver.find_elements(getattr(By, by.upper()), value)
            return elements
        except Exception as e:
            print(f"查找元素失败：{e}")
            return []
    
    def click(self, by: str, value: str, wait: bool = True):
        """点击元素"""
        element = self.find_element(by, value, wait)
        if element:
            try:
                element.click()
                print(f"点击：{by}={value}")
                log_action('element_clicked', {'by': by, 'value': value})
                return True
            except Exception as e:
                print(f"点击失败：{e}")
                return False
        return False
    
    def input_text(self, by: str, value: str, text: str, clear: bool = True):
        """输入文本"""
        element = self.find_element(by, value)
        if element:
            try:
                if clear:
                    element.clear()
                element.send_keys(text)
                print(f"输入：{by}={value} -> {text[:10]}...")
                log_action('text_input', {'by': by, 'value': value, 'text_length': len(text)})
                return True
            except Exception as e:
                print(f"输入失败：{e}")
                return False
        return False
    
    def get_cookie(self, name: str = None):
        """获取 Cookie"""
        if not self.driver:
            return None
        
        if name:
            cookie = self.driver.get_cookie(name)
            return cookie['value'] if cookie else None
        else:
            cookies = self.driver.get_cookies()
            self.cookies = {c['name']: c['value'] for c in cookies}
            return self.cookies
    
    def set_cookie(self, name: str, value: str, domain: str = None):
        """设置 Cookie"""
        if not self.driver:
            return False
        
        try:
            cookie_dict = {'name': name, 'value': value}
            if domain:
                cookie_dict['domain'] = domain
            self.driver.add_cookie(cookie_dict)
            print(f"设置 Cookie: {name}={value[:10]}...")
            return True
        except Exception as e:
            print(f"设置 Cookie 失败：{e}")
            return False
    
    def login_damai(self, username: str, password: str):
        """大麦网自动登录"""
        print("\n开始大麦网自动登录...")
        
        # 打开登录页面
        self.open_url("https://www.damai.cn")
        time.sleep(2)
        
        # 点击登录按钮
        if self.click('xpath', '//a[contains(text(),"登录")]'):
            time.sleep(2)
            
            # 输入账号密码（根据实际页面调整）
            # 注意：大麦网登录可能使用扫码登录，需要手动处理
            
            print("请手动完成登录...")
            print("提示：大麦网主要使用扫码登录，建议手动登录后获取 Cookie")
            
            # 等待用户手动登录
            for i in range(60):
                time.sleep(1)
                if i % 10 == 0:
                    print(f"等待登录... {60-i}秒")
                
                # 检查是否已登录
                user_element = self.find_element('xpath', '//span[contains(@class,"user-name")]', wait=False)
                if user_element:
                    print("登录成功！")
                    self.logged_in = True
                    self.get_cookie()
                    log_action('login_success', {'platform': 'damai'})
                    return True
            
            print("登录超时")
            return False
        else:
            print("未找到登录按钮，可能已登录")
            self.get_cookie()
            return True
    
    def get_ticket_info(self, url: str):
        """获取票务信息"""
        print(f"\n获取票务信息：{url}")
        
        self.open_url(url)
        time.sleep(3)
        
        # 获取页面标题
        title = self.driver.title
        print(f"页面标题：{title}")
        
        # 获取所有 Cookie
        cookies = self.get_cookie()
        
        # 截图
        screenshot = save_screenshot(self.driver, f"ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        # 尝试获取场次信息
        info = {
            'title': title,
            'url': url,
            'cookies': cookies,
            'screenshot': screenshot,
            'timestamp': datetime.now().isoformat()
        }
        
        log_action('ticket_info_got', info)
        
        return info
    
    def auto_select_ticket(self, session_id: str, sku_id: str):
        """自动选择票务"""
        print(f"\n自动选座：session={session_id}, sku={sku_id}")
        
        # 这里需要根据实际页面结构调整
        # 示例代码：
        
        # 1. 选择票档
        # self.click('xpath', f'//div[@data-sku="{sku_id}"]')
        
        # 2. 点击购买
        # self.click('xpath', '//button[contains(text(),"购买")]')
        
        # 3. 选择座位
        # self.click('xpath', f'//div[@seat-id="{seat_id}"]')
        
        # 4. 提交订单
        # self.click('xpath', '//button[contains(text(),"提交订单")]')
        
        print("自动选座功能需要根据具体页面定制")
        return True

# ============ 抢票专用浏览器 ============

class TicketBrowser(BrowserController):
    """抢票专用浏览器"""
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.platform = None
    
    def setup_for_ticket(self, platform: str = 'damai'):
        """为抢票配置浏览器"""
        self.platform = platform
        
        print(f"\n配置浏览器用于 {platform} 抢票...")
        
        # 启动浏览器
        self.start()
        
        # 打开网站
        if platform == 'damai':
            self.open_url("https://www.damai.cn")
        elif platform == 'maoyan':
            self.open_url("https://www.maoyan.com")
        
        print("浏览器已就绪，请手动登录账号")
        print("登录后按 Enter 继续...")
        input()
        
        # 获取 Cookie
        cookies = self.get_cookie()
        print(f"获取到 {len(cookies)} 个 Cookie")
        
        # 保存 Cookie
        cookie_file = os.path.join(OUTPUT_DIR, f"{platform}_cookies.json")
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"Cookie 已保存：{cookie_file}")
        
        return cookies
    
    def monitor_ticket(self, url: str, interval: int = 1):
        """监控票务"""
        print(f"\n开始监控：{url}")
        print(f"间隔：{interval}秒")
        
        attempt = 0
        while True:
            attempt += 1
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            try:
                self.driver.refresh()
                time.sleep(2)
                
                # 检查是否有票（根据实际页面调整）
                # 这里需要具体的选择器
                
                print(f"[{timestamp}] 第 {attempt} 次检查...")
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"检查失败：{e}")
                time.sleep(interval)

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='浏览器自动化技能')
    
    # 基本配置
    parser.add_argument('--browser', type=str, default='chrome', choices=['chrome'], help='浏览器类型')
    parser.add_argument('--headless', action='store_true', help='无头模式')
    parser.add_argument('--url', type=str, help='要打开的网址')
    
    # 平台配置
    parser.add_argument('--platform', type=str, choices=['damai', 'maoyan'], help='票务平台')
    
    # 登录配置
    parser.add_argument('--login', action='store_true', help='自动登录')
    parser.add_argument('--username', type=str, help='用户名')
    parser.add_argument('--password', type=str, help='密码')
    
    # 票务配置
    parser.add_argument('--ticket-url', type=str, help='票务页面 URL')
    parser.add_argument('--session', type=str, help='场次 ID')
    parser.add_argument('--sku', type=str, help='SKU ID')
    
    # 功能选择
    parser.add_argument('--get-cookies', action='store_true', help='获取 Cookie')
    parser.add_argument('--screenshot', action='store_true', help='截图')
    parser.add_argument('--monitor', action='store_true', help='监控余票')
    parser.add_argument('--interval', type=int, default=1, help='监控间隔（秒）')
    
    # Cookie 文件
    parser.add_argument('--cookie-file', type=str, help='Cookie 文件路径')
    
    args = parser.parse_args()
    
    # 创建浏览器控制器
    config = {'headless': args.headless}
    browser = TicketBrowser(config)
    
    try:
        # 获取 Cookie 模式
        if args.get_cookies:
            if not args.platform:
                print("错误：指定平台 --platform damai/maoyan")
                sys.exit(1)
            
            cookies = browser.setup_for_ticket(args.platform)
            print(f"\n获取到 {len(cookies)} 个 Cookie")
            sys.exit(0)
        
        # 监控模式
        if args.monitor:
            if not args.ticket_url:
                print("错误：指定票务页面 URL --ticket-url")
                sys.exit(1)
            
            # 加载 Cookie
            if args.cookie_file:
                with open(args.cookie_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                browser.start()
                browser.open_url(args.ticket_url)
                for name, value in cookies.items():
                    browser.set_cookie(name, value)
                browser.driver.refresh()
            else:
                browser.start()
                browser.open_url(args.ticket_url)
            
            browser.monitor_ticket(args.ticket_url, args.interval)
            sys.exit(0)
        
        # 普通模式
        if args.url:
            browser.start()
            browser.open_url(args.url)
            
            if args.screenshot:
                save_screenshot(browser.driver)
            
            if args.login and args.username and args.password:
                if args.platform == 'damai':
                    browser.login_damai(args.username, args.password)
            
            print("\n浏览器已打开，按 Enter 关闭...")
            input()
        else:
            print("错误：指定 URL --url https://...")
            print("或使用 --get-cookies 获取 Cookie")
            print("或使用 --monitor 监控余票")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n用户中断")
    finally:
        browser.quit()

if __name__ == '__main__':
    main()
