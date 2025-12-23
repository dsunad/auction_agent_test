"""
Agent 核心模块 V2 - 增强版,支持深入拍卖场次获取拍品列表
"""

import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from openai import OpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from scraper import AuctionScraper
from lot_scraper import LotScraper

logger = logging.getLogger(__name__)


class AuctionAgentV2:
    """增强版拍卖信息处理 Agent"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.scraper = AuctionScraper()
        self.lot_scraper = LotScraper()
        self.model = DEEPSEEK_MODEL
        self.conversation_history = []
        
        # 定义工具函数
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_auctions",
                    "description": "搜索拍卖场次信息,支持按时间范围、类别、关键词等条件过滤",
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
                    "name": "get_lots_from_auction",
                    "description": "深入特定拍卖场次,获取所有拍品的详细信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "auction_url": {
                                "type": "string",
                                "description": "拍卖场次的 URL"
                            },
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "用于过滤拍品的关键词(可选)"
                            },
                            "max_pages": {
                                "type": "integer",
                                "description": "最大抓取页数,默认 20"
                            }
                        },
                        "required": ["auction_url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_lots_to_file",
                    "description": "将拍品信息保存到文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lots_data": {
                                "type": "string",
                                "description": "拍品数据的 JSON 字符串"
                            },
                            "filename": {
                                "type": "string",
                                "description": "保存的文件名"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["json", "csv", "txt"],
                                "description": "文件格式"
                            }
                        },
                        "required": ["lots_data", "filename"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_and_export_lots",
                    "description": "搜索拍卖场次,获取所有拍品,按关键词过滤,并导出到文件。这是一个组合操作。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "auction_criteria": {
                                "type": "object",
                                "description": "拍卖场次搜索条件",
                                "properties": {
                                    "time_range_days": {"type": "integer"},
                                    "categories": {"type": "array", "items": {"type": "string"}},
                                    "keywords": {"type": "array", "items": {"type": "string"}}
                                }
                            },
                            "lot_keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "用于过滤拍品的关键词"
                            },
                            "output_file": {
                                "type": "string",
                                "description": "输出文件名"
                            },
                            "output_format": {
                                "type": "string",
                                "enum": ["json", "csv", "txt"],
                                "description": "输出格式"
                            }
                        },
                        "required": ["output_file"]
                    }
                }
            }
        ]
    
    def search_auctions(self, time_range_days: Optional[int] = None, 
                       categories: Optional[List[str]] = None,
                       keywords: Optional[List[str]] = None,
                       min_lots: Optional[int] = None) -> List[Dict]:
        """搜索拍卖场次信息"""
        logger.info(f"搜索拍卖: time_range={time_range_days}, categories={categories}, keywords={keywords}")
        
        # 获取所有拍卖数据
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
    
    def get_lots_from_auction(self, auction_url: str, 
                             keywords: Optional[List[str]] = None,
                             max_pages: int = 20) -> List[Dict]:
        """
        深入拍卖场次获取所有拍品
        
        Args:
            auction_url: 拍卖场次 URL
            keywords: 过滤关键词
            max_pages: 最大抓取页数
        
        Returns:
            拍品列表
        """
        logger.info(f"获取拍卖场次的拍品: {auction_url}")
        
        # 使用 Zyte API 获取所有拍品
        all_lots = self.lot_scraper.get_all_lots_from_auction(auction_url, max_pages)
        
        # 如果指定了关键词,进行过滤
        if keywords:
            all_lots = self.lot_scraper.filter_lots_by_keyword(all_lots, keywords)
        
        return all_lots
    
    def save_lots_to_file(self, lots_data: str, filename: str, format: str = 'json'):
        """
        保存拍品到文件
        
        Args:
            lots_data: 拍品数据的 JSON 字符串
            filename: 文件名
            format: 格式
        """
        try:
            lots = json.loads(lots_data)
            self.lot_scraper.save_lots_to_file(lots, filename, format)
            return {"success": True, "filename": filename, "count": len(lots)}
        except Exception as e:
            logger.error(f"保存文件失败: {e}")
            return {"success": False, "error": str(e)}
    
    def search_and_export_lots(self, 
                              auction_criteria: Optional[Dict] = None,
                              lot_keywords: Optional[List[str]] = None,
                              output_file: str = "auction_lots.json",
                              output_format: str = "json") -> Dict:
        """
        组合操作: 搜索拍卖 -> 获取拍品 -> 过滤 -> 导出
        
        Args:
            auction_criteria: 拍卖场次搜索条件
            lot_keywords: 拍品关键词
            output_file: 输出文件
            output_format: 输出格式
        
        Returns:
            操作结果
        """
        logger.info("执行组合操作: 搜索拍卖 -> 获取拍品 -> 导出")
        
        # 1. 搜索拍卖场次
        criteria = auction_criteria or {}
        auctions = self.search_auctions(**criteria)
        
        if not auctions:
            return {
                "success": False,
                "message": "未找到符合条件的拍卖场次"
            }
        
        logger.info(f"找到 {len(auctions)} 个拍卖场次")
        
        # 2. 获取所有拍品
        all_lots = []
        for auction in auctions:
            url = auction.get('url')
            if url:
                logger.info(f"获取拍卖场次的拍品: {auction.get('title')}")
                lots = self.get_lots_from_auction(url, lot_keywords)
                
                # 添加拍卖场次信息到每个拍品
                for lot in lots:
                    lot['auction_title'] = auction.get('title')
                    lot['auction_date'] = auction.get('date')
                    lot['auction_url'] = url
                
                all_lots.extend(lots)
        
        logger.info(f"总共获取 {len(all_lots)} 个拍品")
        
        # 3. 保存到文件
        self.lot_scraper.save_lots_to_file(all_lots, output_file, output_format)
        
        return {
            "success": True,
            "auctions_count": len(auctions),
            "lots_count": len(all_lots),
            "output_file": output_file,
            "output_format": output_format
        }
    
    def _parse_date(self, date_str: str) -> datetime:
        """解析日期字符串"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except:
            return datetime.now() + timedelta(days=365)
    
    def _get_mock_auctions(self) -> List[Dict]:
        """获取模拟拍卖数据"""
        return [
            {
                "title": "December 2025 Collectors Choice Online Auction - Tokens & Medals",
                "date": "2025-12-05",
                "lots_count": 476,
                "category": "Numismatic Americana",
                "url": "https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475"
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
        elif tool_name == "get_lots_from_auction":
            result = self.get_lots_from_auction(**arguments)
        elif tool_name == "save_lots_to_file":
            result = self.save_lots_to_file(**arguments)
        elif tool_name == "search_and_export_lots":
            result = self.search_and_export_lots(**arguments)
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
1. search_auctions: 搜索拍卖场次,支持按时间、类别、关键词过滤
2. get_lots_from_auction: 深入特定拍卖场次,获取所有拍品的详细信息
3. save_lots_to_file: 将拍品信息保存到文件(JSON/CSV/TXT)
4. search_and_export_lots: 组合操作 - 搜索拍卖、获取拍品、过滤并导出

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

重要功能:
- 当用户需要获取拍品详细信息时,使用 get_lots_from_auction
- 当用户需要导出数据时,使用 save_lots_to_file 或 search_and_export_lots
- search_and_export_lots 是最强大的工具,可以一次性完成搜索、获取、过滤和导出
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
