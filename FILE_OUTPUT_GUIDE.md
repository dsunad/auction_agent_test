# 📁 拍卖信息输出位置说明

## 📍 文件保存位置

**所有拍品信息都保存在项目根目录：**
```
/home/user/webapp/
```

## 📄 支持的文件格式

系统支持三种输出格式，您可以根据需要选择：

### 1. JSON 格式 (推荐)
- **扩展名**: `.json`
- **特点**: 结构化数据，易于程序处理
- **适用场景**: API 集成、数据分析、进一步处理

**示例**:
```json
[
  {
    "lot_number": "10001",
    "title": "1921 Morgan Silver Dollar",
    "description": "Beautiful uncirculated Morgan silver dollar",
    "current_bid": "5000",
    "image_url": "https://example.com/image1.jpg",
    "auction_title": "December 2025 Showcase Auction",
    "auction_url": "https://auctions.stacksbowers.com/..."
  }
]
```

### 2. CSV 格式
- **扩展名**: `.csv`
- **特点**: 表格格式，可用 Excel 打开
- **适用场景**: 数据分析、电子表格处理

**示例**:
```csv
lot_number,title,description,current_bid,image_url
10001,1921 Morgan Silver Dollar,Beautiful uncirculated...,5000,https://...
10002,1909-S VDB Lincoln Cent,Rare Lincoln penny...,1200,https://...
```

### 3. TXT 格式
- **扩展名**: `.txt`
- **特点**: 纯文本格式，易于阅读
- **适用场景**: 快速查看、打印、分享

**示例**:
```
============================================================
拍品 #1
============================================================
lot_number: 10001
title: 1921 Morgan Silver Dollar
description: Beautiful uncirculated Morgan silver dollar
current_bid: 5000
image_url: https://example.com/image1.jpg
```

## 🔧 使用方法

### 方法 1: Python API

```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# AI 智能浏览并保存
lots = agent.ai_smart_browse(
    auction_url="https://auctions.stacksbowers.com/auctions/session-1",
    search_query="找出所有金币"
)

# 保存为不同格式
agent.lot_scraper.save_lots_to_file(lots, "gold_coins.json", format="json")
agent.lot_scraper.save_lots_to_file(lots, "gold_coins.csv", format="csv")
agent.lot_scraper.save_lots_to_file(lots, "gold_coins.txt", format="txt")
```

### 方法 2: 命令行 (CLI)

```bash
# 使用 CLI 工具
python cli_v2.py

# 然后输入命令，例如:
# "找出所有金币并保存到 gold_coins.json"
```

### 方法 3: 多层级浏览并保存

```python
from hierarchical_browser import HierarchicalBrowser

browser = HierarchicalBrowser()

# 从首页自动发现所有场次并搜索
result = browser.browse_all_auctions(
    index_url="https://auctions.stacksbowers.com/",
    search_query="找出所有银元"
)

# 导出所有结果
browser.export_results(result, "all_silver_dollars.json", format="json")
```

## 📊 文件内容说明

每个拍品包含以下信息（如果可用）：

| 字段 | 说明 | 示例 |
|------|------|------|
| `lot_number` | 拍品编号 | "10001" |
| `title` | 拍品标题 | "1921 Morgan Silver Dollar" |
| `description` | 拍品描述 | "Beautiful uncirculated..." |
| `current_bid` | 当前价格 | "5000" |
| `image_url` | 图片链接 | "https://..." |
| `auction_title` | 所属拍卖场次 | "December 2025 Showcase..." |
| `auction_url` | 拍卖链接 | "https://auctions..." |
| `_relevance_score` | 相关性评分 (AI 浏览时) | 8.5 |
| `_ai_reason` | AI 判断理由 (AI 浏览时) | "该拍品是金币..." |

## 🔍 如何查找已保存的文件

### 查看所有输出文件
```bash
cd /home/user/webapp
ls -lh *.json *.csv *.txt
```

### 查看最近生成的文件
```bash
cd /home/user/webapp
ls -lht *.json *.csv *.txt | head -10
```

### 搜索特定关键词的文件
```bash
cd /home/user/webapp
find . -name "*gold*" -o -name "*silver*" -o -name "*coin*"
```

## 📝 命名建议

为了方便查找和管理，建议使用描述性的文件名：

