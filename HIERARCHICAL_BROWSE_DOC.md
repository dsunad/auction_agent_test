# 多层级智能浏览功能

## 🎯 解决的问题

**之前的限制**:
- ❌ 只能浏览单个拍卖场次
- ❌ 需要手动提供每个场次的 URL
- ❌ 无法自动发现网站上的所有场次

**现在的能力**:
- ✅ 自动从首页发现所有拍卖场次
- ✅ 自动遍历每个场次
- ✅ 在每个场次中搜索符合要求的拍品
- ✅ 汇总所有结果

## 🚀 工作流程

```
用户输入: "在 https://auctions.stacksbowers.com/ 找出所有金币"
    ↓
1. 分析首页
    ├─ 使用 AI 识别页面上的所有拍卖场次
    ├─ 提取每个场次的标题、URL、日期等信息
    └─ 返回场次列表
    ↓
2. 遍历场次
    ├─ 场次 1: December 2025 Tokens & Medals
    │   └─ AI 智能浏览 → 找到 3 个金币
    ├─ 场次 2: December 2025 Showcase Auction
    │   └─ AI 智能浏览 → 找到 5 个金币
    └─ 场次 3: World Collectors Choice
        └─ AI 智能浏览 → 找到 2 个金币
    ↓
3. 汇总结果
    └─ 总共找到 10 个符合要求的金币
```

## 💡 使用示例

### 示例 1: 搜索整个网站

```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# 从首页开始搜索
result = agent.browse_all_auction_sessions(
    index_url="https://auctions.stacksbowers.com/",
    search_query="找出所有金币",
    max_auctions=5  # 限制前5个场次
)

print(f"浏览了 {result['auctions_count']} 个场次")
print(f"找到 {result['total_lots']} 个金币")

# 查看每个场次的结果
for auction_result in result['auctions']:
    auction = auction_result['auction']
    lots = auction_result['lots']
    print(f"\n{auction['title']}: {len(lots)} 个拍品")
```

### 示例 2: 命令行使用

```bash
python cli_v2.py
```

```
你: 在 https://auctions.stacksbowers.com/ 找出所有银币

Agent: 好的，我将从首页开始搜索所有拍卖场次...
       
       发现 12 个拍卖场次
       
       正在浏览场次 1/12: December 2025 Tokens & Medals
       找到 5 个符合要求的拍品
       
       正在浏览场次 2/12: December 2025 Showcase Auction
       找到 8 个符合要求的拍品
       
       ...
       
       浏览完成！
       总共找到 45 个银币
```

### 示例 3: 直接调用

```python
from hierarchical_browser import HierarchicalBrowser

browser = HierarchicalBrowser()

# 获取所有符合要求的拍品（扁平化列表）
all_lots = browser.get_all_matching_lots(
    "https://auctions.stacksbowers.com/",
    "找出所有金币",
    max_auctions=3
)

# 按相关性排序
for i, lot in enumerate(all_lots[:10], 1):
    print(f"{i}. {lot['title']}")
    print(f"   来自: {lot['auction_title']}")
    print(f"   评分: {lot['relevance_score']}/10")
```

## 🔧 技术实现

### 核心类: `HierarchicalBrowser`

```python
class HierarchicalBrowser:
    """层级浏览器"""
    
    def discover_auctions(self, index_url):
        """分析首页，发现所有拍卖场次"""
        # 1. 获取首页内容
        # 2. 使用 AI 识别拍卖场次
        # 3. 提取标题、URL、日期等信息
        # 4. 补全相对路径为完整 URL
        # 5. 返回场次列表
    
    def browse_all_auctions(self, index_url, search_query, max_auctions):
        """遍历所有场次并搜索"""
        # 1. 发现所有场次
        # 2. 遍历每个场次
        # 3. 使用 AI 智能浏览器搜索拍品
        # 4. 为每个拍品添加场次信息
        # 5. 汇总所有结果
    
    def get_all_matching_lots(self, index_url, search_query, max_auctions):
        """获取所有符合要求的拍品（扁平化）"""
        # 1. 调用 browse_all_auctions
        # 2. 合并所有场次的拍品
        # 3. 按相关性排序
        # 4. 返回扁平化列表
```

### AI 提示词设计

```python
prompt = f"""请分析这个拍卖网站首页，找出所有的拍卖场次。

页面内容:
{content}

请识别页面上的所有拍卖场次，并返回 JSON 格式的结果：
{{
  "auctions": [
    {{
      "title": "拍卖场次标题",
      "date": "拍卖日期",
      "lots_count": "拍品数量",
      "url": "拍卖场次的链接",
      "category": "拍卖类别"
    }}
  ]
}}
"""
```

## 📊 性能考虑

### 时间成本
- 发现场次: ~5-10秒
- 浏览每个场次: ~40-60秒/场次
- 总时间: 发现时间 + (场次数 × 每场次时间)

**示例**:
```
3 个场次: ~5 + (3 × 50) = ~155 秒 (约 2.5 分钟)
5 个场次: ~5 + (5 × 50) = ~255 秒 (约 4 分钟)
10 个场次: ~5 + (10 × 50) = ~505 秒 (约 8 分钟)
```

