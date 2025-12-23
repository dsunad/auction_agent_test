"""
使用示例 - 演示如何使用拍卖信息处理 Agent
"""

from agent import AuctionAgent


def example_1_basic_query():
    """示例 1: 基本查询"""
    print("\n" + "="*60)
    print("示例 1: 使用自然语言查询拍卖信息")
    print("="*60)
    
    agent = AuctionAgent()
    
    # 查询未来一周内的硬币拍卖
    query = "搜索未来一周内截止的所有硬币拍卖"
    print(f"\n查询: {query}\n")
    
    response = agent.process_command(query)
    print(f"回复:\n{response}\n")


def example_2_direct_search():
    """示例 2: 直接调用搜索函数"""
    print("\n" + "="*60)
    print("示例 2: 直接使用搜索函数")
    print("="*60)
    
    agent = AuctionAgent()
    
    # 搜索硬币拍卖
    results = agent.search_auctions(
        time_range_days=7,
        categories=["U.S. Coins & Related", "World Coins"]
    )
    
    print(f"\n找到 {len(results)} 个拍卖:\n")
    for auction in results:
        print(f"标题: {auction['title']}")
        print(f"日期: {auction['date']}")
        print(f"Lots: {auction['lots_count']}")
        print(f"URL: {auction['url']}")
        print("-" * 60)


def example_3_conversation():
    """示例 3: 多轮对话"""
    print("\n" + "="*60)
    print("示例 3: 多轮对话")
    print("="*60)
    
    agent = AuctionAgent()
    
    queries = [
        "你好,我想查找硬币拍卖",
        "只显示美国硬币的",
        "有哪些拍卖的 Lots 数量超过 100?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n[第 {i} 轮] 用户: {query}")
        response = agent.process_command(query)
        print(f"Agent: {response}\n")


def example_4_category_search():
    """示例 4: 按类别搜索"""
    print("\n" + "="*60)
    print("示例 4: 按类别搜索")
    print("="*60)
    
    agent = AuctionAgent()
    
    categories_to_search = [
        ["U.S. Coins & Related"],
        ["World Coins"],
        ["Numismatic Americana"],
        ["U.S. Paper Currency"]
    ]
    
    for categories in categories_to_search:
        print(f"\n搜索类别: {categories}")
        results = agent.search_auctions(categories=categories)
        print(f"找到 {len(results)} 个拍卖")
        
        for auction in results:
            print(f"  - {auction['title']}")


def example_5_keyword_search():
    """示例 5: 关键词搜索"""
    print("\n" + "="*60)
    print("示例 5: 关键词搜索")
    print("="*60)
    
    agent = AuctionAgent()
    
    # 使用自然语言查询
    query = "查找包含 'Silver Dollar' 的拍卖"
    print(f"\n查询: {query}\n")
    
    response = agent.process_command(query)
    print(f"回复:\n{response}\n")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("拍卖信息处理 Agent - 使用示例")
    print("="*60)
    
    # 运行示例
    example_1_basic_query()
    example_2_direct_search()
    example_3_conversation()
    example_4_category_search()
    example_5_keyword_search()
    
    print("\n" + "="*60)
    print("所有示例运行完成")
    print("="*60)


if __name__ == "__main__":
    main()
