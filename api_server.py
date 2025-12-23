"""
Web API 服务 - 提供 RESTful API 接口
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

from agent import AuctionAgent

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="拍卖信息处理 Agent API",
    description="提供拍卖信息搜索和查询服务",
    version="1.0.0"
)

# 全局 Agent 实例
agent = AuctionAgent()


class QueryRequest(BaseModel):
    """查询请求模型"""
    query: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    """查询响应模型"""
    response: str
    session_id: Optional[str] = None


class SearchRequest(BaseModel):
    """搜索请求模型"""
    time_range_days: Optional[int] = None
    categories: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    min_lots: Optional[int] = None


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "拍卖信息处理 Agent API",
        "version": "1.0.0",
        "endpoints": {
            "query": "/api/query",
            "search": "/api/search",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    处理自然语言查询
    
    示例:
    ```json
    {
        "query": "搜索未来一周内截止的所有硬币拍卖"
    }
    ```
    """
    try:
        logger.info(f"收到查询: {request.query}")
        response = agent.process_command(request.query)
        
        return QueryResponse(
            response=response,
            session_id=request.session_id
        )
    except Exception as e:
        logger.error(f"处理查询时出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search")
async def search(request: SearchRequest):
    """
    直接搜索拍卖
    
    示例:
    ```json
    {
        "time_range_days": 7,
        "categories": ["U.S. Coins & Related", "World Coins"],
        "keywords": ["silver", "dollar"]
    }
    ```
    """
    try:
        logger.info(f"收到搜索请求: {request.dict()}")
        
        results = agent.search_auctions(
            time_range_days=request.time_range_days,
            categories=request.categories,
            keywords=request.keywords,
            min_lots=request.min_lots
        )
        
        return {
            "count": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"搜索时出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reset")
async def reset_conversation():
    """重置对话历史"""
    try:
        agent.reset_conversation()
        return {"message": "对话历史已重置"}
    except Exception as e:
        logger.error(f"重置对话时出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """启动服务器"""
    logger.info(f"启动 API 服务器: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
