# 🔍 拍品文件在哪里？

## 📍 直接答案

**所有拍品信息都保存在这里**:
```
/home/user/webapp/
```

## 📂 文件示例

运行系统后，你会在这个目录看到类似这样的文件：

```
/home/user/webapp/
├── gold_coins.json          ← 搜索金币的结果
├── silver_dollars.csv       ← 搜索银元的结果  
├── rare_pennies.txt         ← 搜索稀有便士的结果
├── demo_lots.json           ← 系统自带的演示文件
├── demo_lots.csv            ← 演示文件 (CSV 格式)
└── demo_lots.txt            ← 演示文件 (TXT 格式)
```

## 🔎 如何查找文件？

### 方法 1: 列出所有输出文件
```bash
cd /home/user/webapp
ls -lh *.json *.csv *.txt
```

### 方法 2: 查看最新的文件
```bash
cd /home/user/webapp
ls -lht | head -20
```

### 方法 3: 搜索包含特定词的文件名
```bash
cd /home/user/webapp
find . -name "*gold*" -o -name "*silver*"
```

## 📋 文件格式

| 格式 | 什么时候用 | 怎么打开 |
|------|-----------|---------|
| `.json` | 需要程序处理数据 | 文本编辑器、Python |
| `.csv` | 需要 Excel 分析 | Excel、Google Sheets |
| `.txt` | 只想快速查看 | 任何文本编辑器 |

## 🎯 快速测试

运行这个命令，立即生成演示文件：

```bash
cd /home/user/webapp
python3 test_save_demo.py
```

你会看到：
```
✅ JSON 格式已保存到: demo_lots.json
✅ CSV 格式已保存到: demo_lots.csv
✅ TXT 格式已保存到: demo_lots.txt
```

然后查看文件：
```bash
ls -lh demo_lots.*
```

## 📖 查看文件内容

### JSON 文件
```bash
cat demo_lots.json
```

### CSV 文件  
```bash
cat demo_lots.csv
```

### TXT 文件
```bash
cat demo_lots.txt
```

## ❓ 还有问题？

查看详细指南: **[FILE_OUTPUT_GUIDE.md](./FILE_OUTPUT_GUIDE.md)**

这个文档包含：
- ✅ 完整的使用示例
- ✅ 文件命名建议
- ✅ 常见问题解答
- ✅ Python API 使用方法

---

**记住**: 所有文件都在 `/home/user/webapp/` 📁
