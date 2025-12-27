"""
多层级 AI 智能浏览器 - 支持首页→场次→拍品的层级浏览
"""

import logging
from typing import List, Dict, Optional
from ai_smart_browser import AISmartBrowser

logger = logging.getLogger(__name__)


class HierarchicalBrowser:
    """层级浏览器 - 自动发现并遍历多个拍卖场次"""
    
    def __init__(self):
        """初始化层级浏览器"""
        self.browser = AISmartBrowser()
    
    def discover_auctions(self, index_url: str) -> List[Dict]:
        """
        分析拍卖网站首页，发现所有拍卖场次
        
        Args:
            index_url: 拍卖网站首页 URL
        
        Returns:
            拍卖场次列表，每个包含 title, url, date 等信息
        """
        logger.info(f"分析拍卖网站首页: {index_url}")
        
        try:
            # 获取首页内容
            content = self.browser.fetch_page_content(index_url)
            if not content:
                logger.error("无法获取首页内容")
                return []
            
            logger.info(f"首页内容长度: {len(content)} 字符")
            
            # 使用 AI 分析首页，识别所有拍卖场次
            prompt = f"""你是一个专业的拍卖网站分析助手。请分析这个拍卖网站首页，找出所有的拍卖场次。

页面内容:
{content[:15000]}  # 只发送前15000字符避免超限

请识别页面上的所有拍卖场次，并返回 JSON 格式的结果：

{{
  "auctions": [
    {{
      "title": "拍卖场次标题",
      "date": "拍卖日期（如果有）",
      "lots_count": "拍品数量（如果有）",
      "url": "拍卖场次的链接（完整 URL 或相对路径）",
      "category": "拍卖类别（如果有）"
    }}
  ]
}}

注意:
1. 只返回拍卖场次信息，不要返回其他类型的链接
2. URL 可能是完整链接或相对路径（如 /auctions/xxx）
3. 如果某些信息缺失，用 "N/A" 表示
4. 确保返回有效的 JSON 格式
"""
            
            response = self.browser.client.chat.completions.create(
                model=self.browser.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的网页分析助手，擅长识别拍卖网站的结构。你总是返回有效的 JSON 格式数据。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            result_text = response.choices[0].message.content
            
            # 解析 JSON
            import json
            try:
                # 提取 JSON 部分
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                elif "```" in result_text:
                    json_start = result_text.find("```") + 3
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                
                result = json.loads(result_text)
                auctions = result.get('auctions', [])
                
                # 处理 URL（补全相对路径）
                from urllib.parse import urljoin
                for auction in auctions:
                    if 'url' in auction and auction['url']:
                        # 如果是相对路径，补全为完整 URL
                        if not auction['url'].startswith('http'):
                            auction['url'] = urljoin(index_url, auction['url'])
                
                logger.info(f"发现 {len(auctions)} 个拍卖场次")
                return auctions
                
            except json.JSONDecodeError as e:
                logger.error(f"解析 JSON 失败: {e}")
                logger.debug(f"原始响应: {result_text}")
                return []
                
        except Exception as e:
            logger.error(f"分析首页失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def browse_all_auctions(self, index_url: str, search_query: str, 
                           max_auctions: int = None) -> Dict:
        """
        浏览拍卖网站，遍历所有场次并搜索拍品
        
        Args:
            index_url: 拍卖网站首页 URL
            search_query: 搜索要求（自然语言）
            max_auctions: 最多浏览多少个场次（None 表示全部）
        
        Returns:
            结果字典，包含所有场次的拍品
        """
        logger.info(f"开始多层级浏览: {index_url}")
        logger.info(f"搜索要求: {search_query}")
        
        # 1. 发现所有拍卖场次
        auctions = self.discover_auctions(index_url)
        
        if not auctions:
            logger.warning("未发现任何拍卖场次")
            return {
                "success": False,
                "message": "未发现任何拍卖场次",
                "auctions": [],
                "total_lots": 0
            }
        
        logger.info(f"共发现 {len(auctions)} 个拍卖场次")
        
        # 限制场次数量
        if max_auctions:
            auctions = auctions[:max_auctions]
            logger.info(f"限制为前 {max_auctions} 个场次")
        
        # 2. 遍历每个场次，搜索拍品
        all_results = []
        total_lots = 0
        
        for idx, auction in enumerate(auctions, 1):
            auction_title = auction.get('title', 'N/A')
            auction_url = auction.get('url')
            
            if not auction_url:
                logger.warning(f"场次 {idx} 没有 URL，跳过")
                continue
            
            logger.info(f"\n{'='*60}")
            logger.info(f"浏览场次 {idx}/{len(auctions)}: {auction_title}")
            logger.info(f"URL: {auction_url}")
            logger.info(f"{'='*60}")
            
            try:
                # 浏览该场次的拍品
                lots = self.browser.smart_browse(
                    auction_url, 
                    search_query,
                    max_pages=1  # 每个场次只浏览第一页，可调整
                )
                
                # 为每个拍品添加场次信息
                for lot in lots:
                    lot['auction_title'] = auction_title
                    lot['auction_url'] = auction_url
                    lot['auction_date'] = auction.get('date', 'N/A')
                
                logger.info(f"场次 {idx} 找到 {len(lots)} 个符合要求的拍品")
                
                all_results.append({
                    "auction": auction,
                    "lots": lots,
                    "lots_count": len(lots)
                })
                
                total_lots += len(lots)
                
            except Exception as e:
                logger.error(f"浏览场次 {idx} 时出错: {e}")
                continue
        
        logger.info(f"\n{'='*60}")
        logger.info(f"浏览完成！")
        logger.info(f"共浏览 {len(all_results)} 个场次")
        logger.info(f"总共找到 {total_lots} 个符合要求的拍品")
        logger.info(f"{'='*60}")
        
        return {
            "success": True,
            "auctions": all_results,
            "auctions_count": len(all_results),
            "total_lots": total_lots,
            "search_query": search_query
        }
    
    def get_all_matching_lots(self, index_url: str, search_query: str,
                             max_auctions: int = None) -> List[Dict]:
        """
        获取所有符合要求的拍品（扁平化列表）
        
        Args:
            index_url: 拍卖网站首页 URL
            search_query: 搜索要求
            max_auctions: 最多浏览多少个场次
        
        Returns:
            所有符合要求的拍品列表
        """
        result = self.browse_all_auctions(index_url, search_query, max_auctions)
        
        if not result['success']:
            return []
        
        # 扁平化：把所有场次的拍品合并成一个列表
        all_lots = []
        for auction_result in result['auctions']:
            all_lots.extend(auction_result['lots'])
        
        # 按相关性排序
        all_lots.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return all_lots
    
    def export_results(self, result: Dict, output_file: str, format: str = 'json'):
        """
        导出搜索结果
        
        Args:
            result: browse_all_auctions 的返回结果
            output_file: 输出文件名
            format: 格式 ('json', 'csv', 'txt')
        """
        if not result['success']:
            logger.error("无结果可导出")
            return
        
        # 获取所有拍品
        all_lots = []
        for auction_result in result['auctions']:
            all_lots.extend(auction_result['lots'])
        
        # 使用 LotScraper 的保存功能
        from lot_scraper import LotScraper
        scraper = LotScraper()
        scraper.save_lots_to_file(all_lots, output_file, format)
        
        logger.info(f"结果已导出到 {output_file}")
