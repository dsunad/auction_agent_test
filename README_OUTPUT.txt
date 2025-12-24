╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  📁 拍品信息输出位置                                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📍 所有文件保存在: /home/user/webapp/

🔍 查看所有输出文件:
   $ cd /home/user/webapp
   $ ls -lh *.json *.csv *.txt

📦 支持的格式:
   • JSON (.json) - 结构化数据，适合程序处理
   • CSV  (.csv)  - 表格格式，可用 Excel 打开
   • TXT  (.txt)  - 纯文本格式，易于阅读

🧪 快速测试:
   $ cd /home/user/webapp
   $ python3 test_save_demo.py

📚 查看演示文件:
   $ cat demo_lots.json    (JSON 格式示例)
   $ cat demo_lots.csv     (CSV 格式示例)
   $ cat demo_lots.txt     (TXT 格式示例)

📖 详细文档:
   • FILE_OUTPUT_GUIDE.md    - 完整指南
   • WHERE_ARE_MY_FILES.md   - 快速参考

═══════════════════════════════════════════════════════════════

🎯 使用示例:

Python API:
-----------
from agent_v2 import AuctionAgentV2

agent = AuctionAgentV2()

# AI 智能浏览
lots = agent.ai_smart_browse(
    auction_url="https://auctions.stacksbowers.com/...",
    search_query="找出所有金币"
)

# 保存结果
agent.lot_scraper.save_lots_to_file(lots, "gold_coins.json", "json")

结果文件: /home/user/webapp/gold_coins.json
         /home/user/webapp/gold_coins.csv
         /home/user/webapp/gold_coins.txt

═══════════════════════════════════════════════════════════════
