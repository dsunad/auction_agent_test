"""
测试脚本 - 验证 Agent 功能
"""

import sys
import logging
from agent import AuctionAgent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_basic_query():
    """测试基本查询功能"""
    print("\n" + "="*60)
    print("测试 1: 基本查询功能")
    print("="*60)
    
    agent = AuctionAgent()
    
    test_queries = [
        "搜索未来一周内截止的所有硬币拍卖",
        "有哪些拍卖包含代币和奖章?",
        "显示所有拍卖信息"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        print("-" * 60)
        
        try:
            response = agent.process_command(query)
            print(f"回复: {response}")
        except Exception as e:
            print(f"错误: {e}")
            logger.error(f"查询失败: {e}", exc_info=True)
        
        print("-" * 60)


def test_search_function():
    """测试搜索函数"""
    print("\n" + "="*60)
    print("测试 2: 直接调用搜索函数")
    print("="*60)
    
    agent = AuctionAgent()
    
    # 测试不同的搜索参数
    test_cases = [
        {
            "name": "按时间范围搜索",
            "params": {"time_range_days": 7}
        },
        {
            "name": "按类别搜索",
            "params": {"categories": ["U.S. Coins & Related", "World Coins"]}
        },
        {
            "name": "按关键词搜索",
            "params": {"keywords": ["Silver", "Dollar"]}
        },
        {
            "name": "组合搜索",
            "params": {
                "time_range_days": 7,
                "categories": ["U.S. Coins & Related"],
                "min_lots": 50
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print(f"参数: {test_case['params']}")
        print("-" * 60)
        
        try:
            results = agent.search_auctions(**test_case['params'])
            print(f"找到 {len(results)} 个拍卖:")
            for auction in results:
                print(f"  - {auction.get('title', 'N/A')}")
                print(f"    日期: {auction.get('date', 'N/A')}, Lots: {auction.get('lots_count', 'N/A')}")
        except Exception as e:
            print(f"错误: {e}")
            logger.error(f"搜索失败: {e}", exc_info=True)
        
        print("-" * 60)


def test_conversation_flow():
    """测试对话流程"""
    print("\n" + "="*60)
    print("测试 3: 多轮对话")
    print("="*60)
    
    agent = AuctionAgent()
    
    conversation = [
        "你好,你能帮我做什么?",
        "搜索硬币拍卖",
        "只显示未来一周内的",
        "重置对话"
    ]
    
    for i, message in enumerate(conversation, 1):
        print(f"\n轮次 {i}: {message}")
        print("-" * 60)
        
        try:
            if "重置" in message:
                agent.reset_conversation()
                print("对话已重置")
            else:
                response = agent.process_command(message)
                print(f"回复: {response}")
        except Exception as e:
            print(f"错误: {e}")
            logger.error(f"对话失败: {e}", exc_info=True)
        
        print("-" * 60)


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("拍卖信息处理 Agent - 功能测试")
    print("="*60)
    
    try:
        # 运行测试
        test_basic_query()
        test_search_function()
        test_conversation_flow()
        
        print("\n" + "="*60)
        print("所有测试完成")
        print("="*60)
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
