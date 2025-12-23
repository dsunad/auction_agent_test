"""
命令行界面 - 提供交互式命令行界面
"""

import sys
import logging
from agent import AuctionAgent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auction_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        拍卖信息处理 Agent - Stacks Bowers 专版           ║
║                                                           ║
║  功能:                                                    ║
║  • 搜索拍卖信息                                          ║
║  • 按时间、类别、关键词过滤                              ║
║  • 获取拍卖详细信息                                      ║
║                                                           ║
║  示例指令:                                                ║
║  - 搜索未来一周内截止的所有硬币拍卖                      ║
║  - 查找 12 月 10 日之前的代币拍卖                        ║
║  - 显示所有包含 "Silver Dollar" 的拍卖                   ║
║                                                           ║
║  输入 'quit' 或 'exit' 退出                              ║
║  输入 'reset' 重置对话                                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """主函数"""
    print_banner()
    
    # 初始化 Agent
    agent = AuctionAgent()
    logger.info("Agent 初始化完成")
    
    print("\nAgent 已就绪,请输入您的指令:\n")
    
    while True:
        try:
            # 获取用户输入
            user_input = input("您: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n感谢使用拍卖信息处理 Agent,再见!")
                break
            
            # 检查重置命令
            if user_input.lower() in ['reset', '重置']:
                agent.reset_conversation()
                print("\n对话已重置\n")
                continue
            
            # 跳过空输入
            if not user_input:
                continue
            
            # 处理用户指令
            print("\nAgent: 正在处理您的请求...\n")
            response = agent.process_command(user_input)
            print(f"Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n检测到中断信号,正在退出...")
            break
        except Exception as e:
            logger.error(f"发生错误: {e}")
            print(f"\n抱歉,发生了一个错误: {str(e)}\n")
    
    logger.info("Agent 已关闭")


if __name__ == "__main__":
    main()
