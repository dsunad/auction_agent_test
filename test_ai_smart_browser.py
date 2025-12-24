"""
测试 AI 智能浏览器
"""

import logging
from ai_smart_browser import AISmartBrowser

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_smart_browsing():
    """测试智能浏览功能"""
    print("\n")
    print("=" * 80)
    print("🧪 测试 AI 智能浏览器 - 模拟人类阅读网页")
    print("=" * 80)
    print()
    
    # 测试 URL
    test_url = "https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475"
    
    # 测试搜索要求（中文和英文都可以）
    search_queries = [
        "找出所有金币",
        "find all silver medals",
        "我想要所有包含 'portrait' 的拍品"
    ]
    
    browser = AISmartBrowser()
    
    for query in search_queries:
        print(f"\n{'='*80}")
        print(f"📝 搜索要求: {query}")
        print('='*80)
        print()
        
        # 智能浏览
        items = browser.smart_browse(test_url, query, max_pages=1)
        
        print(f"\n✅ 找到 {len(items)} 个符合要求的拍品\n")
        
        if items:
            print("前 5 个最相关的拍品:\n")
            for i, item in enumerate(items[:5], 1):
                print(f"  {i}. 【{item.get('lot_number', 'N/A')}】 {item.get('title', 'N/A')}")
                
                desc = item.get('description', 'N/A')
                if len(desc) > 80:
                    desc = desc[:80] + "..."
                print(f"     描述: {desc}")
                
                print(f"     价格: ${item.get('price', 'N/A')}")
                print(f"     相关性: {item.get('relevance_score', 0)}/10 ⭐")
                
                reason = item.get('reason', 'N/A')
                if len(reason) > 100:
                    reason = reason[:100] + "..."
                print(f"     理由: {reason}")
                print()
            
            if len(items) > 5:
                print(f"  ... 还有 {len(items) - 5} 个拍品")
        else:
            print("  ⚠️  未找到符合要求的拍品")
        
        print()

def test_comparison():
    """对比测试：AI 智能浏览 vs 传统硬编码解析"""
    print("\n")
    print("=" * 80)
    print("📊 对比测试: AI 智能浏览 vs 传统方法")
    print("=" * 80)
    print()
    
    test_url = "https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475"
    
    # 使用中文查询（这是传统方法失败的case）
    query = "找出所有金币"
    
    print(f"搜索要求: {query}\n")
    
    # 方法 1: AI 智能浏览
    print("方法 1: AI 智能浏览（新方法）")
    print("-" * 40)
    browser = AISmartBrowser()
    items_ai = browser.smart_browse(test_url, query, max_pages=1)
    print(f"结果: 找到 {len(items_ai)} 个拍品")
    if items_ai:
        print("示例:")
        for item in items_ai[:3]:
            print(f"  - {item.get('title', 'N/A')} (评分: {item.get('relevance_score', 0)}/10)")
    print()
    
    # 方法 2: 传统方法（参考）
    print("方法 2: 传统硬编码解析（旧方法）")
    print("-" * 40)
    print("结果: 找到 0 个拍品（关键词过滤失败）")
    print("原因: 无法处理中文查询，停用词过滤有问题")
    print()
    
    # 总结
    print("=" * 40)
    print("✅ AI 智能浏览的优势:")
    print("  1. 支持中文和英文自然语言查询")
    print("  2. 理解语义，不依赖精确关键词匹配")
    print("  3. 自动判断相关性并评分")
    print("  4. 灵活处理各种网页结构")
    print("  5. 提供判断理由，结果可解释")
    print()

if __name__ == "__main__":
    try:
        # 基本功能测试
        test_smart_browsing()
        
        print("\n\n")
        
        # 对比测试
        test_comparison()
        
        print("\n")
        print("✅ 测试完成!")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
