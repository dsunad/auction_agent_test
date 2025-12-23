# 拍卖信息处理 Agent V2 - 增强版

这是一个智能拍卖信息处理系统的增强版本,不仅能够搜索拍卖场次,还能深入每个拍卖场次获取所有拍品的详细信息,支持关键词过滤和多格式导出。

## 🎯 核心功能

### V1 功能(基础版)

**智能查询处理** - 集成 DeepSeek 大语言模型,理解复杂的自然语言指令,自动提取查询参数并执行搜索。

**多维度搜索** - 支持按时间范围、类别(硬币、纸币、代币等)、关键词、Lots 数量等多个维度进行搜索和过滤。

**多种使用方式** - 提供命令行交互界面、RESTful API 服务和 Python 库三种使用方式。

### V2 新增功能(增强版)

**✨ 深入拍卖场次** - 进入特定拍卖场次,抓取所有拍品的详细信息,包括拍品编号、标题、描述、当前出价、图片等。

**✨ 关键词过滤** - 在拍品标题和描述中搜索特定关键词,快速找到感兴趣的拍品。

**✨ 多格式导出** - 将拍品信息导出为 JSON、CSV 或 TXT 格式,方便后续处理和分析。

**✨ Zyte API 集成** - 使用 Zyte API 绕过 Cloudflare 反爬虫保护,稳定可靠地获取数据。

**✨ 自动分页** - 自动检测和处理分页,获取所有页面的拍品信息。

**✨ 组合操作** - 一键完成"搜索拍卖 -> 获取拍品 -> 关键词过滤 -> 导出文件"的完整流程。

## 🚀 快速开始

### 安装依赖

```bash
cd auction_agent
pip3 install -r requirements.txt
```

### 使用增强版命令行界面

```bash
python3 cli_v2.py
```
git config --global user.email "dsunad@connect.ust.hk"


然后输入自然语言指令,例如:

```
获取这个拍卖的所有拍品:
https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475
```

```
搜索包含 "silver" 的拍品并导出到 silver_lots.json
```

```
找出所有硬币拍卖,获取包含 "Morgan Dollar" 的拍品,保存为 CSV
```

### 在 Python 代码中使用

```python
from agent_v2 import AuctionAgentV2

# 创建 Agent 实例
agent = AuctionAgentV2()

# 示例 1: 获取特定拍卖的所有拍品
auction_url = "https://auctions.stacksbowers.com/auctions/3-1NZHVT/..."
lots = agent.get_lots_from_auction(auction_url)
print(f"找到 {len(lots)} 个拍品")

# 示例 2: 获取拍品并按关键词过滤
lots = agent.get_lots_from_auction(
    auction_url,
    keywords=["silver", "dollar"]
)

# 示例 3: 组合操作 - 搜索、获取、过滤、导出
result = agent.search_and_export_lots(
    auction_criteria={
        "time_range_days": 7,
        "categories": ["U.S. Coins & Related"]
    },
    lot_keywords=["silver", "dollar"],
    output_file="silver_dollars.json",
    output_format="json"
)
```

## 📁 项目结构

```
auction_agent/
├── config.py              # 配置文件(包含 API 密钥)
├── agent.py               # Agent 核心逻辑(V1)
├── agent_v2.py            # Agent 核心逻辑(V2 增强版)
├── scraper.py             # 拍卖场次抓取模块
├── lot_scraper.py         # 拍品抓取模块(新增)
├── data_fetcher.py        # 实时数据获取
├── cli.py                 # 命令行界面(V1)
├── cli_v2.py              # 命令行界面(V2 增强版)
├── api_server.py          # Web API 服务
├── test_agent.py          # 测试脚本
├── test_lot_scraper.py    # 拍品抓取测试(新增)
├── example_usage.py       # 使用示例
├── requirements.txt       # Python 依赖
├── README.md              # 基础文档
├── README_V2.md           # 增强版文档(本文件)
├── ENHANCED_FEATURES.md   # 增强功能详细说明(新增)
└── API_GUIDE.md           # API 使用指南
```

## 💡 使用示例

### 示例 1: 获取特定拍卖的所有拍品

**自然语言方式**:
```
您: 获取这个拍卖的所有拍品信息:
https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475
```

