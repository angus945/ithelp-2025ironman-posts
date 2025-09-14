"""
RawToMedium - Raw 格式直接轉換為 Medium 發布格式的工具

這個模組提供了一套簡化的工具，可以將 Raw 資料夾中的 Markdown 檔案
直接轉換成適合 Medium 發布的格式，跳過複雜的中間處理步驟。

主要功能：
- 從檔名自動提取元數據
- 清理 Notion 導出格式
- 處理圖片並生成 GitHub URL
- 生成 Medium 友好的 Markdown 格式

使用方式：
    from Tools.RawToMedium.processor import process_single_file
    result = process_single_file("Raw/Day1 - 標題.md")

或直接執行：
    python -m Tools.RawToMedium.converter --all
"""

__version__ = "1.0.0"
__author__ = "Angus"

from .processor import process_single_file, process_multiple_files, setup_environment
from .config import RAW_DIR, PUBLISH_DIR, init_directories

__all__ = [
    'process_single_file',
    'process_multiple_files',
    'setup_environment',
    'RAW_DIR',
    'PUBLISH_DIR',
    'init_directories'
]