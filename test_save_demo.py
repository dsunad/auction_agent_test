"""
演示拍品信息保存功能
"""

from lot_scraper import LotScraper

# 创建测试数据
test_lots = [
    {
        "lot_number": "10001",
        "title": "1921 Morgan Silver Dollar",
        "description": "Beautiful uncirculated Morgan silver dollar",
        "current_bid": "5000",
        "image_url": "https://example.com/image1.jpg"
    },
    {
        "lot_number": "10002",
        "title": "1909-S VDB Lincoln Cent",
        "description": "Rare Lincoln penny in excellent condition",
        "current_bid": "1200",
        "image_url": "https://example.com/image2.jpg"
    }
]

# 创建 LotScraper 实例
scraper = LotScraper()

# 保存为不同格式
print("=" * 60)
print("演示: 拍品信息保存功能")
print("=" * 60)

# 1. 保存为 JSON
json_file = "demo_lots.json"
scraper.save_lots_to_file(test_lots, json_file, format='json')
print(f"✅ JSON 格式已保存到: {json_file}")

# 2. 保存为 CSV
csv_file = "demo_lots.csv"
scraper.save_lots_to_file(test_lots, csv_file, format='csv')
print(f"✅ CSV 格式已保存到: {csv_file}")

# 3. 保存为 TXT
txt_file = "demo_lots.txt"
scraper.save_lots_to_file(test_lots, txt_file, format='txt')
print(f"✅ TXT 格式已保存到: {txt_file}")

print("\n" + "=" * 60)
print("所有文件都保存在当前目录:")
print("/home/user/webapp/")
print("=" * 60)

# 列出保存的文件
import os
print("\n生成的文件列表:")
for f in ['demo_lots.json', 'demo_lots.csv', 'demo_lots.txt']:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"  📄 {f} ({size} bytes)")
