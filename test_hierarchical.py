"""
测试多层级浏览功能
"""

import logging
from hierarchical_browser import HierarchicalBrowser

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_discover_auctions():
    """测试发现拍卖场次功能"""
    print("\n")
    print("=" * 80)
    print("🧪 测试 1: 发现拍卖场次")
    print("=" * 80)
    print()
    
    browser = HierarchicalBrowser()
    
    # 测试首页
    index_url = "https://auctions.stacksbowers.com/"
    
    print(f"分析首页: {index_url}\n")
    
    auctions = browser.discover_auctions(index_url)
    
    print(f"\n✅ 发现 {len(auctions)} 个拍卖场次:\n")
    
    for i, auction in enumerate(auctions[:10], 1):  # 只显示前10个
        print(f"  {i}. {auction.get('title', 'N/A')}")
        print(f"     日期: {auction.get('date', 'N/A')}")
        print(f"     拍品数: {auction.get('lots_count', 'N/A')}")
        print(f"     URL: {auction.get('url', 'N/A')[:80]}...")
        print()
    
    if len(auctions) > 10:
        print(f"  ... 还有 {len(auctions) - 10} 个场次")
    
    return auctions

def test_browse_all_auctions():
    """测试多场次浏览功能"""
    print("\n")
    print("=" * 80)
    print("🧪 测试 2: 多场次浏览")
    print("=" * 80)
    print()
    
    browser = HierarchicalBrowser()
    
    index_url = "https://auctions.stacksbowers.com/"
    search_query = "找出所有金币"
    
    print(f"首页: {index_url}")
    print(f"搜索: {search_query}")
    print(f"限制: 前 2 个场次（测试用）\n")
    
    # 只浏览前2个场次进行测试
    result = browser.browse_all_auctions(
        index_url, 
        search_query,
        max_auctions=2
    )
    
    if result['success']:
        print(f"\n✅ 浏览完成！")
        print(f"\n统计:")
        print(f"  - 浏览场次数: {result['auctions_count']}")
        print(f"  - 找到拍品数: {result['total_lots']}")
        print()
        
        # 显示每个场次的结果
        for i, auction_result in enumerate(result['auctions'], 1):
            auction = auction_result['auction']
            lots = auction_result['lots']
            
            print(f"\n场次 {i}: {auction.get('title', 'N/A')}")
            print(f"  找到 {len(lots)} 个符合要求的拍品")
            
            if lots:
                print(f"  前 3 个拍品:")
                for j, lot in enumerate(lots[:3], 1):
                    print(f"    {j}. {lot.get('title', 'N/A')}")
                    print(f"       评分: {lot.get('relevance_score', 0)}/10")
    else:
        print(f"\n❌ 浏览失败: {result.get('message', 'Unknown error')}")

def test_get_all_lots():
    """测试获取所有拍品（扁平化）"""
    print("\n")
    print("=" * 80)
    print("🧪 测试 3: 获取所有拍品（扁平化）")
    print("=" * 80)
    print()
    
    browser = HierarchicalBrowser()
    
    index_url = "https://auctions.stacksbowers.com/"
    search_query = "silver medal"
    
    print(f"搜索: {search_query}")
    print(f"限制: 前 2 个场次\n")
    
    all_lots = browser.get_all_matching_lots(
        index_url,
        search_query,
        max_auctions=2
    )
    
    print(f"\n✅ 找到 {len(all_lots)} 个符合要求的拍品")
    
    if all_lots:
        print(f"\n按相关性排序的前 5 个拍品:\n")
        for i, lot in enumerate(all_lots[:5], 1):
            print(f"  {i}. {lot.get('title', 'N/A')}")
            print(f"     场次: {lot.get('auction_title', 'N/A')}")
            print(f"     评分: {lot.get('relevance_score', 0)}/10")
            print(f"     理由: {lot.get('reason', 'N/A')[:60]}...")
            print()

def quick_demo():
    """快速演示"""
    print("\n")
    print("=" * 80)
    print("🚀 快速演示: 完整工作流")
    print("=" * 80)
    print()
    
    browser = HierarchicalBrowser()
    
    print("步骤:")
    print("  1. 分析拍卖网站首页")
    print("  2. 发现所有拍卖场次")
    print("  3. 遍历每个场次")
    print("  4. 在每个场次中搜索符合要求的拍品")
    print("  5. 汇总所有结果\n")
    
    print("开始执行...\n")
    
    # 执行
    all_lots = browser.get_all_matching_lots(
        "https://auctions.stacksbowers.com/",
        "找出所有金币",
        max_auctions=2  # 限制为2个场次
    )
    
    print(f"\n✅ 完成！找到 {len(all_lots)} 个金币")
    
    if all_lots:
        print(f"\n最相关的 3 个结果:\n")
        for i, lot in enumerate(all_lots[:3], 1):
            print(f"  {i}. 【{lot.get('lot_number', 'N/A')}】 {lot.get('title', 'N/A')}")
            print(f"     来自: {lot.get('auction_title', 'N/A')}")
            print(f"     价格: ${lot.get('price', 'N/A')}")
            print(f"     评分: {lot.get('relevance_score', 0)}/10")
            print()

if __name__ == "__main__":
    try:
        # 选择要运行的测试
        import sys
        
        if len(sys.argv) > 1 and sys.argv[1] == 'quick':
            # 快速演示
            quick_demo()
        else:
            # 完整测试套件
            print("\n🧪 多层级浏览测试套件\n")
            
            # 测试 1
            auctions = test_discover_auctions()
            
            if auctions:
                input("\n按 Enter 继续下一个测试...")
                
                # 测试 2
                test_browse_all_auctions()
                
                input("\n按 Enter 继续下一个测试...")
                
                # 测试 3  
                test_get_all_lots()
        
        print("\n✅ 所有测试完成!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