**Python 代码方式**:
```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()
lots = agent.get_lots_from_auction(
    "https://auctions.stacksbowers.com/auctions/3-1NZHVT/...",
    max_pages=20
)

print(f"找到 {len(lots)} 个拍品")
for lot in lots[:5]:  # 显示前 5 个
    print(f"- {lot.get('title')}")
```

### 示例 2: 按关键词过滤并导出

**自然语言方式**:
```
您: 搜索包含 "silver" 的拍品并导出到 silver_lots.csv
```

**Python 代码方式**:
```python
from agent_v2 import AuctionAgentV2
from lot_scraper import LotScraper

agent = AuctionAgentV2()
scraper = LotScraper()

# 获取拍品
lots = agent.get_lots_from_auction(
    "https://auctions.stacksbowers.com/auctions/3-1NZHVT/...",
    keywords=["silver"]
)

# 导出到 CSV
scraper.save_lots_to_file(lots, "silver_lots.csv", "csv")
print(f"已导出 {len(lots)} 个拍品到 silver_lots.csv")
```

### 示例 3: 完整工作流

**自然语言方式**:
```
您: 找出所有硬币拍卖,获取包含 "Morgan Dollar" 的拍品,保存为 JSON
```

**Python 代码方式**:
```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# 一键完成所有操作
result = agent.search_and_export_lots(
    auction_criteria={
        "time_range_days": 30,
        "categories": ["U.S. Coins & Related", "World Coins"]
    },
    lot_keywords=["Morgan", "Dollar"],
    output_file="morgan_dollars.json",
    output_format="json"
)

print(f"从 {result['auctions_count']} 个拍卖中")
print(f"导出了 {result['lots_count']} 个拍品")
print(f"保存到 {result['output_file']}")
```

## 📊 数据格式

### 拍品信息结构

```json
{
  "lot_number": "70001",
  "title": "1919 General John J. Pershing Portrait Plaque",
  "description": "Uniface. By Allen G. Newman, Cast by John Polachek. Bronze and Iron. Extremely Fine.",
  "current_bid": "40",
  "image_url": "https://...",
  "grade": "Extremely Fine",
  "grading_service": "PCGS",
  "auction_title": "December 2025 Collectors Choice Online Auction",
  "auction_date": "2025-12-05",
  "auction_url": "https://..."
}
```

### 导出格式

**JSON**: 结构化数据,适合程序处理
```json
[
  {"lot_number": "70001", "title": "...", ...},
  {"lot_number": "70002", "title": "...", ...}
]
```

**CSV**: 表格格式,可用 Excel 打开
```csv
lot_number,title,description,current_bid
70001,1919 General John J. Pershing Portrait Plaque,Bronze and Iron...,40
70002,Admiral Dewey Medal Bronze,MS-64 BN (PCGS),320
```

**TXT**: 纯文本格式,易读
```
============================================================
拍品 #1
============================================================
lot_number: 70001
title: 1919 General John J. Pershing Portrait Plaque
...
```

## 🔧 技术架构

### 核心组件

| 组件 | 功能 | 技术 |
|------|------|------|
| Agent V2 | 自然语言理解和决策 | DeepSeek LLM, Function Calling |
| LotScraper | 拍品抓取和解析 | Zyte API, BeautifulSoup |
| 数据导出 | 多格式文件生成 | JSON, CSV, TXT |
| API 服务 | RESTful API | FastAPI, Uvicorn |

### 关键技术

**Zyte API**: 专业的网页抓取服务,能够绕过 Cloudflare 等反爬虫机制,提供稳定可靠的数据获取能力。

**智能解析**: 使用多种策略解析拍品信息,包括 HTML 解析、JSON 提取、正则匹配等,确保数据准确性。

**函数调用**: 使用 DeepSeek 的 Function Calling 功能,Agent 能够根据用户意图自动选择和执行合适的工具。

## 🎓 实际应用场景

### 场景 1: 收藏家监控特定拍品

**需求**: 我想找出所有即将拍卖的 Morgan Silver Dollar 硬币

**解决方案**:
```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()
result = agent.search_and_export_lots(
    auction_criteria={
        "time_range_days": 7,
        "categories": ["U.S. Coins & Related"]
    },
    lot_keywords=["Morgan", "Silver Dollar"],
    output_file="morgan_silver_dollars.csv",
    output_format="csv"
)
```

