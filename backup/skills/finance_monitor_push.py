# -*- coding: utf-8 -*-
"""
财经快讯监控 + 推送
每 30 分钟执行：抓取财联社 -> 匹配关键词 -> 推送飞书群
静默执行，只在有新闻时推送
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import urllib.error
import json
import re
import os
from datetime import datetime

# ============ 配置区域 ============

FEISHU_APP_ID = "cli_a924c3fc05f89cee"
FEISHU_APP_SECRET = "43MXrfLFa7sORlI3aMapEdG0aHVJqZ3E"
FEISHU_GROUP_CHAT_ID = "oc_b37cd210e982e8d1d9da4c3ed4014f00"  # 私人龙虾公司

KEYWORDS = {
    "🤖 AI 大模型": ["MiniMax", "阶跃星辰", "OpenAI", "Anthropic", "Claude", "大模型", "AI", "人工智能", "芯片", "半导体", "激光雷达", "GPU", "NVIDIA", "英伟达", "算力", "智谱", "DeepSeek", "Kimi", "月之暗面", "百川", "通义千问", "文心一言", "讯飞星火", "ChatGPT", "Gemini", "LLM", "Transformer", "推理", "训练", "Agent", "智能体", "多模态", "AIGC", "生成式 AI", "AI 芯片", "TPU", "FPGA", "ASIC", "神经网络", "深度学习", "强化学习", "计算机视觉", "自然语言处理", "语音识别", "机器翻译", "AI 制药", "AI 医疗", "AI 教育", "AI 金融", "AI 法律", "AI 游戏", "AI 绘画", "AI 音乐", "AI 视频", "Sora", "Runway", "Midjourney", "Stable Diffusion"],
    "🔌 AI 产业链": ["光模块", "CPO", "服务器", "数据中心", "液冷", "散热", "PCB", "高速连接", "HBM", "存储芯片", "DRAM", "NAND", "先进封装", "CoWoS", "晶圆", "光刻机", "ASML", "台积电", "中芯国际", "寒武纪", "海光信息", "景嘉微", "AI 手机", "AI PC", "边缘计算", "机器人", "人形机器人", "自动驾驶", "智能驾驶", "工业母机", "数控机床", "传感器", "机器视觉", "伺服系统", "减速器", "控制器", "执行器", "激光雷达", "毫米波雷达", "摄像头", "高精地图", "车规级芯片", "智能座舱", "车联网", "V2X", "5G", "6G", "物联网", "工业互联网", "云计算", "边缘云", "混合云", "私有云", "公有云", "SaaS", "PaaS", "IaaS", "IDC", "CDN", "带宽", "流量", "数据中心", "超算中心", "智算中心"],
    "🏢 公司动态": ["阿里巴巴", "腾讯", "美团", "京东", "拼多多", "字节跳动", "百度", "网易", "快手", "哔哩哔哩", "IPO", "上市", "财报", "营收", "利润", "净利润", "毛利率", "三星", "SK 海力士", "美光", "英特尔", "AMD", "苹果", "华为", "荣耀", "OPPO", "vivo", "联想", "戴尔", "惠普", "微软", "谷歌", "亚马逊", "Meta", "特斯拉", "Netflix", "迪士尼", "沃尔玛", "可口可乐", "百事", "宝洁", "联合利华", "耐克", "阿迪达斯", "LVMH", "爱马仕", "香奈儿", "丰田", "本田", "日产", "大众", "宝马", "奔驰", "保时捷", "法拉利", "通用汽车", "福特", "Stellantis", "现代", "起亚", "比亚迪", "蔚来", "小鹏", "理想", "极氪", "零跑", "哪吒", "问界", "智己", "阿维塔", "腾势", "仰望", "方程豹", "岚图", "深蓝", "埃安", "广汽", "上汽", "一汽", "长安", "长城", "吉利", "奇瑞", "江淮", "北汽", "东风", "重汽", "陕汽", "宇通", "金龙", "中通", "顺丰", "圆通", "申通", "韵达", "中通快递", "京东物流", "菜鸟", "饿了么", "滴滴", "Uber", "Lyft", "Airbnb", "Booking", "Expedia", "携程", "同程", "飞猪", "美团旅行"],
    "🔋 储能能源": ["储能", "电池", "锂电池", "磷酸铁锂", "三元锂", "钠离子电池", "固态电池", "氢能", "燃料电池", "光伏", "太阳能", "风电", "核电", "电网", "特高压", "智能电网", "充电桩", "换电", "宁德时代", "比亚迪", "亿纬锂能", "国轩高科", "阳光电源", "隆基绿能", "通威股份", "TCL 中环", "晶科能源", "晶澳科技", "天合光能", "派能科技", "鹏辉能源", "欣旺达", "孚能科技", "当升科技", "天赐材料", "新宙邦", "恩捷股份", "璞泰来", "杉杉股份", "科达利", "尚太科技", "负极", "正极", "隔膜", "电解液", "锂矿", "碳酸锂", "氢氧化锂", "六氟磷酸锂", "VC", "FEC", "PVDF", "铜箔", "铝箔", "电池壳", "BMS", "EMS", "PCS", "逆变器", "变流器", "变压器", "开关柜", "断路器", "继电器", "接触器", "熔断器", "电抗器", "电容器", "电阻器", "连接器", "线束", "热管理", "温控", "空调", "热泵", "PTC", "液冷板", "冷却液", "导热材料", "绝缘材料", "封装材料", "粘结剂", "分散剂", "溶剂", "添加剂"],
    "🏭 大宗商品": ["金属", "有色金属", "铜", "铝", "锌", "铅", "镍", "锡", "钴", "锂", "镁", "钛", "钨", "钼", "稀土", "黄金", "白银", "铂金", "钯金", "钢铁", "钢材", "铁矿石", "焦炭", "焦煤", "锰", "铬", "钒", "锑", "锗", "镓", "铟", "锆", "铪", "铌", "钽", "铍", "铷", "铯", "锶", "钡", "镉", "铋", "硒", "碲", "碘", "溴", "氟", "氯", "磷", "硫", "钾", "钠", "钙", "硅", "硼", "碳", "石墨", "金刚石", "碳纤维", "复合材料", "合金", "不锈钢", "特种钢", "高温合金", "磁性材料", "催化材料", "电子材料", "化工材料", "塑料", "橡胶", "纤维", "树脂", "涂料", "颜料", "染料", "农药", "化肥", "尿素", "钾肥", "磷肥", "复合肥", "纯碱", "烧碱", "PVC", "PP", "PE", "PS", "ABS", "PC", "PA", "POM", "PBT", "PET", "PTA", "乙二醇", "甲醇", "乙醇", "醋酸", "苯", "甲苯", "二甲苯", "苯乙烯", "丙烯", "乙烯", "丁二烯", "己内酰胺", "己二酸", "己二胺", "尼龙", "氨纶", "涤纶", "锦纶", "腈纶", "粘胶", "棉花", "羊毛", "蚕丝", "麻", "皮革", "木材", "纸浆", "纸张", "包装", "印刷"],
    "🛢️ 能源化工": ["原油", "布伦特", "WTI", "上海国际能源交易中心", "INE", "燃油", "汽油", "柴油", "煤油", "航空煤油", "液化石油气", "LPG", "天然气", "LNG", "CNG", "管道气", "页岩气", "煤层气", "可燃冰", "煤炭", "动力煤", "焦煤", "无烟煤", "褐煤", "焦炭", "兰炭", "半焦", "煤焦油", "沥青", "石脑油", "燃料油", "低硫燃料油", "高硫燃料油", "成品油", "炼油", "炼化", "石化", "化工", "煤化工", "油煤气", "甲醇制烯烃", "MTO", "MTP", "PDH", "乙烯裂解", "丙烯裂解", "芳烃", "PX", "PTA", "聚酯", "化纤", "纺织", "印染", "服装", "家纺", "产业用纺织品", "OPEC", "OPEC+", "沙特阿美", "阿联酋", "科威特", "伊拉克", "伊朗", "委内瑞拉", "尼日利亚", "安哥拉", "阿尔及利亚", "刚果", "赤道几内亚", "加蓬", "俄罗斯", "哈萨克斯坦", "阿塞拜疆", "墨西哥", "巴西", "加拿大", "美国", "页岩油", "油砂", "深海油", "海上钻井", "陆上钻井", "勘探", "开采", "运输", "管道", "油轮", "VLCC", "苏伊士型", "阿芙拉型", "成品油轮", "LNG 船", "LPG 船", " tanker", "freight", "shipping", "BDI", "波罗的海干散货指数", "集装箱", "集运", "航运", "港口", "码头", "物流", "供应链"],
    "📈 美股市场": ["美股", "纳斯达克", "纽交所", "道琼斯", "标普 500", "罗素 2000", "VIX", "恐慌指数", "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "NVDA", "AMD", "INTC", "QCOM", "AVGO", "TXN", "ADI", "MCHP", "MU", "WDC", "STX", "NTAP", "DELL", "HPE", "IBM", "ORCL", "CRM", "ADBE", "NOW", "WDAY", "TEAM", "ZM", "DOCU", "OKTA", "CRWD", "ZS", "NET", "DDOG", "MDB", "SNOW", "PLTR", "PATH", "U", "ESTC", "FROG", "C3AI", "IONQ", "RGTI", "QBTS", "COIN", "MARA", "RIOT", "CLSK", "HUT", "BITF", "TIGR", "FUTU", "UP", "HOOD", "SQ", "PYPL", "V", "MA", "AXP", "SOFI", "ABNB", "UBER", "LYFT", "DASH", "EXPE", "BKNG", "CVNA", "KMX", "高盛", "摩根士丹利", "摩根大通", "花旗", "美银", "富国银行", "贝莱德", "先锋", "桥水", "文艺复兴", "Two Sigma", "Citadel", "Virtu", "Jane Street"],
    "📈 港股市场": ["港股", "恒生指数", "恒生科技", "国企指数", "红筹", "H 股", "港交所", "HKEX", "腾讯控股", "阿里巴巴", "美团", "京东", "网易", "百度", "快手", "哔哩哔哩", "小米集团", "理想汽车", "小鹏汽车", "蔚来", "比亚迪股份", "吉利汽车", "长城汽车", "广汽集团", "上汽集团", "中芯国际", "华虹半导体", "ASMPT", "舜宇光学", "瑞声科技", "高伟电子", "丘钛科技", "联想集团", "联想控股", "中兴通讯", "中国电信", "中国移动", "中国联通", "中国海洋石油", "中国石油股份", "中国石化", "中海油服", "中海油田服务", "中煤能源", "中国神华", "兖矿能源", "紫金矿业", "江西铜业股份", "中国铝业", "中国宏桥", "天山铝业", "云铝股份", "中国黄金国际", "山东黄金", "招金矿业", "紫金黄金", "周大福", "六福集团", "老凤祥", "豫园股份", "港铁公司", "中远海控", "中远海能", "招商局港口", "太古股份", "国泰航空", "中国国航", "南方航空", "东方航空", "华润置地", "龙湖集团", "万科企业", "碧桂园", "融创中国", "世茂集团", "旭辉控股集团", "中国海外发展", "华润万象生活", "碧桂园服务", "保利物业", "招商积余", "新城悦服务", "雅生活服务", "融创服务", "金科服务", "时代邻里", "滨江服务", "星盛商业", "宝龙商业", "华润啤酒", "青岛啤酒股份", "百威亚太", "蒙牛乳业", "伊利股份", "康师傅控股", "统一企业中国", "农夫山泉", "李宁", "安踏体育", "特步国际", "361 度", "中国动向", "宝胜国际", "滔搏", "申洲国际", "晶苑国际", "华利集团", "九兴控股", "百丽国际", "周大生", "老凤祥", "豫园股份", "六福集团", "周生生", "高鑫零售", "永辉超市", "物美商业", "苏宁易购", "国美零售", "京东健康", "阿里健康", "平安好医生", "微医", "医渡科技", "诺辉健康", "启明医疗", "沛嘉医疗", "心通医疗", "微创医疗", "威高股份", "鱼跃医疗", "乐普医疗", "蓝帆医疗", "英科医疗", "振德医疗", "奥美医疗", "稳健医疗", "康德莱", "三鑫医疗", "拱东医疗", "采纳股份", "维力医疗", "海尔生物", "昌红科技", "楚天科技", "东富龙", "新华医疗", "万东医疗", "乐普医疗", "微创医疗", "威高股份", "鱼跃医疗"],
    "📊 期货市场": ["期货", "大宗商品", "集运欧线", "原油", "燃油", "沥青", "液化石油气", "LPG", "天然气", "甲醇", "PTA", "短纤", "苯乙烯", "乙二醇", "塑料", "PP", "PVC", "玻璃", "纯碱", "尿素", "豆粕", "豆油", "棕榈油", "菜籽油", "菜籽粕", "玉米", "玉米淀粉", "生猪", "鸡蛋", "苹果", "红枣", "花生", "白糖", "棉花", "棉纱", "纸浆", "橡胶", "20 号胶", "不锈钢", "热轧卷板", "螺纹钢", "线材", "铁矿石", "焦煤", "焦炭", "动力煤", "硅铁", "锰硅", "碳酸锂", "工业硅", "沪铜", "沪铝", "沪锌", "沪铅", "沪镍", "沪锡", "沪金", "沪银", "氧化铝", "烧碱", "多晶硅", "对二甲苯", "PX", "丁二烯橡胶", "BR", "LME 铜", "LME 铝", "LME 锌", "LME 镍", "LME 铅", "LME 锡", "COMEX 铜", "COMEX 金", "COMEX 银", "NYMEX 原油", "布伦特原油", "WTI 原油", "郑商所", "大商所", "上期所", "能源中心", "INE", "CZCE", "DCE", "SHFE", "CME", "CBOT", "COMEX", "NYMEX", "ICE", "LME", "TOCOM", "SHFE", "广期所", "GFEX"],
    "🌏 宏观经济": ["美联储", "FOMC", "利率", "CPI", "PPI", "核心 CPI", "核心 PCE", "非农", "ADP", "初请失业金", "续请失业金", "降准", "降息", "加息", "缩表", "QE", "QT", "央行", "人民银行", "欧洲央行", "日本央行", "英国央行", "澳洲联储", "加拿大央行", "通胀", "通缩", "滞胀", "GDP", "经济", "财政", "国债", "美债", "中债", "欧债", "日债", "收益率曲线", "倒挂", "中东", "贸易战", "关税", "汇率", "人民币", "美元", "欧元", "日元", "英镑", "澳元", "加元", "瑞郎", "港元", "离岸人民币", "在岸人民币", "USDCNY", "USDCNH", "EURUSD", "GBPUSD", "USDJPY", "外汇储备", "M2", "社融", "信贷", "新增贷款", "社会融资规模", "PMI", "制造业 PMI", "服务业 PMI", "非制造业 PMI", "财新 PMI", "ISM 制造业", "ISM 服务业", "制造业", "服务业", "房地产", "基建", "投资", "固定资产投资", "民间投资", "房地产投资", "制造业投资", "消费", "社会消费品零售", "网上零售", "餐饮", "旅游", "电影", "票房", "零售", "就业", "失业率", "城镇调查失业率", "青年失业率", "工资", "人均可支配收入", "养老金", "医保", "社保", "税收", "财政赤字", "地方政府债", "专项债", "特别国债", "货币政策", "财政政策", "产业政策", "十四五", "五年规划", "碳中和", "碳达峰", "双碳", "新能源", "碳排放", "碳交易", "碳税", "环保", "污染", "减排", "节能", "能效", "ESG", "绿色金融", "可持续发展", "一带一路", "RCEP", "CPTPP", "DEPA", "自贸区", "自贸港", "粤港澳大湾区", "长三角", "京津冀", "成渝经济圈", "长江经济带", "黄河流域", "西部大开发", "东北振兴", "中部崛起", "东部率先", "乡村振兴", "城镇化", "城市化", "户籍改革", "土地改革", "房产税", "遗产税", "资本利得税", "企业所得税", "个人所得税", "增值税", "消费税", "关税", "出口退税", "进口税", "反倾销", "反补贴", "保障措施", "301 调查", "232 调查", "实体清单", "出口管制", "技术封锁", "芯片禁令", "数据安全", "隐私保护", "GDPR", "CCPA", "个人信息保护法", "数据安全法", "网络安全法", "反垄断", "反不正当竞争", "平台经济", "数字经济", "直播电商", "社区团购", "预制菜", "新消费", "国潮", "Z 世代", "银发经济", "单身经济", "宠物经济", "盲盒", "潮玩", "元宇宙", "Web3", "区块链", "比特币", "以太坊", "加密货币", "NFT", "DeFi", "DAO", "稳定币", "央行数字货币", "数字人民币", "e-CNY", "CBDC", "USDT", "USDC", "BUSD", "DAI"]
}

WORKSPACE = r"C:\Users\zyc\.nanobot\workspace"
HISTORY_FILE = os.path.join(WORKSPACE, "finance_news_history.json")
OUTPUT_FILE = os.path.join(WORKSPACE, "finance_news_result.json")

# ============ 飞书 API ============

def get_feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result.get('tenant_access_token')
            return None
    except Exception as e:
        return None

def send_feishu_message(content):
    """发送纯文本消息到飞书群"""
    token = get_feishu_token()
    if not token:
        return False
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = {
        "receive_id": FEISHU_GROUP_CHAT_ID,
        "msg_type": "text",
        "content": json.dumps({
            "text": content
        })
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return True
            return False
    except Exception as e:
        return False

# ============ 监控工具 ============

def load_history():
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"sent_ids": [], "last_check": None}

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def fetch_cls_telegraph():
    """从财联社 API 获取快讯（深度版）"""
    url = "https://www.cls.cn/nodeapi/updateTelegraphList"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.cls.cn/telegraph',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('data') and data['data'].get('roll_data'):
                return parse_cls_api_data(data['data']['roll_data'])
            return []
    except Exception as e:
        return []

def parse_cls_api_data(roll_data):
    """解析财联社 API 数据 - 直接使用 API 返回的完整内容"""
    news_list = []
    for item in roll_data[:50]:  # 增加抓取数量
        # 使用 API 返回的 content 字段（这是最完整的）
        content = item.get('content', '')
        
        # 如果 content 为空，尝试 brief 或 title
        if not content:
            content = item.get('brief', '') or item.get('title', '')
        
        # 清理可能的 HTML 标签
        import re
        content = re.sub(r'<[^>]+>', '', content)
        
        if len(content) > 15:
            news_id = f"cls_{item.get('id', len(news_list))}"
            ctime = item.get('ctime', 0)
            time_str = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S') if ctime else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            article_id = item.get('id', '')
            news_list.append({
                "id": news_id,
                "content": content,
                "source": "财联社",
                "time": time_str,
                "url": f"https://www.cls.cn/detail/{article_id}" if article_id else ""
            })
    return news_list

def match_keywords(content):
    matched = []
    content_lower = content.lower()
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                matched.append(category)
                break
    return list(set(matched))

def format_message(news_list):
    lines = []
    lines.append(f"**📰 财经快讯监控**")
    lines.append(f"_更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
    
    for i, news in enumerate(news_list, 1):
        categories = news.get('categories', [])
        
        if 'AI 大模型' in categories or 'AI 产业链' in categories:
            icon = "🤖"
            priority = "🔴"
        elif '储能能源' in categories:
            icon = "🔋"
            priority = "🟡"
        elif '金属原料' in categories:
            icon = "🏭"
            priority = "🟡"
        elif '公司动态' in categories:
            icon = "🏢"
            priority = "🟡"
        elif '宏观经济' in categories:
            icon = "📊"
            priority = "🟡"
        else:
            icon = "📰"
            priority = "⚪"
        
        content = news.get('content', '')
        
        lines.append(f"{priority} {icon} {i}. {content}\n")
    
    lines.append("💡 监控频率：每 30 分钟")
    
    return "\n".join(lines)

# ============ 主函数 ============

def main():
    # 静默执行，不输出日志
    history = load_history()
    sent_ids = history.get("sent_ids", [])
    
    # 抓取新闻
    cls_news = fetch_cls_telegraph()
    
    # 过滤已推送的
    new_news = [n for n in cls_news if n["id"] not in sent_ids]
    
    # 匹配关键词
    matched_news = []
    for news in new_news:
        categories = match_keywords(news["content"])
        if categories:
            news["categories"] = categories
            matched_news.append(news)
    
    # 有匹配新闻才推送
    if matched_news:
        message = format_message(matched_news)
        
        # 推送到飞书
        success = send_feishu_message(message)
        
        if success:
            # 更新历史
            for news in matched_news:
                sent_ids.append(news["id"])
            history["sent_ids"] = sent_ids[-500:]
            history["last_check"] = datetime.now().isoformat()
            save_history(history)
            
            # 保存结果
            output = {
                "has_news": True,
                "count": len(matched_news),
                "pushed_at": datetime.now().isoformat(),
                "news": matched_news
            }
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
    else:
        # 没有新闻，静默保存结果
        output = {"has_news": False, "count": 0, "checked_at": datetime.now().isoformat()}
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