### 优化建议

1. **限制场次数量**
```python
max_auctions=3  # 只浏览前3个场次
```

2. **限制每个场次的页数**
```python
# 在 hierarchical_browser.py 中修改
max_pages=1  # 每个场次只浏览第一页
```

3. **并行处理**（未来优化）
```python
# 使用多线程同时浏览多个场次
# （需要注意 API 速率限制）
```

## 🎨 特色功能

### 1. 自动 URL 补全
```python
# 输入: /auctions/3-1NZHVT/...
# 输出: https://auctions.stacksbowers.com/auctions/3-1NZHVT/...
```

### 2. 场次信息追踪
每个拍品自动包含:
- `auction_title`: 来自哪个场次
- `auction_url`: 场次链接
- `auction_date`: 拍卖日期

### 3. 灵活的结果格式
```python
# 方式 1: 分场次的结构化结果
result = browser.browse_all_auctions(...)
for auction_result in result['auctions']:
    print(auction_result['auction']['title'])
    print(auction_result['lots'])

# 方式 2: 扁平化列表
all_lots = browser.get_all_matching_lots(...)
for lot in all_lots:
    print(lot['title'])
```

## 🔄 与其他功能的关系

```
多层级浏览 (browse_all_auction_sessions)
    ↓
    调用 AI 智能浏览 (ai_smart_browse) 
        ↓
        调用基础浏览器 (smart_browse)
```

**使用场景选择**:

| 场景 | 使用的工具 |
|------|----------|
| 搜索整个网站 | `browse_all_auction_sessions` |
| 搜索单个场次 | `ai_smart_browse` |
| 已知精确关键词 | `search_lots_intelligently` |

## 📝 完整示例

```python
from agent_v2 import AuctionAgentV2

# 创建 Agent
agent = AuctionAgentV2()

# 场景 1: 自动发现并搜索所有场次
print("="*60)
print("场景 1: 搜索整个网站")
print("="*60)

result = agent.browse_all_auction_sessions(
    index_url="https://auctions.stacksbowers.com/",
    search_query="找出所有金币",
    max_auctions=3  # 限制前3个场次
)

if result['success']:
    print(f"\n浏览了 {result['auctions_count']} 个场次")
    print(f"找到 {result['total_lots']} 个金币\n")
    
    # 显示每个场次的结果
    for i, auction_result in enumerate(result['auctions'], 1):
        auction = auction_result['auction']
        lots_count = auction_result['lots_count']
        print(f"{i}. {auction['title']}: {lots_count} 个金币")

# 场景 2: 单个场次搜索
print("\n" + "="*60)
print("场景 2: 搜索单个场次")
print("="*60)

lots = agent.ai_smart_browse(
    auction_url="https://auctions.stacksbowers.com/auctions/...",
    search_query="silver medal",
    max_pages=1
)

print(f"\n找到 {len(lots)} 个银牌")

# 场景 3: 导出结果
print("\n" + "="*60)
print("场景 3: 导出到文件")
print("="*60)

# 使用 hierarchical_browser 直接导出
from hierarchical_browser import HierarchicalBrowser

browser = HierarchicalBrowser()
result = browser.browse_all_auctions(
    "https://auctions.stacksbowers.com/",
    "找出所有金币",
    max_auctions=2
)

browser.export_results(result, "gold_coins.json", "json")
print("\n结果已导出到 gold_coins.json")
```

## 🐛 故障排除

### 问题 1: 未发现任何场次

**可能原因**:
- 首页结构与预期不同
- AI 未能识别拍卖场次

**解决方法**:
```python
# 检查首页内容
browser = HierarchicalBrowser()
content = browser.browser.fetch_page_content(index_url)
print(content[:2000])  # 查看前2000字符
```

### 问题 2: URL 错误

**可能原因**:
- 相对路径未正确补全

**解决方法**:
```python
# 查看发现的场次
auctions = browser.discover_auctions(index_url)
for auction in auctions:
    print(auction['url'])
```

### 问题 3: 处理时间太长

**解决方法**:
```python
# 1. 减少场次数量
max_auctions=2

# 2. 减少每个场次的页数
# 修改 hierarchical_browser.py line 93
max_pages=1

# 3. 先测试一个场次
max_auctions=1
```

## 🚀 未来优化

1. **并行处理**: 同时浏览多个场次
2. **增量更新**: 只浏览新增的场次
3. **缓存机制**: 缓存已浏览的场次
4. **智能优先级**: 根据场次信息优先浏览相关度高的

## 📋 总结

**多层级智能浏览**完美解决了"不能识别分场"的问题：

| 功能 | 实现 |
|-----|------|
| 自动发现场次 | ✅ AI 分析首页 |
| 遍历所有场次 | ✅ 自动进入每个场次 |
| 搜索拍品 | ✅ AI 智能浏览 |
| 汇总结果 | ✅ 按场次或扁平化 |
| 导出数据 | ✅ JSON/CSV/TXT |

现在您可以轻松地搜索整个拍卖网站了！🎉