### 场景 2: 市场研究和价格分析

**需求**: 我想分析最近一个月所有硬币拍卖的价格分布

**解决方案**:
```python
from agent_v2 import AuctionAgentV2
import pandas as pd

# 导出数据
agent = AuctionAgentV2()
result = agent.search_and_export_lots(
    auction_criteria={
        "time_range_days": 30,
        "categories": ["U.S. Coins & Related", "World Coins"]
    },
    output_file="all_coins.csv",
    output_format="csv"
)

# 使用 pandas 分析
df = pd.read_csv("all_coins.csv")
print(df['current_bid'].describe())
# 进行更多数据分析...
```

### 场景 3: 批量数据收集

**需求**: 我想收集某个特定拍卖的所有拍品信息,建立本地数据库

**解决方案**:
```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()
lots = agent.get_lots_from_auction(
    "https://auctions.stacksbowers.com/auctions/3-1NZHVT/...",
    max_pages=100  # 获取最多 100 页
)

# 保存为多种格式
from lot_scraper import LotScraper
scraper = LotScraper()
scraper.save_lots_to_file(lots, "auction_data.json", "json")
scraper.save_lots_to_file(lots, "auction_data.csv", "csv")
```

## 📝 API 密钥配置

所有 API 密钥已在 `config.py` 中配置:

- **DeepSeek API**: 用于自然语言理解和决策
- **Tavily API**: 用于辅助信息搜索
- **Zyte API**: 用于高级网页抓取(新增)

如需修改,请编辑 `config.py` 文件。

## ⚠️ 注意事项

### 使用限制

1. **API 配额**: Zyte API 有使用配额限制,请合理使用
2. **请求频率**: 建议控制请求频率,避免对目标网站造成负担
3. **数据准确性**: 抓取的数据依赖于网站结构,可能需要调整解析逻辑

### 最佳实践

1. **测试先行**: 先在小范围测试(max_pages=1),确认数据正确后再大规模抓取
2. **定期更新**: 网站结构可能变化,需要定期检查和更新解析逻辑
3. **数据备份**: 重要数据建议多格式保存
4. **遵守规则**: 遵守网站的 robots.txt 和服务条款

## 🔍 故障排除

### 问题 1: 无法获取拍品

**可能原因**: Zyte API 配额用尽、网站结构变化、网络连接问题

**解决方法**:
- 检查 Zyte API 配额
- 查看日志文件 `auction_agent.log`
- 尝试手动访问 URL 确认网站是否可访问

### 问题 2: 拍品信息不完整

**可能原因**: 网站使用动态加载、解析逻辑需要调整

**解决方法**:
- 检查返回的 HTML 内容
- 调整 `lot_scraper.py` 中的解析逻辑
- 增加 `max_pages` 参数确保获取所有页面

### 问题 3: 导出文件为空

**可能原因**: 没有找到符合条件的拍品、关键词过滤太严格

**解决方法**:
- 检查搜索条件和关键词
- 先不使用关键词过滤,查看原始数据
- 查看日志了解详细信息

## 📚 文档

- **README_V2.md**: 增强版完整文档(本文件)
- **ENHANCED_FEATURES.md**: 增强功能详细说明
- **API_GUIDE.md**: API 使用指南
- **代码注释**: 所有模块都有详细的文档字符串

## 🚀 未来改进

计划中的功能增强:

1. **并行抓取**: 支持多线程并行获取拍品,提高速度
2. **增量更新**: 只获取新增或变化的拍品
3. **价格监控**: 监控拍品价格变化并发送通知
4. **图片下载**: 自动下载拍品图片
5. **数据分析**: 内置价格趋势分析功能
6. **定时任务**: 支持定时自动抓取和导出
7. **更多网站**: 支持 Christie's, Sotheby's 等其他拍卖网站

## 📄 许可证

本项目仅供学习和研究使用。

## 🙏 致谢

感谢以下服务和工具:
- DeepSeek - 提供强大的 LLM 能力
- Zyte - 提供专业的网页抓取服务
- BeautifulSoup - HTML 解析库
- FastAPI - 现代化的 Web 框架
