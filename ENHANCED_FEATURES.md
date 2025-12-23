# 增强功能说明

## 新增功能概览

Agent V2 版本新增了强大的拍品抓取和导出功能,现在可以深入到每个拍卖场次内部,获取所有拍品的详细信息,并支持关键词过滤和多格式导出。

## 核心增强

### 1. 深入拍卖场次获取拍品列表

Agent 现在能够进入特定的拍卖场次,抓取所有拍品的详细信息,包括拍品编号、标题、描述、当前出价、图片等。

**技术实现**:
- 使用 Zyte API 绕过 Cloudflare 反爬虫保护
- 支持自动分页,获取所有页面的拍品
- 智能解析 HTML 和 JSON 数据

### 2. 关键词过滤

可以按关键词过滤拍品,在标题和描述中搜索特定词汇,快速找到感兴趣的拍品。

**支持的过滤方式**:
- 单个关键词或多个关键词
- 不区分大小写
- 在标题和描述中同时搜索

### 3. 多格式导出

支持将拍品信息导出为多种格式,方便后续处理和分析。

**支持的格式**:
- **JSON**: 结构化数据,便于程序处理
- **CSV**: 表格格式,可用 Excel 打开
- **TXT**: 纯文本格式,易读

## 使用方法

### 方法 1: 自然语言指令(推荐)

直接用自然语言告诉 Agent 你想做什么,它会自动调用相应的功能。

**示例指令**:

```
获取这个拍卖的所有拍品信息:
https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475
```

```
搜索包含 "silver" 的拍品并导出到 silver_lots.json
```

```
找出所有硬币拍卖的拍品,筛选包含 "dollar" 的,保存为 CSV 格式
```

```
获取未来一周内的代币拍卖,找出所有包含 "Washington" 的拍品,导出到文件
```

### 方法 2: Python 代码

在代码中直接调用 Agent 的功能。

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
print(f"过滤后: {len(lots)} 个拍品")

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
print(f"导出了 {result['lots_count']} 个拍品到 {result['output_file']}")
```

### 方法 3: 命令行界面

使用增强版命令行界面。

```bash
cd auction_agent
python3 cli_v2.py
```

然后输入自然语言指令,例如:

```
您: 获取这个拍卖的所有拍品: https://auctions.stacksbowers.com/auctions/3-1NZHVT/...

您: 搜索包含 "silver" 的拍品并导出到 silver_lots.csv

您: 找出所有硬币拍卖,获取包含 "Morgan Dollar" 的拍品,保存为 JSON
```

## 实际应用场景

### 场景 1: 收集特定类型的拍品

**需求**: 我想找出所有即将拍卖的 Morgan Silver Dollar 硬币

**操作**:
```
搜索未来一周内的硬币拍卖,找出所有包含 "Morgan" 和 "Silver Dollar" 的拍品,导出到 morgan_dollars.csv
```

Agent 会:
1. 搜索未来 7 天内的硬币拍卖场次
2. 进入每个拍卖场次获取所有拍品
3. 过滤出包含 "Morgan" 和 "Silver Dollar" 的拍品
4. 导出到 CSV 文件

### 场景 2: 监控特定拍卖

**需求**: 我想获取某个特定拍卖的所有拍品信息,方便离线查看

**操作**:
```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()
lots = agent.get_lots_from_auction(
    "https://auctions.stacksbowers.com/auctions/3-1NZHVT/...",
    max_pages=50  # 获取最多 50 页
)

# 保存到文件
import json
with open("auction_lots.json", "w", encoding="utf-8") as f:
    json.dump(lots, f, ensure_ascii=False, indent=2)
```

### 场景 3: 批量数据分析

**需求**: 我想分析最近所有硬币拍卖的价格分布

**操作**:
```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# 搜索并导出
result = agent.search_and_export_lots(
    auction_criteria={
        "time_range_days": 30,
        "categories": ["U.S. Coins & Related", "World Coins"]
    },
    output_file="all_coin_lots.csv",
    output_format="csv"
)

print(f"导出了 {result['lots_count']} 个拍品")

