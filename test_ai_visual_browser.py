"""
测试 AI 视觉浏览器
"""

import logging
from ai_visual_browser import AIVisualBrowser

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_basic_browsing():
    """测试基本浏览功能"""
    print("=" * 60)
    print("测试 AI 视觉浏览器")
    print("=" * 60)
    
    # 测试 URL
    test_url = "https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475"
    
    # 测试搜索要求
    search_queries = [
        "找出所有金币",
        "find all silver dollars",
        "我想要 Morgan 硬币"
    ]
    
    with AIVisualBrowser() as browser:
        for query in search_queries:
            print(f"\n{'='*60}")
            print(f"搜索要求: {query}")
            print('='*60)
            
            # 浏览页面
            items = browser.browse_auction_page(test_url, query)
            
            print(f"\n找到 {len(items)} 个符合要求的拍品:\n")
            
            for i, item in enumerate(items[:5], 1):  # 只显示前 5 个
                print(f"{i}. {item.get('title', 'N/A')}")
                print(f"   编号: {item.get('lot_number', 'N/A')}")
                print(f"   价格: ${item.get('price', 'N/A')}")
                print(f"   相关性: {item.get('relevance_score', 0)}/10")
                print(f"   理由: {item.get('reason', 'N/A')}")
                print()
            
            if len(items) > 5:
                print(f"   ... 还有 {len(items) - 5} 个拍品")
            
            print()

def test_multi_page_browsing():
    """测试多页面浏览"""
    print("=" * 60)
    print("测试多页面浏览")
    print("=" * 60)
    
    test_url = "https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475"
    search_query = "找出所有包含'silver'的拍品"
    
    with AIVisualBrowser() as browser:
        items = browser.browse_multiple_pages(
            test_url, 
            search_query,
            max_pages=2
        )
        
        print(f"\n总共找到 {len(items)} 个符合要求的拍品")
        
        # 按相关性排序
        items_sorted = sorted(
            items, 
            key=lambda x: x.get('relevance_score', 0), 
            reverse=True
        )
        
        print("\n最相关的 5 个拍品:")
        for i, item in enumerate(items_sorted[:5], 1):
            print(f"{i}. {item.get('title', 'N/A')} (评分: {item.get('relevance_score', 0)}/10)")

if __name__ == "__main__":
    print("\n")
    print("🧪 测试 AI 视觉浏览器")
    print("=" * 60)
    print()
    
    try:
        # 测试基本浏览
        test_basic_browsing()
        
        print("\n\n")
        
        # 测试多页面浏览
        # test_multi_page_browsing()  # 暂时注释，避免太多请求
        
        print("\n")
        print("✅ 测试完成!")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
