# API 使用指南

本文档介绍如何使用拍卖信息处理 Agent 的 RESTful API。

## 启动 API 服务

运行以下命令启动 API 服务器:

```bash
python api_server.py
```

服务器默认运行在 `http://localhost:8000`。

## API 端点

### 1. 根路径

**端点**: `GET /`

**描述**: 获取 API 基本信息和可用端点列表

**示例请求**:
```bash
curl http://localhost:8000/
```

**响应**:
```json
{
  "message": "拍卖信息处理 Agent API",
  "version": "1.0.0",
  "endpoints": {
    "query": "/api/query",
    "search": "/api/search",
    "health": "/health"
  }
}
```

### 2. 健康检查

**端点**: `GET /health`

**描述**: 检查服务健康状态

**示例请求**:
```bash
curl http://localhost:8000/health
```

**响应**:
```json
{
  "status": "healthy"
}
```

### 3. 自然语言查询

**端点**: `POST /api/query`

**描述**: 使用自然语言查询拍卖信息,Agent 会自动理解意图并调用相应的工具

**请求体**:
```json
{
  "query": "搜索未来一周内截止的所有硬币拍卖",
  "session_id": "optional-session-id"
}
```

**参数说明**:
- `query` (必需): 自然语言查询字符串
- `session_id` (可选): 会话 ID,用于维持对话上下文

**示例请求**:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "搜索未来一周内截止的所有硬币拍卖"
  }'
```

**响应**:
```json
{
  "response": "根据搜索结果,找到以下拍卖...",
  "session_id": "optional-session-id"
}
```

**更多查询示例**:

查找特定类别的拍卖:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "有哪些代币和奖章的拍卖?"
  }'
```

按关键词搜索:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "查找包含 Silver Dollar 的拍卖"
  }'
```

### 4. 直接搜索

**端点**: `POST /api/search`

**描述**: 使用结构化参数直接搜索拍卖,不需要自然语言处理

**请求体**:
```json
{
  "time_range_days": 7,
  "categories": ["U.S. Coins & Related", "World Coins"],
  "keywords": ["silver", "dollar"],
  "min_lots": 50
}
```

**参数说明**:
- `time_range_days` (可选): 时间范围(天数),例如 7 表示未来 7 天内
- `categories` (可选): 拍卖类别数组
- `keywords` (可选): 搜索关键词数组
- `min_lots` (可选): 最小 Lots 数量

**支持的类别**:
- `U.S. Coins & Related` - 美国硬币及相关
- `World Coins` - 世界硬币
- `U.S. Paper Currency` - 美国纸币
- `World Paper Currency` - 世界纸币
- `Numismatic Americana` - 美国钱币学(代币、奖章等)
- `Ancient Coins` - 古币
- `Bullion` - 金银条

**示例请求**:
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "time_range_days": 7,
    "categories": ["U.S. Coins & Related", "World Coins"]
  }'
```

**响应**:
```json
{
  "count": 2,
  "results": [
    {
      "title": "December 2025 Showcase Auction - Silver Dollars & Double Eagles",
      "date": "2025-12-09",
      "lots_count": 55,
      "category": "U.S. Coins & Related",
      "url": "https://auctions.stacksbowers.com/auctions/session-1"
    },
    {
      "title": "December 2025 World Collectors Choice Online Auction - Coins of Denmark",
      "date": "2025-12-10",
      "lots_count": 334,
      "category": "World Coins",
      "url": "https://auctions.stacksbowers.com/auctions/denmark"
    }
  ]
}
```

**更多搜索示例**:

按类别搜索:
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["Numismatic Americana"]
  }'
```

按关键词搜索:
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["silver", "dollar"]
  }'
```

组合条件搜索:
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "time_range_days": 7,
    "categories": ["U.S. Coins & Related"],
    "min_lots": 100
  }'
```

### 5. 重置对话

**端点**: `POST /api/reset`

**描述**: 重置对话历史,清除之前的上下文

**示例请求**:
```bash
curl -X POST http://localhost:8000/api/reset
```

**响应**:
```json
{
  "message": "对话历史已重置"
}
```

## Python 客户端示例

使用 Python 的 `requests` 库调用 API:

```python
import requests

# API 基础 URL
base_url = "http://localhost:8000"

# 示例 1: 自然语言查询
def query_example():
    response = requests.post(
        f"{base_url}/api/query",
        json={"query": "搜索未来一周内截止的所有硬币拍卖"}
    )
    result = response.json()
    print(result["response"])

# 示例 2: 直接搜索
def search_example():
    response = requests.post(
        f"{base_url}/api/search",
        json={
            "time_range_days": 7,
            "categories": ["U.S. Coins & Related", "World Coins"]
        }
    )
    result = response.json()
    print(f"找到 {result['count']} 个拍卖")
    for auction in result["results"]:
        print(f"- {auction['title']}")

# 运行示例
query_example()
search_example()
```

## JavaScript 客户端示例

使用 JavaScript 的 `fetch` API 调用:

```javascript
// API 基础 URL
const baseUrl = 'http://localhost:8000';

// 示例 1: 自然语言查询
async function queryExample() {
  const response = await fetch(`${baseUrl}/api/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: '搜索未来一周内截止的所有硬币拍卖'
    })
  });
  
  const result = await response.json();
  console.log(result.response);
}

// 示例 2: 直接搜索
async function searchExample() {
  const response = await fetch(`${baseUrl}/api/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      time_range_days: 7,
      categories: ['U.S. Coins & Related', 'World Coins']
    })
  });
  
  const result = await response.json();
  console.log(`找到 ${result.count} 个拍卖`);
  result.results.forEach(auction => {
    console.log(`- ${auction.title}`);
  });
}

// 运行示例
queryExample();
searchExample();
```

## 错误处理

API 使用标准的 HTTP 状态码:

- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数错误
- `500 Internal Server Error`: 服务器内部错误

错误响应格式:
```json
{
  "detail": "错误描述信息"
}
```

## 交互式 API 文档

启动服务器后,可以访问以下 URL 查看交互式 API 文档:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

这些文档提供了可视化的 API 测试界面,可以直接在浏览器中测试 API 端点。

## 部署建议

在生产环境中部署时,建议:

1. 使用反向代理(如 Nginx)处理 HTTPS 和负载均衡
2. 配置适当的 CORS 策略
3. 添加身份验证和授权机制
4. 实施速率限制防止滥用
5. 使用环境变量管理 API 密钥
6. 配置日志记录和监控

## 性能优化

为了提高 API 性能,可以考虑:

1. 实现缓存机制,减少重复的网页抓取
2. 使用异步处理长时间运行的任务
3. 实现请求队列管理并发请求
4. 定期更新本地数据缓存