**推荐命名方式**:
- `gold_coins_2024-12-24.json` - 按日期
- `silver_dollars_showcase_auction.csv` - 按拍卖会
- `rare_pennies_search_results.txt` - 按搜索内容

**避免的命名方式**:
- `results.json` - 太泛化
- `data.csv` - 不清晰
- `output.txt` - 无法识别内容

## 🚀 快速开始示例

### 示例 1: 搜索单个场次并保存

```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# 使用 AI 智能浏览
lots = agent.ai_smart_browse(
    auction_url="https://auctions.stacksbowers.com/auctions/session-1",
    search_query="找出所有金币",
    max_pages=5
)

print(f"找到 {len(lots)} 个符合条件的拍品")

# 保存结果
agent.lot_scraper.save_lots_to_file(lots, "gold_coins_results.json", format="json")
print(f"✅ 已保存到: /home/user/webapp/gold_coins_results.json")
```

### 示例 2: 遍历整个网站并保存

```python
from hierarchical_browser import HierarchicalBrowser

browser = HierarchicalBrowser()

# 从首页开始遍历所有场次
result = browser.browse_all_auctions(
    index_url="https://auctions.stacksbowers.com/",
    search_query="找出所有银元",
    max_auctions=10  # 限制搜索前 10 个场次
)

# 导出结果
browser.export_results(result, "all_silver_dollars.json", format="json")

# 查看统计
print(f"搜索场次数: {result['total_auctions']}")
print(f"找到拍品数: {result['total_lots']}")
print(f"✅ 已保存到: /home/user/webapp/all_silver_dollars.json")
```

### 示例 3: 使用现有的演示文件

项目中已经包含了一些演示输出文件：

```bash
# 查看演示文件
ls -lh /home/user/webapp/demo_lots.*

# 输出:
# demo_lots.json (440 bytes)  - JSON 格式示例
# demo_lots.csv (274 bytes)   - CSV 格式示例
# demo_lots.txt (598 bytes)   - TXT 格式示例
```

## ❓ 常见问题

### Q1: 为什么找不到输出文件？
**A**: 确保您在正确的目录中查找：
```bash
cd /home/user/webapp
pwd  # 应该显示 /home/user/webapp
ls -la  # 查看所有文件
```

### Q2: 如何指定自定义保存位置？
**A**: 使用完整路径或相对路径：
```python
# 完整路径
agent.lot_scraper.save_lots_to_file(lots, "/home/user/webapp/results/gold_coins.json", "json")

# 相对路径（相对于 /home/user/webapp）
agent.lot_scraper.save_lots_to_file(lots, "./output/gold_coins.json", "json")
```

### Q3: 文件已存在怎么办？
**A**: 默认会覆盖同名文件。建议使用不同的文件名或添加时间戳：
```python
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"gold_coins_{timestamp}.json"
agent.lot_scraper.save_lots_to_file(lots, filename, "json")
```

### Q4: 如何合并多次搜索的结果？
**A**: 可以使用 Python 合并 JSON 文件：
```python
import json

# 读取多个文件
with open("results1.json", "r") as f:
    data1 = json.load(f)

with open("results2.json", "r") as f:
    data2 = json.load(f)

# 合并
merged = data1 + data2

# 保存
with open("merged_results.json", "w") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
```

## 📚 相关文档

- **AI 智能浏览**: [AI_SMART_BROWSE_DOC.md](./AI_SMART_BROWSE_DOC.md)
- **多层级浏览**: [HIERARCHICAL_BROWSE_DOC.md](./HIERARCHICAL_BROWSE_DOC.md)
- **功能改进**: [IMPROVEMENTS.md](./IMPROVEMENTS.md)
- **系统日志**: [auction_agent.log](./auction_agent.log)

## 💡 提示

1. **使用绝对路径**: 如果不确定当前目录，使用 `/home/user/webapp/` 开头的绝对路径
2. **添加日期**: 在文件名中包含日期，方便追踪历史记录
3. **选择合适格式**: 
   - 需要进一步处理 → JSON
   - 需要 Excel 查看 → CSV
   - 只是阅读查看 → TXT
4. **检查日志**: 如果保存失败，查看 `auction_agent.log` 文件了解详情

---

**最后更新**: 2024-12-24

如有问题，请查看项目文档或查看日志文件 `auction_agent.log`。
