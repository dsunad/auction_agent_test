"""
AI 智能浏览器 - 使用 Zyte 浏览器渲染 + AI 文本理解
模拟人类阅读网页的过程，而不是硬编码解析 HTML
"""

import logging
import json
import time
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, ZYTE_API_KEY
import requests
import base64

logger = logging.getLogger(__name__)


class AISmartBrowser:
    """AI 智能浏览器 - 使用 AI 理解页面内容而不是硬编码解析"""
    
    def __init__(self):
        """初始化 AI 智能浏览器"""
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.model = DEEPSEEK_MODEL
        self.zyte_api_key = ZYTE_API_KEY
        self.zyte_url = "https://api.zyte.com/v1/extract"
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """
        获取页面的可读文本内容
        
        Args:
            url: 页面 URL
        
        Returns:
            页面的文本内容
        """
        try:
            # 使用 Zyte API 获取渲染后的 HTML
            auth_string = f"{self.zyte_api_key}:"
            auth_bytes = auth_string.encode('ascii')
            auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {auth_base64}"
            }
            
            payload = {
                "url": url,
                "browserHtml": True
            }
            
            logger.info(f"获取页面内容: {url}")
            response = requests.post(self.zyte_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                html = data.get("browserHtml")
                if html:
                    # 提取可读文本
                    return self._extract_readable_text(html)
                else:
                    logger.error("未获取到 HTML 内容")
                    return None
            else:
                logger.error(f"Zyte API 请求失败: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"获取页面内容失败: {e}")
            return None
    
    def _extract_readable_text(self, html: str) -> str:
        """
        从 HTML 中提取可读的文本内容，保持结构
        
        Args:
            html: HTML 内容
        
        Returns:
            结构化的文本内容
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 移除脚本和样式
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # 提取主要内容
            text_parts = []
            
            # 查找所有可能的拍品容器
            # 使用更通用的选择器
            containers = soup.find_all(['div', 'article', 'li'], 
                                      class_=re.compile(r'(lot|item|product|card)', re.I))
            
            for idx, container in enumerate(containers, 1):
                # 提取容器内的文本
                texts = container.stripped_strings
                container_text = '\n'.join(texts)
                
                if container_text and len(container_text) > 20:  # 过滤太短的内容
                    text_parts.append(f"\n--- Item {idx} ---\n{container_text}")
            
            # 如果没找到容器，就提取所有文本
            if not text_parts:
                text_parts = [soup.get_text(separator='\n', strip=True)]
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            logger.error(f"提取文本失败: {e}")
            return ""
    
    def analyze_content_with_ai(self, content: str, search_query: str, 
                                max_items: int = 50) -> List[Dict]:
        """
        使用 AI 分析页面内容，识别和筛选拍品
        
        Args:
            content: 页面文本内容
            search_query: 搜索要求（自然语言）
            max_items: 最多返回多少个拍品
        
        Returns:
            符合要求的拍品列表
        """
        try:
            # 如果内容太长，分批处理
            content_chunks = self._split_content(content, max_length=8000)
            
            all_items = []
            
            for chunk_idx, chunk in enumerate(content_chunks, 1):
                logger.info(f"使用 AI 分析内容块 {chunk_idx}/{len(content_chunks)}...")
                
                # 构造提示
                prompt = f"""你是一个专业的拍卖网站内容分析助手。我会给你一个拍卖网页的文本内容，你需要：

1. 识别页面上的所有拍品信息
2. 根据搜索要求判断每个拍品的相关性
3. 只返回符合要求的拍品

搜索要求: {search_query}

页面内容:
{chunk}

请以 JSON 格式返回结果，格式如下:
{{
  "items": [
    {{
      "lot_number": "拍品编号",
      "title": "拍品标题",
      "description": "拍品描述",
      "price": "当前价格",
      "relevance_score": 8,
      "reason": "符合要求的理由"
    }}
  ]
}}

注意:
- relevance_score 是 0-10 的评分，10 表示完全符合要求
- 只返回 relevance_score >= 6 的拍品
- 如果信息不完整，用 "N/A" 表示
- 确保返回有效的 JSON 格式
"""
                
                # 调用 AI
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的内容分析助手，擅长识别和筛选拍卖信息。你总是返回有效的 JSON 格式数据。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=4000
                )
                
                result_text = response.choices[0].message.content
                
                # 解析 JSON
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
                    items = result.get('items', [])
                    all_items.extend(items)
                    
                    logger.info(f"内容块 {chunk_idx} 识别到 {len(items)} 个符合要求的拍品")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"解析 JSON 失败: {e}")
                    logger.debug(f"原始响应: {result_text}")
                    continue
            
            # 去重（根据 lot_number）
            unique_items = self._deduplicate_items(all_items)
            
            # 按相关性排序
            unique_items.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # 限制返回数量
            return unique_items[:max_items]
            
        except Exception as e:
            logger.error(f"AI 分析失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _split_content(self, content: str, max_length: int = 8000) -> List[str]:
        """
        将长内容分割成多个块
        
        Args:
            content: 内容
            max_length: 每块最大长度
        
        Returns:
            内容块列表
        """
        if len(content) <= max_length:
            return [content]
        
        chunks = []
        # 按 "--- Item" 分割
        items = content.split('--- Item')
        
        current_chunk = ""
        for item in items:
            if len(current_chunk) + len(item) < max_length:
                current_chunk += "--- Item" + item
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = "--- Item" + item
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks if chunks else [content]
    
    def _deduplicate_items(self, items: List[Dict]) -> List[Dict]:
        """
        根据 lot_number 去重
        
        Args:
            items: 拍品列表
        
        Returns:
            去重后的列表
        """
        seen = set()
        unique = []
        
        for item in items:
            lot_num = item.get('lot_number', '')
            if lot_num and lot_num not in seen:
                seen.add(lot_num)
                unique.append(item)
            elif not lot_num:
                # 没有编号的也保留
                unique.append(item)
        
        return unique
    
    def smart_browse(self, url: str, search_query: str, 
                    max_pages: int = 1) -> List[Dict]:
        """
        智能浏览拍卖页面
        
        Args:
            url: 页面 URL
            search_query: 搜索要求（自然语言，中文或英文都可以）
            max_pages: 最多浏览多少页
        
        Returns:
            符合要求的拍品列表
        """
        all_items = []
        
        for page_num in range(1, max_pages + 1):
            logger.info(f"智能浏览第 {page_num} 页...")
            
            # 构造页面 URL
            page_url = url
            if page_num > 1:
                if '?' in url:
                    page_url = f"{url}&page={page_num}"
                else:
                    page_url = f"{url}?page={page_num}"
            
            # 1. 获取页面内容
            content = self.fetch_page_content(page_url)
            if not content:
                logger.error(f"第 {page_num} 页获取内容失败")
                break
            
            logger.info(f"页面内容长度: {len(content)} 字符")
            
            # 2. 使用 AI 分析内容
            items = self.analyze_content_with_ai(content, search_query)
            all_items.extend(items)
            
            logger.info(f"第 {page_num} 页找到 {len(items)} 个符合要求的拍品")
            
            # 延迟避免请求过快
            if page_num < max_pages:
                time.sleep(2)
        
        logger.info(f"总共找到 {len(all_items)} 个符合要求的拍品")
        return all_items
