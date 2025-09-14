import yaml
from pathlib import Path

# 設定資料夾路徑
ROOT = Path(".").resolve()
RAW_DIR = ROOT / "Raw"
PUBLISH_DIR = ROOT / "Publish"

# GitHub Raw URL 前綴（用於圖片路徑）
GITHUB_RAW_PREFIX = "https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/"

# 支援的圖片格式
SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

def init_directories():
    """建立所有必要的資料夾"""
    PUBLISH_DIR.mkdir(parents=True, exist_ok=True)
    print(f"已確認資料夾存在: {PUBLISH_DIR}")

def get_current_year():
    """取得當前年份"""
    from datetime import datetime
    return str(datetime.now().year)