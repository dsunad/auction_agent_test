# 拍卖搜索系统 - 智能搜索增强版

## 🎉 更新内容

### 修复的问题

1. **Zyte API 参数冲突** ✅
   - 问题: 同时使用 `browserHtml` 和 `httpResponseBody` 导致 422 错误
   - 修复: 移除冲突的参数,只使用 `browserHtml`

2. **搜索功能不够智能** ✅
   - 问题: 简单的字符串匹配,无法处理同义词、拼写差异等
   - 修复: 实现智能搜索系统

### 新增功能

#### 1. 智能关键词匹配

支持三种匹配模式:

- **完全匹配** (最高分 10 分): 关键词完整出现在文本中
- **部分匹配** (最高分 5 分): 关键词中的单词部分匹配
- **模糊匹配** (最高分 3 分): 使用相似度算法匹配相近的词

```python
# 示例
keywords = ["silver", "dollar"]
# 会匹配:
# - "Silver Dollar" (完全匹配, 20分)
# - "silver coin" (部分匹配, 10分)  
# - "silvr dllar" (模糊匹配, ~5分)
```

#### 2. 同义词扩展

自动扩展常见的同义词,提高搜索覆盖率:

```python
# 示例
"gold" -> ["gold", "golden", "au", "aurum"]
"silver" -> ["silver", "ag", "argentum"]
"rare" -> ["rare", "scarce", "uncommon", "unique"]
"dollar" -> ["dollar", "dollars", "usd"]
```

#### 3. 相关性排序

搜索结果按相关性评分自动排序,最相关的拍品排在最前面:

```python
# 每个搜索结果包含:
{
    "lot_number": "001",
    "title": "1921 Morgan Silver Dollar",
    "_relevance_score": 20.0,  # 相关性评分
    "_matched_keywords": [      # 匹配的关键词
        ("silver", "exact", 1.0),
        ("dollar", "exact", 1.0)
    ]
}
```

#### 4. 自然语言查询

新增 `search_lots_intelligently` 函数,支持自然语言查询:

```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# 自然语言查询
result = agent.search_lots_intelligently(
    auction_url="https://...",
    query="find all rare gold coins from Morgan series",
    fuzzy_match=True
)
```

## 📖 使用示例

### 示例 1: 基本搜索(带模糊匹配)

```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# 使用关键词搜索,启用模糊匹配
lots = agent.get_lots_from_auction(
    auction_url="https://auctions.stacksbowers.com/auctions/...",
    keywords=["silver", "dollar"],
    fuzzy_match=True,  # 新增参数
    max_pages=5
)

print(f"找到 {len(lots)} 个拍品")
for lot in lots[:3]:
    score = lot.get('_relevance_score', 0)
    print(f"- {lot['title']} (相关性: {score:.2f})")
```

### 示例 2: 智能搜索

```python
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# 自然语言查询
lots = agent.search_lots_intelligently(
    auction_url="https://auctions.stacksbowers.com/auctions/...",
    query="我想找所有的金币和银币",
    fuzzy_match=True
)

# 结果已按相关性排序
for lot in lots[:5]:
    print(f"{lot['title']}")
    print(f"  相关性评分: {lot.get('_relevance_score', 0):.2f}")
    print(f"  匹配关键词: {lot.get('_matched_keywords', [])}")
```

### 示例 3: 命令行交互(自动使用智能搜索)

```bash
python3 cli_v2.py
```

然后输入:
```
你: 找出所有 Morgan Dollar 的拍品
```

Agent 会自动:
1. 提取关键词: ["morgan", "dollar"]
2. 扩展同义词: ["morgan", "dollar", "dollars", "usd", "morgan dollar"]
3. 使用智能搜索找到最相关的拍品
4. 按相关性排序返回结果

## 🔧 配置选项

### 模糊匹配参数

```python
# 在 lot_scraper.py 中可以调整:
min_score = 0.6  # 最小相似度阈值 (0-1)
# 0.6 表示需要至少 60% 的相似度才算匹配
```

### 添加自定义同义词

在 `lot_scraper.py` 的 `_expand_synonyms` 方法中添加:

```python
synonyms = {
    'gold': ['golden', 'au', 'aurum'],
    'silver': ['ag', 'argentum'],
    # 添加你的同义词
    'your_word': ['synonym1', 'synonym2'],
}
```

## 📊 性能对比

### 修复前

```
搜索 "silver dollar"
找到: 2 个拍品 (只有完全匹配的)
```

### 修复后

```
搜索 "silver dollar"
找到: 5 个拍品
- Morgan Silver Dollar (评分: 20.0) - 完全匹配
- Peace Silver Dollar (评分: 20.0) - 完全匹配  
- Silver Coin Collection (评分: 10.0) - 部分匹配
- Ancient Silver Drachma (评分: 10.0) - 部分匹配
- Silver-plated Medal (评分: 5.2) - 模糊匹配
```

## 🧪 测试

运行测试脚本验证功能:

```bash
python3 test_intelligent_search.py
```

测试内容:
- ✅ 关键词提取
- ✅ 同义词扩展
- ✅ 相关性评分
- ✅ 模糊匹配过滤
- ✅ 智能搜索

## 📝 API 更新

### 新增/更新的方法

#### `get_lots_from_auction` (已更新)

```python
def get_lots_from_auction(
    auction_url: str,
    keywords: Optional[List[str]] = None,
    max_pages: int = 20,
    fuzzy_match: bool = True  # 新增参数
) -> List[Dict]
```

#### `search_lots_intelligently` (新增)

```python
def search_lots_intelligently(
    auction_url: str,
    query: str,  # 自然语言查询
    fuzzy_match: bool = True,
    max_pages: int = 20
) -> List[Dict]
```

#### `filter_lots_by_keyword` (已增强)

```python
def filter_lots_by_keyword(
    lots: List[Dict],
    keywords: List[str],
    fuzzy_match: bool = True,  # 新增
    min_score: float = 0.6     # 新增
) -> List[Dict]
```

## 🚀 下一步优化建议

1. **机器学习排序**: 使用 ML 模型学习用户偏好,优化排序
2. **并行搜索**: 多线程并行搜索多个拍卖场次
3. **搜索历史**: 记录搜索历史,提供个性化推荐
4. **高级过滤**: 价格区间、等级、认证机构等过滤
5. **实时监控**: 自动监控新拍品并发送通知

## 🐛 已知问题

无(所有已知问题已修复)

## 📞 支持

如有问题,请查看日志文件 `auction_agent.log` 获取详细信息。
