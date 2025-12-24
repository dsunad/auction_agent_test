"""
测试智能搜索功能
"""

import logging
from lot_scraper import LotScraper

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_keyword_extraction():
    """测试关键词提取"""
    scraper = LotScraper()
    
    test_queries = [
        "找出所有金币",
        "search for silver dollar",
        "我想要 Morgan 硬币",
        "find rare ancient coins"
    ]
    
    print("=" * 60)
    print("测试关键词提取")
    print("=" * 60)
    
    for query in test_queries:
        keywords = scraper._extract_keywords_from_query(query)
        print(f"查询: {query}")
        print(f"关键词: {keywords}")
        print()

def test_synonym_expansion():
    """测试同义词扩展"""
    scraper = LotScraper()
    
    test_keywords = [
        ["gold", "coin"],
        ["silver", "dollar"],
        ["rare", "ancient"],
        ["morgan", "eagle"]
    ]
    
    print("=" * 60)
    print("测试同义词扩展")
    print("=" * 60)
    
    for keywords in test_keywords:
        expanded = scraper._expand_synonyms(keywords)
        print(f"原始: {keywords}")
        print(f"扩展: {expanded}")
        print()

def test_relevance_scoring():
    """测试相关性评分"""
    scraper = LotScraper()
    
    # 模拟拍品数据
    test_lots = [
        {
            "lot_number": "001",
            "title": "1921 Morgan Silver Dollar",
            "description": "Beautiful silver coin in excellent condition"
        },
        {
            "lot_number": "002",
            "title": "Ancient Gold Coin",
            "description": "Rare golden coin from Roman era"
        },
        {
            "lot_number": "003",
            "title": "Double Eagle Gold Coin",
            "description": "US gold coin, AU grade"
        },
        {
            "lot_number": "004",
            "title": "Bronze Medal",
            "description": "Commemorative bronze piece"
        }
    ]
    
    test_keywords = ["silver", "dollar"]
    
    print("=" * 60)
    print("测试相关性评分")
    print("=" * 60)
    print(f"搜索关键词: {test_keywords}\n")
    
    for lot in test_lots:
        content = f"{lot['title']} {lot['description']}".lower()
        score, matched = scraper._calculate_relevance_score(
            content, test_keywords, fuzzy_match=True, min_score=0.6
        )
        print(f"拍品 #{lot['lot_number']}: {lot['title']}")
        print(f"  评分: {score:.2f}")
        print(f"  匹配: {matched}")
        print()

def test_filter_with_fuzzy():
    """测试模糊匹配过滤"""
    scraper = LotScraper()
    
    # 模拟拍品数据
    test_lots = [
        {
            "lot_number": "001",
            "title": "1921 Morgan Silver Dollar",
            "description": "Beautiful silver coin"
        },
        {
            "lot_number": "002",
            "title": "Gold Eagle Coin",
            "description": "US gold piece"
        },
        {
            "lot_number": "003",
            "title": "Peace Silver Dollar",
            "description": "1922 silver dollar"
        },
        {
            "lot_number": "004",
            "title": "Ancient Drachma",
            "description": "Silver coin from Greece"
        }
    ]
    
    print("=" * 60)
    print("测试模糊匹配过滤")
    print("=" * 60)
    
    # 测试 1: 精确匹配
    keywords = ["silver", "dollar"]
    filtered = scraper.filter_lots_by_keyword(test_lots, keywords, fuzzy_match=False)
    print(f"\n关键词 {keywords} (精确匹配):")
    print(f"找到 {len(filtered)} 个拍品")
    for lot in filtered:
        print(f"  - {lot['title']} (评分: {lot.get('_relevance_score', 0):.2f})")
    
    # 测试 2: 模糊匹配
    filtered = scraper.filter_lots_by_keyword(test_lots, keywords, fuzzy_match=True)
    print(f"\n关键词 {keywords} (模糊匹配):")
    print(f"找到 {len(filtered)} 个拍品")
    for lot in filtered:
        print(f"  - {lot['title']} (评分: {lot.get('_relevance_score', 0):.2f})")
    
    # 测试 3: 智能搜索
    query = "find all silver dollar coins"
    filtered = scraper.search_lots_intelligently(test_lots, query, fuzzy_match=True)
    print(f"\n查询 '{query}' (智能搜索):")
    print(f"找到 {len(filtered)} 个拍品")
    for lot in filtered:
        print(f"  - {lot['title']} (评分: {lot.get('_relevance_score', 0):.2f})")

if __name__ == "__main__":
    print("\n")
    print("🧪 测试智能搜索功能")
    print("=" * 60)
    print()
    
    try:
        test_keyword_extraction()
        print("\n")
        
        test_synonym_expansion()
        print("\n")
        
        test_relevance_scoring()
        print("\n")
        
        test_filter_with_fuzzy()
        
        print("\n")
        print("✅ 所有测试完成!")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