# 然后可以用 pandas 分析 CSV 文件
import pandas as pd
df = pd.read_csv("all_coin_lots.csv")
# 进行数据分析...
```

## 数据结构

### 拍品信息字段

每个拍品包含以下字段(根据实际抓取结果可能有所不同):

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

## 文件格式示例

### JSON 格式

```json
[
  {
    "lot_number": "70001",
    "title": "1919 General John J. Pershing Portrait Plaque",
    "description": "Bronze and Iron. Extremely Fine.",
    "current_bid": "40"
  },
  {
    "lot_number": "70002",
    "title": "Admiral Dewey Medal Bronze",
    "description": "MS-64 BN (PCGS)",
    "current_bid": "320"
  }
]
```

### CSV 格式

```csv
lot_number,title,description,current_bid
70001,1919 General John J. Pershing Portrait Plaque,Bronze and Iron. Extremely Fine.,40
70002,Admiral Dewey Medal Bronze,MS-64 BN (PCGS),320
```

### TXT 格式

```
============================================================
拍品 #1
============================================================
lot_number: 70001
title: 1919 General John J. Pershing Portrait Plaque
description: Bronze and Iron. Extremely Fine.
current_bid: 40

============================================================
拍品 #2
============================================================
lot_number: 70002
title: Admiral Dewey Medal Bronze
description: MS-64 BN (PCGS)
current_bid: 320
```

## 技术细节

### Zyte API 集成

为了绕过 Cloudflare 反爬虫保护,系统集成了 Zyte API。Zyte 是一个专业的网页抓取服务,能够:

- 自动处理 JavaScript 渲染
- 绕过反爬虫机制
- 提供稳定可靠的抓取服务

**配置**: API 密钥已在 `config.py` 中配置,无需额外设置。

### 智能解析

系统使用多种策略解析拍品信息:

1. **HTML 解析**: 使用 BeautifulSoup 解析页面结构
2. **JSON 提取**: 从页面脚本中提取 JSON 数据
3. **正则匹配**: 使用正则表达式提取特定信息
4. **容错处理**: 多种解析方法互为备份

### 性能优化

- **分页处理**: 自动检测和处理分页
- **请求限速**: 避免过快请求导致封禁
- **错误重试**: 失败时自动重试
- **缓存机制**: 可选的缓存功能(未来实现)

## 注意事项

### 使用限制

1. **API 配额**: Zyte API 有使用配额限制,请合理使用
2. **请求频率**: 建议控制请求频率,避免对目标网站造成负担
3. **数据准确性**: 抓取的数据依赖于网站结构,可能需要调整解析逻辑

### 最佳实践

1. **测试先行**: 先在小范围测试,确认数据正确后再大规模抓取
2. **定期更新**: 网站结构可能变化,需要定期检查和更新解析逻辑
3. **数据备份**: 重要数据建议多格式保存
4. **遵守规则**: 遵守网站的 robots.txt 和服务条款

## 故障排除

### 问题 1: 无法获取拍品

**可能原因**:
- Zyte API 配额用尽
- 网站结构变化
- 网络连接问题

**解决方法**:
- 检查 Zyte API 配额
- 查看日志文件了解详细错误
- 尝试手动访问 URL 确认网站是否可访问

### 问题 2: 拍品信息不完整

**可能原因**:
- 网站使用动态加载
- 解析逻辑需要调整

**解决方法**:
- 检查返回的 HTML 内容
- 调整 `lot_scraper.py` 中的解析逻辑
- 增加等待时间让页面完全加载

### 问题 3: 导出文件为空

**可能原因**:
- 没有找到符合条件的拍品
- 关键词过滤太严格

**解决方法**:
- 检查搜索条件和关键词
- 先不使用关键词过滤,查看原始数据
- 查看日志了解详细信息

## 未来改进

计划中的功能增强:

1. **并行抓取**: 支持多线程并行获取拍品,提高速度
2. **增量更新**: 只获取新增或变化的拍品
3. **价格监控**: 监控拍品价格变化并发送通知
4. **图片下载**: 自动下载拍品图片
5. **数据分析**: 内置价格趋势分析功能
6. **定时任务**: 支持定时自动抓取和导出

## 总结

增强版 Agent 提供了强大的拍品抓取和导出功能,能够满足各种数据收集和分析需求。通过自然语言指令,您可以轻松完成复杂的数据获取任务,无需编写代码即可获得结构化的拍品信息。
