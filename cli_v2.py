"""
命令行界面 V2 - 增强版,支持拍品抓取和导出
"""

import sys
import logging
from agent_v2 import AuctionAgentV2

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
║     拍卖信息处理 Agent V2 - 增强版                       ║
║                                                           ║
║  新功能:                                                  ║
║  ✨ 深入拍卖场次获取所有拍品详细信息                     ║
║  ✨ 按关键词过滤拍品                                     ║
║  ✨ 导出拍品到 JSON/CSV/TXT 文件                         ║
║                                                           ║
║  示例指令:                                                ║
║  - 获取某个拍卖的所有拍品信息                            ║
║  - 搜索包含"silver"的拍品并导出到文件                    ║
║  - 找出所有硬币拍卖的拍品,保存为 CSV                    ║
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
    agent = AuctionAgentV2()
    logger.info("Agent V2 初始化完成")
    
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
