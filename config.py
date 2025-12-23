"""
配置文件 - 存储 API 密钥和系统配置
"""

import os

# API 密钥配置
DEEPSEEK_API_KEY = "sk-46d5f7ddf86c43dfb66bf094006b05e6"
TAVILY_API_KEY = "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"
ZYTE_API_KEY = "94941c33f31d480c8f69e8dbbc871720"

# DeepSeek API 配置
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# 拍卖网站配置
AUCTION_SITE_URL = "https://auctions.stacksbowers.com"

# 缓存配置
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
CACHE_EXPIRY_HOURS = 24

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "auction_agent.log"
