"""
快速测试 AI 智能浏览器 - 单个查询
"""

import logging
from ai_smart_browser import AISmartBrowser

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def quick_test():
    """快速测试"""
    print("\n")
    print("=" * 80)
    print("🧪 快速测试 AI 智能浏览器")
    print("=" * 80)
    print()
    
    # 测试 URL
    test_url = "https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475"
    
    # 测试查询 - 这个是之前硬编码方法失败的case
    query = "找出所有金币"
    
    print(f"📝 搜索要求: {query}")
    print()
    
    browser = AISmartBrowser()
    items = browser.smart_browse(test_url, query, max_pages=1)
    
    print(f"\n✅ 找到 {len(items)} 个符合要求的拍品\n")
    
    if items:
        print("结果列表:\n")
        for i, item in enumerate(items, 1):
            print(f"  {i}. 【{item.get('lot_number', 'N/A')}】 {item.get('title', 'N/A')}")
            print(f"     价格: ${item.get('price', 'N/A')}")
            print(f"     相关性: {item.get('relevance_score', 0)}/10 ⭐")
            
            reason = item.get('reason', 'N/A')
            if len(reason) > 80:
                reason = reason[:80] + "..."
            print(f"     理由: {reason}")
            print()
        
        print("\n对比:")
        print("  传统硬编码方法: 找到 0 个拍品 ❌")
        print(f"  AI 智能浏览: 找到 {len(items)} 个拍品 ✅")
    else:
        print("  ⚠️  未找到符合要求的拍品")
    
    print()

if __name__ == "__main__":
    try:
        quick_test()
        print("✅ 测试完成!")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
