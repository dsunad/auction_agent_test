"""
测试拍品抓取功能
"""

import logging
from lot_scraper import LotScraper

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_fetch_lots():
    """测试获取拍品"""
    print("\n" + "="*60)
    print("测试: 获取拍卖场次的拍品列表")
    print("="*60)
    
    scraper = LotScraper()
    
    # 测试 URL
    test_url = "https://auctions.stacksbowers.com/auctions/3-1NZHVT/december-2025-collectors-choice-online-auction-tokens-medals-lots-70001-70475"
    
    print(f"\n正在获取拍卖场次的拍品: {test_url}\n")
    print("注意: 这将使用 Zyte API,可能需要一些时间...\n")
    
    # 只获取第一页进行测试
    lots = scraper.get_all_lots_from_auction(test_url, max_pages=1)
    
    print(f"\n找到 {len(lots)} 个拍品\n")
    
    if lots:
        print("前 3 个拍品示例:")
        print("-" * 60)
        for i, lot in enumerate(lots[:3], 1):
            print(f"\n拍品 #{i}:")
            for key, value in lot.items():
                print(f"  {key}: {value}")
        print("-" * 60)
    
    return lots


def test_filter_and_save():
    """测试过滤和保存功能"""
    print("\n" + "="*60)
    print("测试: 关键词过滤和文件保存")
    print("="*60)
    
    scraper = LotScraper()
    
    # 创建测试数据
    test_lots = [
        {
            "lot_number": "70001",
            "title": "1919 General John J. Pershing Portrait Plaque",
            "description": "Bronze and Iron. Extremely Fine.",
            "current_bid": "40"
        },
        {
            "lot_number": "70002",
            "title": "Admiral Dewey Medal Bronze",
            "description": "MS-64 BN (PCGS)",
            "current_bid": "320"
        },
        {
            "lot_number": "70003",
            "title": "Indian Peace Medals Silver",
            "description": "Lot of 3 medals",
            "current_bid": "260"
        }
    ]
    
    print(f"\n测试数据: {len(test_lots)} 个拍品")
    
    # 测试关键词过滤
    keywords = ["Silver", "Bronze"]
    print(f"\n使用关键词过滤: {keywords}")
    
    filtered = scraper.filter_lots_by_keyword(test_lots, keywords)
    print(f"过滤后: {len(filtered)} 个拍品")
    
    for lot in filtered:
        print(f"  - {lot['title']}")
    
    # 测试保存到文件
    print("\n测试保存到文件...")
    
    # JSON 格式
    scraper.save_lots_to_file(test_lots, "test_lots.json", "json")
    print("✓ 已保存到 test_lots.json")
    
    # CSV 格式
    scraper.save_lots_to_file(test_lots, "test_lots.csv", "csv")
    print("✓ 已保存到 test_lots.csv")
    
    # TXT 格式
    scraper.save_lots_to_file(test_lots, "test_lots.txt", "txt")
    print("✓ 已保存到 test_lots.txt")


def main():
    """运行测试"""
    print("\n" + "="*60)
    print("拍品抓取功能测试")
    print("="*60)
    
    try:
        # 测试过滤和保存(不需要网络请求)
        test_filter_and_save()
        
        # 询问是否测试真实抓取
        print("\n" + "="*60)
        response = input("\n是否测试真实的拍品抓取? (这将使用 Zyte API) [y/N]: ").strip().lower()
        
        if response == 'y':
            test_fetch_lots()
        else:
            print("\n跳过真实抓取测试")
        
        print("\n" + "="*60)
        print("测试完成")
        print("="*60)
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)


if __name__ == "__main__":
    main()
