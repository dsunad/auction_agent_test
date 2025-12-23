#!/bin/bash

# 拍卖信息处理 Agent - 快速启动脚本

echo "=================================="
echo "拍卖信息处理 Agent"
echo "=================================="
echo ""

# 检查 Python 版本
python3 --version

echo ""
echo "选择运行模式:"
echo "1. 命令行交互模式"
echo "2. API 服务模式"
echo "3. 运行测试"
echo "4. 运行示例"
echo ""

read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "启动命令行交互模式..."
        python3 cli.py
        ;;
    2)
        echo ""
        echo "启动 API 服务..."
        echo "服务将运行在 http://localhost:8000"
        python3 api_server.py
        ;;
    3)
        echo ""
        echo "运行测试..."
        python3 test_agent.py
        ;;
    4)
        echo ""
        echo "运行示例..."
        python3 example_usage.py
        ;;
    *)
        echo "无效的选项"
        exit 1
        ;;
esac
