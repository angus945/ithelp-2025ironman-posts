#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

from .config import RAW_DIR
from .processor import process_single_file, process_multiple_files, setup_environment

def find_raw_files():
    """找到所有 Raw 資料夾中的 Markdown 檔案"""
    if not RAW_DIR.exists():
        print(f"Raw 資料夾不存在: {RAW_DIR}")
        return []

    md_files = list(RAW_DIR.glob("*.md"))
    md_files.extend(RAW_DIR.rglob("*.md"))

    return sorted(set(md_files))

def main():
    parser = argparse.ArgumentParser(
        description="Raw to Medium 格式轉換工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  # 轉換單個檔案
  python -m Tools.RawToMedium.converter "Raw/Day1 - 用 Vibe Coding.md"

  # 批次轉換所有檔案
  python -m Tools.RawToMedium.converter --all

  # 列出可用檔案
  python -m Tools.RawToMedium.converter --list
        """)

    parser.add_argument(
        "file",
        nargs="?",
        help="要轉換的 Markdown 檔案路徑"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="轉換所有 Raw 資料夾中的檔案"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用的 Raw 檔案"
    )

    parser.add_argument(
        "--output",
        help="指定輸出目錄（可選）"
    )

    args = parser.parse_args()

    # 設置環境
    setup_environment()

    # 列出檔案
    if args.list:
        raw_files = find_raw_files()
        if raw_files:
            print("可用的 Raw 檔案:")
            for i, file_path in enumerate(raw_files, 1):
                print(f"  {i}. {file_path.relative_to(RAW_DIR)}")
        else:
            print("沒有找到 Markdown 檔案")
        return

    # 批次處理所有檔案
    if args.all:
        raw_files = find_raw_files()
        if not raw_files:
            print("沒有找到 Markdown 檔案")
            return

        print(f"找到 {len(raw_files)} 個檔案")
        results, failed = process_multiple_files(raw_files)

        print(f"\n=== 處理結果 ===")
        print(f"成功轉換: {len(results)} 個檔案")
        if failed:
            print(f"轉換失敗: {len(failed)} 個檔案")
            for file_path, error in failed:
                print(f"  - {file_path}: {error}")

        return

    # 處理單個檔案
    if args.file:
        file_path = Path(args.file)

        # 如果提供的是相對路徑，嘗試在 Raw 資料夾中找到
        if not file_path.is_absolute():
            potential_path = RAW_DIR / args.file
            if potential_path.exists():
                file_path = potential_path

        try:
            result_path, metadata = process_single_file(file_path)
            print(f"\n=== 轉換完成 ===")
            print(f"標題: {metadata['title']}")
            print(f"輸出路徑: {result_path}")
        except Exception as e:
            print(f"轉換失敗: {e}")
            sys.exit(1)

        return

    # 如果沒有提供任何參數，顯示幫助
    parser.print_help()

if __name__ == "__main__":
    main()