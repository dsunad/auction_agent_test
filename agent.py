"""
Agent 核心模块 - 使用 DeepSeek LLM 处理用户指令
"""

import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from openai import OpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from scraper import AuctionScraper

logger = logging.getLogger(__name__)


class AuctionAgent:
    """拍卖信息处理 Agent"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.scraper = AuctionScraper()
        self.model = DEEPSEEK_MODEL
        self.conversation_history = []
        
        # 定义工具函数
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_auctions",
                    "description": "搜索拍卖信息,支持按时间范围、类别、关键词等条件过滤",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time_range_days": {
                                "type": "integer",
                                "description": "时间范围(天数),例如 7 表示未来 7 天内"
                            },
                            "categories": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "拍卖类别,如 ['U.S. Coins & Related', 'World Coins']"
                            },
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "搜索关键词"
                            },
                            "min_lots": {
                                "type": "integer",
                                "description": "最小 Lots 数量"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_auction_details",
                    "description": "获取特定拍卖的详细信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "auction_id": {
                                "type": "string",
                                "description": "拍卖 ID 或 URL"
                            }
                        },
                        "required": ["auction_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "filter_by_price",
                    "description": "按价格范围过滤拍卖项目",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "min_price": {
                                "type": "number",
                                "description": "最低价格"
                            },
                            "max_price": {
                                "type": "number",
                                "description": "最高价格"
                            }
                        },
                        "required": []
                    }
                }
            }
        ]
    
    def search_auctions(self, time_range_days: Optional[int] = None, 
                       categories: Optional[List[str]] = None,
                       keywords: Optional[List[str]] = None,
                       min_lots: Optional[int] = None) -> List[Dict]:
        """搜索拍卖信息"""
        logger.info(f"搜索拍卖: time_range={time_range_days}, categories={categories}, keywords={keywords}")
        
        # 获取所有拍卖数据
        # 这里使用简化的实现,实际应该从网站抓取
        auctions = self._get_mock_auctions()
        
        # 应用过滤条件
        filtered = auctions
        
        if time_range_days:
            cutoff_date = datetime.now() + timedelta(days=time_range_days)
            filtered = [a for a in filtered if self._parse_date(a.get('date', '')) <= cutoff_date]
        
        if categories:
            filtered = [a for a in filtered if any(cat in a.get('title', '') for cat in categories)]
        
        if keywords:
            filtered = [a for a in filtered if any(kw.lower() in a.get('title', '').lower() for kw in keywords)]
        
        if min_lots:
            filtered = [a for a in filtered if a.get('lots_count', 0) >= min_lots]
        
        return filtered
    
    def get_auction_details(self, auction_id: str) -> Dict:
        """获取拍卖详情"""
        logger.info(f"获取拍卖详情: {auction_id}")
        
        # 实际实现应该调用 scraper 获取详细信息
        return {"auction_id": auction_id, "details": "详细信息"}
    
    def filter_by_price(self, min_price: Optional[float] = None, 
                       max_price: Optional[float] = None) -> List[Dict]:
        """按价格过滤"""
        logger.info(f"按价格过滤: min={min_price}, max={max_price}")
        return []
    
    def _parse_date(self, date_str: str) -> datetime:
        """解析日期字符串"""
        try:
            # 简化实现,实际需要更复杂的日期解析
            return datetime.strptime(date_str, "%Y-%m-%d")
        except:
            return datetime.now() + timedelta(days=365)
    
    def _get_mock_auctions(self) -> List[Dict]:
        """获取模拟拍卖数据(用于测试)"""
        return [
            {
                "title": "December 2025 Collectors Choice Online Auction - Tokens & Medals",
                "date": "2025-12-05",
                "lots_count": 476,
                "category": "Numismatic Americana",
                "url": "https://auctions.stacksbowers.com/auctions/3-1NZHVT"
            },
            {
                "title": "December 2025 Showcase Auction - Session 1 - Silver Dollars & Double Eagles",
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
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> str:
        """执行工具函数"""
        if tool_name == "search_auctions":
            result = self.search_auctions(**arguments)
        elif tool_name == "get_auction_details":
            result = self.get_auction_details(**arguments)
        elif tool_name == "filter_by_price":
            result = self.filter_by_price(**arguments)
        else:
            result = {"error": f"未知的工具: {tool_name}"}
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def process_command(self, user_input: str) -> str:
        """处理用户指令"""
        logger.info(f"处理用户指令: {user_input}")
        
        # 添加用户消息到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # 系统提示
        system_message = {
            "role": "system",
            "content": """你是一个拍卖信息处理助手。你可以帮助用户搜索和分析 Stacks Bowers 拍卖网站上的拍卖信息。

你有以下工具可以使用:
1. search_auctions: 搜索拍卖,支持按时间、类别、关键词过滤
2. get_auction_details: 获取特定拍卖的详细信息
3. filter_by_price: 按价格范围过滤

当用户提出请求时,你需要:
1. 理解用户的意图
2. 提取关键参数(时间范围、类别、关键词等)
3. 调用合适的工具
4. 将结果以清晰的方式呈现给用户

类别映射:
- "硬币" 或 "coins" -> ["U.S. Coins & Related", "World Coins"]
- "纸币" 或 "currency" -> ["U.S. Paper Currency", "World Paper Currency"]
- "代币" 或 "tokens" -> ["Numismatic Americana"]
- "古币" 或 "ancient" -> ["Ancient Coins"]
"""
        }
        
        messages = [system_message] + self.conversation_history
        
        # 调用 LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            
            # 检查是否需要调用工具
            if response_message.tool_calls:
                # 执行工具调用
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"调用工具: {function_name}, 参数: {function_args}")
                    
                    # 执行工具
                    function_result = self.execute_tool(function_name, function_args)
                    
                    # 添加工具调用和结果到对话历史
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call.model_dump()]
                    })
                    
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": function_result
                    })
                
                # 再次调用 LLM 生成最终回复
                second_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[system_message] + self.conversation_history
                )
                
                final_message = second_response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_message
                })
                
                return final_message
            else:
                # 直接返回 LLM 的回复
                content = response_message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": content
                })
                return content
                
        except Exception as e:
            logger.error(f"处理指令时出错: {e}")
            return f"抱歉,处理您的请求时出现错误: {str(e)}"
    
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []
        logger.info("对话历史已重置")
