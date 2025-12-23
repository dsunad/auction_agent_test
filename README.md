# 拍卖信息处理 Agent

这是一个智能拍卖信息处理系统,能够从 Stacks Bowers 拍卖网站获取数据,并根据用户的自然语言指令进行搜索、过滤和分析。

## 功能特性

本系统集成了 DeepSeek 大语言模型,能够理解复杂的自然语言查询,并自动调用相应的工具函数完成任务。主要功能包括按时间范围搜索拍卖(如"未来一周内截止的拍卖"),按类别过滤(如硬币、纸币、代币等),按关键词搜索特定拍卖品,以及获取拍卖的详细信息。

系统支持多种使用方式,包括命令行交互界面和 RESTful API 服务,可以灵活集成到不同的应用场景中。

## 技术架构

系统采用模块化设计,核心组件包括:

**Agent 核心模块** 使用 DeepSeek LLM 进行自然语言理解和决策,支持函数调用(Function Calling)功能,能够根据用户意图自动选择和执行工具。

**数据抓取模块** 支持使用 Zyte API 进行高级网页抓取,也可以使用标准 HTTP 请求获取数据,能够解析 HTML 并提取结构化信息。

**查询引擎** 提供灵活的过滤和搜索功能,支持多条件组合查询,包括时间范围、类别、关键词、价格等。

**API 服务** 基于 FastAPI 构建的 RESTful API,提供标准的 HTTP 接口,方便与其他系统集成。

## 安装和配置

### 环境要求

系统需要 Python 3.8 或更高版本,建议使用虚拟环境进行安装。

### 安装步骤

首先安装依赖包:

```bash
pip install -r requirements.txt
```

配置文件 `config.py` 中已经预设了 API 密钥,包括 DeepSeek API、Tavily API 和 Zyte API。如需修改,请直接编辑该文件。

## 使用方法

### 命令行模式

启动命令行交互界面:

```bash
python cli.py
```

然后可以输入自然语言指令,例如:

- "搜索未来一周内截止的所有硬币拍卖"
- "查找 12 月 10 日之前的代币拍卖"
- "显示所有包含 Silver Dollar 的拍卖"
- "有哪些拍卖的 Lots 数量超过 100"

输入 `quit` 或 `exit` 退出程序,输入 `reset` 重置对话历史。

### API 服务模式

启动 API 服务器:

```bash
python api_server.py
```

服务器默认运行在 `http://localhost:8000`,可以通过以下端点访问:

**查询端点** `POST /api/query`

发送自然语言查询:

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "搜索未来一周内截止的所有硬币拍卖"}'
```

**搜索端点** `POST /api/search`

直接使用参数搜索:

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "time_range_days": 7,
    "categories": ["U.S. Coins & Related", "World Coins"],
    "keywords": ["silver"]
  }'
```

**健康检查** `GET /health`

检查服务状态:

```bash
curl http://localhost:8000/health
```

### Python 代码集成

也可以直接在 Python 代码中使用 Agent:

```python
from agent import AuctionAgent

# 创建 Agent 实例
agent = AuctionAgent()

# 处理自然语言指令
response = agent.process_command("搜索未来一周内截止的所有硬币拍卖")
print(response)

# 直接调用搜索函数
results = agent.search_auctions(
    time_range_days=7,
    categories=["U.S. Coins & Related", "World Coins"]
)
print(results)
```

## 支持的拍卖类别

系统能够识别以下拍卖类别:

- **U.S. Coins & Related**: 美国硬币及相关
- **World Coins**: 世界硬币
- **U.S. Paper Currency**: 美国纸币
- **World Paper Currency**: 世界纸币
- **Numismatic Americana**: 美国钱币学相关(代币、奖章等)
- **Ancient Coins**: 古币
- **Bullion**: 金银条

## 示例查询

以下是一些典型的查询示例:

**按时间范围搜索**
- "未来一周内截止的拍卖"
- "12 月 10 日之前的拍卖"
- "本月的所有拍卖"

**按类别搜索**
- "所有硬币拍卖"
- "美国纸币拍卖"
- "代币和奖章拍卖"

**按关键词搜索**
- "包含 Silver Dollar 的拍卖"
- "Morgan Dollar 拍卖"
- "中国硬币拍卖"

**组合查询**
- "未来一周内截止的硬币拍卖,Lots 数量超过 100"
- "12 月份的所有美国纸币拍卖"

## 数据结构

### 拍卖信息

每个拍卖包含以下字段:

```json
{
  "title": "拍卖标题",
  "date": "2025-12-05",
  "lots_count": 476,
  "category": "U.S. Coins & Related",
  "url": "拍卖详情页 URL"
}
```

### 拍卖项目

每个拍卖项目包含:

```json
{
  "lot_number": "70001",
  "title": "项目标题",
  "description": "详细描述",
  "current_bid": 40,
  "grade": "MS-65",
  "grading_service": "PCGS",
  "category": "U.S. Coins & Related"
}
```

## 扩展开发

系统采用模块化设计,便于扩展和定制:

**添加新的工具函数**: 在 `agent.py` 中的 `tools` 列表中添加新的工具定义,并实现相应的执行函数。

**自定义数据源**: 修改 `scraper.py` 或 `data_fetcher.py` 中的数据获取逻辑,支持其他拍卖网站。

**增强查询能力**: 在查询引擎中添加更多的过滤条件,如价格范围、评级等。

**集成通知功能**: 添加监控和通知模块,当符合条件的拍卖出现时自动提醒用户。

## 注意事项

本系统仅用于学习和研究目的,在使用网页抓取功能时,请遵守目标网站的 robots.txt 规则和服务条款。建议合理控制请求频率,避免对目标网站造成过大负担。

API 密钥已在配置文件中预设,请妥善保管,避免泄露。在生产环境中,建议使用环境变量或密钥管理服务来存储敏感信息。

## 许可证

本项目仅供学习和研究使用。
