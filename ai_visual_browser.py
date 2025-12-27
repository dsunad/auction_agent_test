"""
AI 视觉浏览器 - 使用 AI 视觉理解来"阅读"网页，而不是解析 HTML
模拟人类浏览网页的过程：看->理解->判断->点击
"""

import logging
import base64
import json
import time
from typing import List, Dict, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

logger = logging.getLogger(__name__)


class AIVisualBrowser:
    """AI 视觉浏览器 - 使用 AI 视觉理解代替传统 HTML 解析"""
    
    def __init__(self):
        """初始化 AI 视觉浏览器"""
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.model = DEEPSEEK_MODEL
        self.driver = None
        self._init_browser()
    
    def _init_browser(self):
        """初始化浏览器"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("浏览器初始化成功")
        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            self.driver = None
    
    def take_screenshot(self, element=None) -> str:
        """
        截取网页或元素的截图
        
        Args:
            element: 要截图的元素，None 表示整个页面
        
        Returns:
            base64 编码的截图
        """
        try:
            if element:
                screenshot = element.screenshot_as_base64
            else:
                screenshot = self.driver.get_screenshot_as_base64()
            return screenshot
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    def analyze_page_with_ai(self, screenshot_base64: str, task: str) -> Dict:
        """
        使用 AI 分析网页截图
        
        Args:
            screenshot_base64: base64 编码的截图
            task: 要执行的任务描述
        
        Returns:
            AI 分析结果
        """
        try:
            # 构造消息
            messages = [
                {
                    "role": "system",
                    "content": """你是一个专业的网页分析助手。你的任务是分析网页截图，识别拍品信息。

你需要返回 JSON 格式的结果，包含以下信息：
- items: 识别到的拍品列表，每个拍品包含：
  - title: 拍品标题
  - description: 拍品描述
  - price: 当前价格
  - lot_number: 拍品编号
  - relevance_score: 与搜索要求的相关性评分 (0-10)
  - reason: 相关性判断理由
  - position: 拍品在页面上的大致位置 (top/middle/bottom, left/center/right)

请仔细观察图片中的所有拍品信息，包括标题、描述、价格等。"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{screenshot_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": task
                        }
                    ]
                }
            ]
            
            # 调用 AI 视觉理解
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=4000
            )
            
            result_text = response.choices[0].message.content
            
            # 尝试解析 JSON
            try:
                # 提取 JSON 部分（可能被包裹在 ```json ... ``` 中）
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                elif "```" in result_text:
                    json_start = result_text.find("```") + 3
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError:
                logger.warning("AI 返回的不是有效的 JSON，返回原始文本")
                return {"raw_text": result_text, "items": []}
                
        except Exception as e:
            logger.error(f"AI 分析失败: {e}")
            return {"error": str(e), "items": []}
    
    def browse_auction_page(self, url: str, search_query: str) -> List[Dict]:
        """
        智能浏览拍卖页面，使用 AI 视觉理解识别和筛选拍品
        
        Args:
            url: 拍卖页面 URL
            search_query: 搜索要求（自然语言）
        
        Returns:
            符合要求的拍品列表
        """
        if not self.driver:
            logger.error("浏览器未初始化")
            return []
        
        try:
            logger.info(f"开始智能浏览: {url}")
            logger.info(f"搜索要求: {search_query}")
            
            # 1. 打开页面
            self.driver.get(url)
            time.sleep(3)  # 等待页面加载
            
            # 2. 截取整个页面
            logger.info("截取页面截图...")
            screenshot = self.take_screenshot()
            
            if not screenshot:
                logger.error("截图失败")
                return []
            
            # 3. 使用 AI 分析页面
            logger.info("使用 AI 分析页面内容...")
            task = f"""
请分析这个拍卖网站页面，找出所有拍品。

搜索要求: {search_query}

请识别页面上的每个拍品，并判断它们是否符合上述搜索要求。
为每个拍品打分（0-10分），10分表示完全符合要求，0分表示完全不符合。
只返回评分大于等于 5 分的拍品。

请以 JSON 格式返回结果。
"""
            
            result = self.analyze_page_with_ai(screenshot, task)
            
            # 4. 处理结果
            items = result.get('items', [])
            logger.info(f"AI 识别到 {len(items)} 个符合要求的拍品")
            
            # 5. 对于高分拍品，尝试获取详细信息
            detailed_items = []
            for item in items:
                score = item.get('relevance_score', 0)
                if score >= 7:  # 高相关性
                    # 尝试获取详细信息
                    detailed = self._get_item_details(item, url)
                    if detailed:
                        detailed_items.append(detailed)
                    else:
                        detailed_items.append(item)
                else:
                    detailed_items.append(item)
            
            return detailed_items
            
        except Exception as e:
            logger.error(f"智能浏览失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_item_details(self, item: Dict, base_url: str) -> Optional[Dict]:
        """
        获取拍品详细信息（模拟点击进入详情页）
        
        Args:
            item: 拍品基本信息
            base_url: 基础 URL
        
        Returns:
            详细信息
        """
        try:
            # 尝试通过 lot_number 构造详情页 URL
            lot_number = item.get('lot_number')
            if not lot_number:
                return None
            
            # TODO: 根据实际网站结构构造详情页 URL
            # 这里需要根据具体网站调整
            logger.info(f"尝试获取拍品 {lot_number} 的详细信息...")
            
            # 暂时返回原始信息
            return item
            
        except Exception as e:
            logger.error(f"获取详细信息失败: {e}")
            return None
    
    def browse_multiple_pages(self, url: str, search_query: str, 
                             max_pages: int = 5) -> List[Dict]:
        """
        浏览多个页面
        
        Args:
            url: 起始页面 URL
            search_query: 搜索要求
            max_pages: 最大页数
        
        Returns:
            所有符合要求的拍品
        """
        all_items = []
        
        for page_num in range(1, max_pages + 1):
            logger.info(f"浏览第 {page_num} 页...")
            
            # 构造页面 URL
            page_url = url
            if page_num > 1:
                # 根据实际网站的分页参数调整
                if '?' in url:
                    page_url = f"{url}&page={page_num}"
                else:
                    page_url = f"{url}?page={page_num}"
            
            # 浏览页面
            items = self.browse_auction_page(page_url, search_query)
            all_items.extend(items)
            
            logger.info(f"第 {page_num} 页找到 {len(items)} 个符合要求的拍品")
            
            # 检查是否还有下一页
            if not self._has_next_page():
                logger.info("没有更多页面了")
                break
            
            time.sleep(2)  # 避免请求过快
        
        logger.info(f"总共找到 {len(all_items)} 个符合要求的拍品")
        return all_items
    
    def _has_next_page(self) -> bool:
        """
        检查是否有下一页
        
        Returns:
            是否有下一页
        """
        try:
            # 使用 AI 分析页面判断是否有下一页
            screenshot = self.take_screenshot()
            if not screenshot:
                return False
            
            task = "请查看页面底部，判断是否有'下一页'或'Next'按钮。如果有，返回 {\"has_next\": true}，否则返回 {\"has_next\": false}"
            result = self.analyze_page_with_ai(screenshot, task)
            
            return result.get('has_next', False)
        except:
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
