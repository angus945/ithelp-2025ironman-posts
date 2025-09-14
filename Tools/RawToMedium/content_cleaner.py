import re
from pathlib import Path

def clean_content(md_content):
    """清理和格式化 Markdown 內容"""
    content = md_content.strip()

    # 移除 Notion 導出的 metadata（如 "Status: Draft"）
    content = re.sub(r'^Status:\s*\w+\n*', '', content, flags=re.MULTILINE)

    # 移除其他常見的 metadata 格式
    content = re.sub(r'^(Tags?|Category|Author|Created|Updated|Page-?ID):\s*.+\n*', '', content, flags=re.MULTILINE)

    # 移除多餘的空行（超過兩個連續的空行壓縮為兩個）
    content = re.sub(r'\n\n\n+', '\n\n', content)

    # 清理開頭和結尾的空白
    content = content.strip()

    return content

def process_image_paths(content, image_mapping=None, post_slug=None):
    """處理圖片路徑，將本地路徑轉換為 GitHub URL"""
    if not image_mapping or not post_slug:
        return content

    from .config import GITHUB_RAW_PREFIX

    def replace_image_path(match):
        # 提取圖片路徑
        img_path = match.group(1)

        # 解碼整個路徑後再提取檔名
        import urllib.parse
        decoded_path = urllib.parse.unquote(img_path)
        # 手動提取檔名，避免 Path.name 在長路徑時的問題
        original_name = decoded_path.split('/')[-1]

        # 嘗試在 image_mapping 中找到對應
        found_mapping = None

        for orig_name, new_name in image_mapping.items():
            # 嘗試完全匹配
            if orig_name == original_name:
                found_mapping = new_name
                print(f"圖片匹配成功: {orig_name} -> {new_name}")
                break
            # 嘗試解碼後的原始檔名匹配
            elif urllib.parse.unquote(orig_name) == original_name:
                found_mapping = new_name
                print(f"圖片匹配成功（解碼）: {orig_name} -> {new_name}")
                break
            # 嘗試部分匹配（當原始路徑被截斷時）
            elif orig_name.startswith(original_name) and len(original_name) > 20:
                found_mapping = new_name
                print(f"圖片部分匹配成功: {orig_name} -> {new_name}")
                break

        if found_mapping:
            # 使用 GitHub Raw URL
            github_url = f"{GITHUB_RAW_PREFIX}{post_slug}/images/{found_mapping}"
            return f"![圖片]({github_url})"
        else:
            # 如果找不到對應，顯示詳細資訊並保持原始路徑
            print(f"警告：找不到圖片 '{original_name}' 的對應關係")
            print(f"解碼前路徑: {img_path}")
            print(f"解碼後路徑: {decoded_path}")
            print(f"可用的圖片對應: {list(image_mapping.keys())}")
            return match.group(0)

    # 替換所有圖片標記，特別處理截斷的路徑
    # 先處理正常的圖片標記
    processed_content = re.sub(r'!\[[^\]]*\]\(([^)]*)\)', replace_image_path, content)

    # 清理可能剩餘的截斷文字（在替換圖片後可能出現的額外文字）
    # 這會移除類似 "___DX11__2025-09-04_10-45-26_0.gif)" 的殘留文字
    processed_content = re.sub(r'[_-]+[A-Z0-9_-]*\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d+\.gif\)', '', processed_content)

    return processed_content

def format_for_medium(content):
    """針對 Medium 平台進行格式調整"""
    # Medium 支援標準 Markdown，主要是確保格式正確

    # 確保標題有適當的空行
    content = re.sub(r'^(#{1,6}\s.+)$', r'\1\n', content, flags=re.MULTILINE)

    # 確保段落之間有適當的空行
    lines = content.split('\n')
    processed_lines = []

    for i, line in enumerate(lines):
        processed_lines.append(line)

        # 如果當前行不是空行，且下一行也不是空行，且下一行不是標題或列表
        if (i < len(lines) - 1 and
            line.strip() and
            lines[i + 1].strip() and
            not lines[i + 1].startswith('#') and
            not lines[i + 1].startswith('-') and
            not lines[i + 1].startswith('*') and
            not lines[i + 1].startswith('!')):

            # 檢查是否需要添加空行
            if not (i + 1 < len(lines) and lines[i + 1] == ''):
                processed_lines.append('')

    return '\n'.join(processed_lines)