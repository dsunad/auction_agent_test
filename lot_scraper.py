"""
拍品抓取模块 - 深入拍卖场次获取详细拍品列表
"""

import requests
import json
import base64
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re
import logging
import time
from difflib import SequenceMatcher

from config import ZYTE_API_KEY

logger = logging.getLogger(__name__)


class LotScraper:
    """拍品详细信息抓取器"""
    
    def __init__(self):
        self.zyte_api_key = ZYTE_API_KEY
        self.zyte_url = "https://api.zyte.com/v1/extract"
        
    def fetch_with_zyte(self, url: str) -> Optional[str]:
        """使用 Zyte API 获取页面内容,绕过 Cloudflare"""
        try:
            # Zyte API 需要 Base64 编码的 API key
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
            
            logger.info(f"使用 Zyte API 获取: {url}")
            response = requests.post(self.zyte_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                html = data.get("browserHtml") or data.get("httpResponseBody")
                if html:
                    logger.info(f"成功获取页面内容,长度: {len(html)}")
                    return html
                else:
                    logger.error("Zyte API 返回数据中没有 HTML 内容")
                    return None
            else:
                logger.error(f"Zyte API 请求失败: {response.status_code}, {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Zyte API 调用异常: {e}")
            return None
    
    def parse_lot_list(self, html: str) -> List[Dict]:
        """解析拍品列表页面"""
        lots = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 尝试多种方式查找拍品信息
            # 方法 1: 查找包含 lot 信息的容器
            lot_containers = soup.find_all(['div', 'article', 'li'], class_=re.compile(r'lot|item|product', re.I))
            
            logger.info(f"找到 {len(lot_containers)} 个可能的拍品容器")
            
            for container in lot_containers:
                lot_data = self._extract_lot_from_container(container)
                if lot_data and lot_data.get('lot_number'):
                    lots.append(lot_data)
            
            # 方法 2: 如果方法 1 没找到,尝试从脚本中提取 JSON 数据
            if not lots:
                lots = self._extract_lots_from_scripts(soup)
            
            logger.info(f"成功解析 {len(lots)} 个拍品")
            
        except Exception as e:
            logger.error(f"解析拍品列表失败: {e}")
        
        return lots
    
    def _extract_lot_from_container(self, container) -> Optional[Dict]:
        """从容器中提取拍品信息"""
        try:
            lot_data = {}
            
            # 提取 lot 编号
            lot_num = container.find(text=re.compile(r'\b\d{5,6}\b'))
            if lot_num:
                lot_data['lot_number'] = lot_num.strip()
            
            # 提取标题
            title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name', re.I))
            if title_elem:
                lot_data['title'] = title_elem.get_text(strip=True)
            
            # 提取描述
            desc_elem = container.find(['p', 'div'], class_=re.compile(r'desc|detail', re.I))
            if desc_elem:
                lot_data['description'] = desc_elem.get_text(strip=True)
            
            # 提取价格
            price_elem = container.find(text=re.compile(r'\$\s*\d+'))
            if price_elem:
                price_match = re.search(r'\$\s*(\d+(?:,\d{3})*)', price_elem)
                if price_match:
                    lot_data['current_bid'] = price_match.group(1).replace(',', '')
            
            # 提取图片
            img_elem = container.find('img')
            if img_elem and img_elem.get('src'):
                lot_data['image_url'] = img_elem['src']
            
            return lot_data if lot_data else None
            
        except Exception as e:
            logger.debug(f"从容器提取拍品信息失败: {e}")
            return None
    
    def _extract_lots_from_scripts(self, soup) -> List[Dict]:
        """从页面脚本中提取 JSON 格式的拍品数据"""
        lots = []
        
        try:
            # 查找所有 script 标签
            scripts = soup.find_all('script', type='application/json')
            
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    # 递归查找可能包含拍品信息的数据
                    lots.extend(self._find_lots_in_json(data))
                except:
                    continue
            
            # 也尝试查找普通的 JavaScript 变量
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # 查找类似 var lots = [...] 的模式
                    matches = re.findall(r'(?:var|const|let)\s+\w*lots?\w*\s*=\s*(\[.+?\]);', script.string, re.DOTALL)
                    for match in matches:
                        try:
                            data = json.loads(match)
                            if isinstance(data, list):
                                lots.extend(data)
                        except:
                            continue
        
        except Exception as e:
            logger.error(f"从脚本提取拍品数据失败: {e}")
        
        return lots
    
    def _find_lots_in_json(self, data, depth=0, max_depth=5) -> List[Dict]:
        """递归查找 JSON 数据中的拍品信息"""
        lots = []
        
        if depth > max_depth:
            return lots
        
        if isinstance(data, dict):
            # 检查是否是拍品对象
            if 'lot_number' in data or 'lotNumber' in data or 'lot' in data:
                lots.append(data)
            else:
                # 递归查找
                for value in data.values():
                    lots.extend(self._find_lots_in_json(value, depth + 1, max_depth))
        
        elif isinstance(data, list):
            for item in data:
                lots.extend(self._find_lots_in_json(item, depth + 1, max_depth))
        
        return lots
    
    def get_all_lots_from_auction(self, auction_url: str, max_pages: int = 20) -> List[Dict]:
        """
        获取拍卖场次的所有拍品
        
        Args:
            auction_url: 拍卖场次 URL
            max_pages: 最大抓取页数
        
        Returns:
            拍品列表
        """
        all_lots = []
        
        logger.info(f"开始获取拍卖场次的所有拍品: {auction_url}")
        
        # 第一页
        html = self.fetch_with_zyte(auction_url)
        if html:
            lots = self.parse_lot_list(html)
            all_lots.extend(lots)
            logger.info(f"第 1 页: 找到 {len(lots)} 个拍品")
            
            # 检查是否有分页
            soup = BeautifulSoup(html, 'html.parser')
            total_pages = self._get_total_pages(soup)
            
            if total_pages > 1:
                logger.info(f"检测到 {total_pages} 页,开始抓取后续页面")
                
                for page in range(2, min(total_pages + 1, max_pages + 1)):
                    # 构造分页 URL (需要根据实际网站调整)
                    page_url = self._build_page_url(auction_url, page)
                    
                    logger.info(f"抓取第 {page} 页: {page_url}")
                    html = self.fetch_with_zyte(page_url)
                    
                    if html:
                        lots = self.parse_lot_list(html)
                        all_lots.extend(lots)
                        logger.info(f"第 {page} 页: 找到 {len(lots)} 个拍品")
                    
                    # 避免请求过快
                    time.sleep(2)
        
        logger.info(f"总共获取 {len(all_lots)} 个拍品")
        return all_lots
    
    def _get_total_pages(self, soup) -> int:
        """获取总页数"""
        try:
            # 查找分页信息
            pagination = soup.find(['div', 'nav'], class_=re.compile(r'pag', re.I))
            if pagination:
                # 查找页码
                page_links = pagination.find_all('a', href=True)
                page_numbers = []
                
                for link in page_links:
                    text = link.get_text(strip=True)
                    if text.isdigit():
                        page_numbers.append(int(text))
                
                if page_numbers:
                    return max(page_numbers)
            
            # 尝试从文本中提取 "Page 1 of 14" 这样的信息
            page_info = soup.find(text=re.compile(r'Page\s+\d+\s+of\s+(\d+)', re.I))
            if page_info:
                match = re.search(r'of\s+(\d+)', page_info, re.I)
                if match:
                    return int(match.group(1))
        
        except Exception as e:
            logger.debug(f"获取总页数失败: {e}")
        
        return 1
    
    def _build_page_url(self, base_url: str, page: int) -> str:
        """构造分页 URL"""
        # 根据实际网站的分页参数调整
        if '?' in base_url:
            return f"{base_url}&page={page}"
        else:
            return f"{base_url}?page={page}"
    
    def filter_lots_by_keyword(self, lots: List[Dict], keywords: List[str], 
                               fuzzy_match: bool = True, min_score: float = 0.6) -> List[Dict]:
        """
        按关键词过滤拍品（支持智能匹配）
        
        Args:
            lots: 拍品列表
            keywords: 关键词列表
            fuzzy_match: 是否启用模糊匹配
            min_score: 模糊匹配的最小相似度分数（0-1）
        
        Returns:
            过滤后的拍品列表（按相关性评分排序）
        """
        if not keywords:
            return lots
        
        filtered = []
        
        for lot in lots:
            # 在标题和描述中搜索关键词
            title = lot.get('title', '').lower()
            description = lot.get('description', '').lower()
            content = f"{title} {description}"
            
            # 计算相关性评分
            score, matched_keywords = self._calculate_relevance_score(
                content, keywords, fuzzy_match, min_score
            )
            
            if score > 0:
                lot_copy = lot.copy()
                lot_copy['_relevance_score'] = score
                lot_copy['_matched_keywords'] = matched_keywords
                filtered.append(lot_copy)
        
        # 按相关性评分排序
        filtered.sort(key=lambda x: x.get('_relevance_score', 0), reverse=True)
        
        logger.info(f"关键词过滤: {len(lots)} -> {len(filtered)}")
        if filtered:
            logger.info(f"最高相关性分数: {filtered[0].get('_relevance_score', 0):.2f}")
        
        return filtered
    
    def _calculate_relevance_score(self, content: str, keywords: List[str], 
                                   fuzzy_match: bool, min_score: float) -> tuple:
        """
        计算内容与关键词的相关性评分
        
        Args:
            content: 要搜索的内容
            keywords: 关键词列表
            fuzzy_match: 是否启用模糊匹配
            min_score: 最小匹配分数
        
        Returns:
            (总分, 匹配的关键词列表)
        """
        score = 0
        matched_keywords = []
        content_lower = content.lower()
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # 1. 完全匹配（最高分）
            if keyword_lower in content_lower:
                score += 10
                matched_keywords.append((keyword, 'exact', 1.0))
                continue
            
            # 2. 单词级别匹配
            keyword_words = re.findall(r'\b\w+\b', keyword_lower)
            word_matches = sum(1 for kw in keyword_words if kw in content_words)
            if word_matches > 0:
                word_score = (word_matches / len(keyword_words)) * 5
                score += word_score
                matched_keywords.append((keyword, 'partial', word_matches / len(keyword_words)))
                continue
            
            # 3. 模糊匹配（如果启用）
            if fuzzy_match:
                best_ratio = 0
                for content_word in content_words:
                    ratio = SequenceMatcher(None, keyword_lower, content_word).ratio()
                    best_ratio = max(best_ratio, ratio)
                
                if best_ratio >= min_score:
                    score += best_ratio * 3
                    matched_keywords.append((keyword, 'fuzzy', best_ratio))
        
        return score, matched_keywords
    
    def search_lots_intelligently(self, lots: List[Dict], query: str, 
                                  fuzzy_match: bool = True) -> List[Dict]:
        """
        智能搜索拍品（自动提取查询词并应用同义词扩展）
        
        Args:
            lots: 拍品列表
            query: 搜索查询（自然语言）
            fuzzy_match: 是否启用模糊匹配
        
        Returns:
            匹配的拍品列表
        """
        # 提取关键词
        keywords = self._extract_keywords_from_query(query)
        
        # 扩展同义词
        keywords = self._expand_synonyms(keywords)
        
        logger.info(f"搜索关键词: {keywords}")
        
        # 使用增强的过滤功能
        return self.filter_lots_by_keyword(lots, keywords, fuzzy_match)
    
    def _extract_keywords_from_query(self, query: str) -> List[str]:
        """
        从查询中提取关键词
        
        Args:
            query: 自然语言查询
        
        Returns:
            关键词列表
        """
        # 移除常见的停用词
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
                     'including', 'all', 'any', 'some', 'find', 'search', 'get', 'show', 'list'}
        
        # 提取单词
        words = re.findall(r'\b\w+\b', query.lower())
        
        # 过滤停用词
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def _expand_synonyms(self, keywords: List[str]) -> List[str]:
        """
        扩展关键词的同义词
        
        Args:
            keywords: 原始关键词列表
        
        Returns:
            扩展后的关键词列表
        """
        # 常见同义词映射（可以扩展）
        synonyms = {
            'gold': ['golden', 'au', 'aurum'],
            'silver': ['ag', 'argentum'],
            'coin': ['coins', 'coinage'],
            'dollar': ['dollars', 'usd'],
            'penny': ['pennies', 'cent', 'cents'],
            'rare': ['scarce', 'uncommon', 'unique'],
            'ancient': ['antique', 'old', 'historical'],
            'morgan': ['morgan dollar'],
            'eagle': ['double eagle', 'half eagle'],
        }
        
        expanded = list(keywords)
        for keyword in keywords:
            if keyword.lower() in synonyms:
                expanded.extend(synonyms[keyword.lower()])
        
        return list(set(expanded))  # 去重
    
    def save_lots_to_file(self, lots: List[Dict], filename: str, format: str = 'json'):
        """
        保存拍品到文件
        
        Args:
            lots: 拍品列表
            filename: 文件名
            format: 格式 ('json', 'csv', 'txt')
        """
        try:
            if format == 'json':
                self._save_as_json(lots, filename)
            elif format == 'csv':
                self._save_as_csv(lots, filename)
            elif format == 'txt':
                self._save_as_txt(lots, filename)
            else:
                logger.error(f"不支持的格式: {format}")
        
        except Exception as e:
            logger.error(f"保存文件失败: {e}")
    
    def _save_as_json(self, lots: List[Dict], filename: str):
        """保存为 JSON 格式"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(lots, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存 {len(lots)} 个拍品到 {filename}")
    
    def _save_as_csv(self, lots: List[Dict], filename: str):
        """保存为 CSV 格式"""
        import csv
        
        if not lots:
            return
        
        # 获取所有字段
        fields = set()
        for lot in lots:
            fields.update(lot.keys())
        fields = sorted(list(fields))
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(lots)
        
        logger.info(f"已保存 {len(lots)} 个拍品到 {filename}")
    
    def _save_as_txt(self, lots: List[Dict], filename: str):
        """保存为文本格式"""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, lot in enumerate(lots, 1):
                f.write(f"{'='*60}\n")
                f.write(f"拍品 #{i}\n")
                f.write(f"{'='*60}\n")
                
                for key, value in lot.items():
                    f.write(f"{key}: {value}\n")
                
                f.write("\n")
        
        logger.info(f"已保存 {len(lots)} 个拍品到 {filename}")
