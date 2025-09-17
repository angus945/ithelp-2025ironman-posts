import re
from datetime import datetime
from pathlib import Path
from .config import get_current_year

def extract_metadata_from_filename(md_path):
    """從檔名提取元數據"""
    filename = md_path.stem

    # 移除檔名末尾的 hash 後綴（32位十六進制）
    clean_filename = re.sub(r'\s[0-9a-f]{32}$', '', filename)

    # 解析 Day 格式：Day1 - 標題 或 DAY1 - 標題
    # 也處理 Windows 短檔名格式 (如 DAY5-~1, DAY15~1)
    day_match = re.match(r'^[Dd][Aa][Yy](\d+)\s*-\s*(.+)', clean_filename)

    # 如果沒有匹配到有連字號的格式，嘗試沒有連字號的格式（如 DAY15~1）
    if not day_match:
        day_match = re.match(r'^[Dd][Aa][Yy](\d+)(.+)', clean_filename)

    # 如果匹配到但標題是 Windows 短檔名格式 (~1, ~2 等)，從檔案內容讀取真實標題
    if day_match and re.match(r'^~\d+$', day_match.group(2).strip()):
        day_number = int(day_match.group(1))
        # 嘗試從檔案內容讀取真實標題
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('#'):
                    # 提取標題，移除 # 和可能的 Day 前綴
                    title = first_line.lstrip('#').strip()
                    title_match = re.match(r'^[Dd][Aa][Yy]\d+\s*-?\s*(.+)', title)
                    if title_match:
                        title = title_match.group(1).strip()
                else:
                    title = f"Day {day_number} 文章"
        except:
            title = f"Day {day_number} 文章"
    elif day_match:
        day_number = int(day_match.group(1))
        title = day_match.group(2).strip()
    else:
        # 如果不是 Day 格式，使用通用處理
        title = clean_filename
        today = datetime.now()
        slug_title = re.sub(r'[^\w\s-]', '', title)
        slug_title = re.sub(r'[-\s]+', '-', slug_title)
        slug_title = slug_title.lower().strip('-')
        slug = f"post-{today.strftime('%Y_%m_%d')}-{slug_title}"

        return {
            'title': title,
            'day_number': None,
            'date': today.strftime('%Y-%m-%d'),
            'slug': slug,
            'category': 'general'
        }

    # 生成日期（假設從9月15日開始）
    from datetime import date, timedelta
    start_date = date(2025, 9, 15)  # 鐵人賽開始日期
    post_date = start_date + timedelta(days=day_number - 1)

    # 生成 slug
    slug_title = re.sub(r'[^\w\s-]', '', title)  # 移除特殊字符
    slug_title = re.sub(r'[-\s]+', '-', slug_title)  # 多個空格或連字號合併
    slug_title = slug_title.lower().strip('-')  # 轉小寫並移除首尾連字號
    slug = f"post-{post_date.strftime('%Y_%m_%d')}-day{day_number}-{slug_title}"

    return {
        'title': title,
        'day_number': day_number,
        'date': post_date.strftime('%Y-%m-%d'),
        'slug': slug,
        'category': 'ironman-2025'
    }

def generate_frontmatter(metadata):
    """生成適用於 Medium 的 frontmatter"""
    frontmatter = f"""---
title: "{metadata['title']}"
date: {metadata['date']}
category: {metadata['category']}
slug: {metadata['slug']}
"""

    if metadata['day_number']:
        frontmatter += f"day: {metadata['day_number']}\n"

    frontmatter += "---\n\n"

    return frontmatter