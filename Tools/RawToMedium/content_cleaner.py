import re
from pathlib import Path

def clean_content(md_content):
    """清理和格式化 Markdown 內容"""
    content = md_content.strip()

    # 移除 Notion 導出的 metadata（如 "Status: Draft"）
    content = re.sub(r'^Status:\s*\w+\n*', '', content, flags=re.MULTILINE)

    # 移除其他常見的 metadata 格式
    content = re.sub(r'^(Tags?|Category|Author|Created|Updated|Page-?ID):\s*.+\n*', '', content, flags=re.MULTILINE)

    # 移除新增的 date 和 index metadata
    content = re.sub(r'^date:\s*.+\n*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^index:\s*.+\n*', '', content, flags=re.MULTILINE)

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
    import urllib.parse
    import os

    def find_best_match(target_name, image_mapping):
        """找到最佳匹配的圖片檔案"""
        print(f"\n=== 尋找圖片匹配: '{target_name}' ===")

        # 解碼目標檔名
        decoded_target = urllib.parse.unquote(target_name)
        print(f"解碼後目標: '{decoded_target}'")

        # 提取檔案擴展名
        target_ext = os.path.splitext(decoded_target)[1].lower()
        print(f"目標擴展名: '{target_ext}'")

        # 1. 完全匹配
        for orig_name, new_name in image_mapping.items():
            if orig_name == target_name or orig_name == decoded_target:
                print(f"[MATCH] 完全匹配: {orig_name} -> {new_name}")
                return new_name

        # 2. 解碼後匹配
        for orig_name, new_name in image_mapping.items():
            decoded_orig = urllib.parse.unquote(orig_name)
            if decoded_orig == decoded_target:
                print(f"[MATCH] 解碼匹配: {orig_name} -> {new_name}")
                return new_name

        # 3. 檔名（不含路徑）匹配
        target_basename = os.path.basename(decoded_target)
        for orig_name, new_name in image_mapping.items():
            orig_basename = os.path.basename(urllib.parse.unquote(orig_name))
            if orig_basename == target_basename:
                print(f"[MATCH] 檔名匹配: {orig_basename} -> {new_name}")
                return new_name

        # 4. 擴展名匹配（針對重複檔名如 圖片.png, 圖片 1.png）
        if target_ext:
            target_base = os.path.splitext(target_basename)[0]
            for orig_name, new_name in image_mapping.items():
                orig_decoded = urllib.parse.unquote(orig_name)
                orig_basename = os.path.basename(orig_decoded)
                orig_base = os.path.splitext(orig_basename)[0]
                orig_ext = os.path.splitext(orig_basename)[1].lower()

                # 檢查是否是同一系列的檔案（如 圖片.png, 圖片 1.png）
                if (orig_ext == target_ext and
                    (orig_base == target_base or
                     orig_base.startswith(target_base + ' ') or
                     target_base.startswith(orig_base + ' '))):
                    print(f"[MATCH] 系列檔案匹配: {orig_basename} -> {new_name}")
                    return new_name

        # 5. 部分匹配（處理截斷的路徑）
        for orig_name, new_name in image_mapping.items():
            orig_decoded = urllib.parse.unquote(orig_name)
            # 如果原始檔名包含目標檔名，或反之
            if (len(decoded_target) > 10 and decoded_target in orig_decoded) or \
               (len(orig_decoded) > 10 and orig_decoded in decoded_target):
                print(f"[MATCH] 部分匹配: {orig_name} -> {new_name}")
                return new_name

        # 6. 檔案大小或順序推測（最後手段）
        if target_ext:
            matching_exts = [(orig_name, new_name) for orig_name, new_name in image_mapping.items()
                           if os.path.splitext(urllib.parse.unquote(orig_name))[1].lower() == target_ext]
            if len(matching_exts) == 1:
                print(f"[MATCH] 唯一擴展名匹配: {matching_exts[0][0]} -> {matching_exts[0][1]}")
                return matching_exts[0][1]

        print(f"[NO MATCH] 無法找到匹配")
        return None

    def replace_image_path(match):
        # 提取圖片路徑和可能的圖片描述
        img_desc = match.group(1) if match.group(1) else "圖片"
        img_path = match.group(2)

        print(f"\n--- 處理圖片: {img_desc} ---")
        print(f"原始路徑: {img_path}")

        # 解碼路徑
        decoded_path = urllib.parse.unquote(img_path)
        print(f"解碼路徑: {decoded_path}")

        # 提取檔名
        original_name = decoded_path.split('/')[-1]
        print(f"提取檔名: {original_name}")

        # 尋找最佳匹配
        found_mapping = find_best_match(original_name, image_mapping)

        if found_mapping:
            # 使用 GitHub Raw URL
            github_url = f"{GITHUB_RAW_PREFIX}{post_slug}/images/{found_mapping}"
            print(f"[SUCCESS] 轉換為: {github_url}")
            return f"![{img_desc}]({github_url})"
        else:
            # 如果找不到對應，顯示詳細資訊
            print(f"[WARNING] 找不到圖片 '{original_name}' 的對應關係")
            print(f"可用的圖片對應:")
            for i, (orig, new) in enumerate(image_mapping.items(), 1):
                print(f"  {i}. {orig} -> {new}")

            # 保持原始格式但使用 GitHub URL 嘗試
            github_url = f"{GITHUB_RAW_PREFIX}{post_slug}/images/unknown_{original_name}"
            print(f"[FALLBACK] 使用備用路徑: {github_url}")
            return f"![{img_desc}]({github_url})"

    # 處理正常的圖片標記 ![描述](路徑)
    print(f"\n=== 開始處理圖片路徑轉換 ===")
    print(f"圖片對應表: {image_mapping}")

    # 手動解析圖片標記，正確處理嵌套括號
    import re

    def find_image_links(content):
        """手動解析圖片連結，正確處理括號"""
        results = []
        i = 0
        while i < len(content):
            # 尋找 ![
            if content[i:i+2] == '![':
                # 找到描述的結束
                desc_start = i + 2
                desc_end = content.find('](', desc_start)
                if desc_end == -1:
                    i += 1
                    continue

                description = content[desc_start:desc_end]

                # 找到路徑的開始
                path_start = desc_end + 2

                # 手動找到匹配的結束括號
                paren_count = 1
                path_end = path_start
                while path_end < len(content) and paren_count > 0:
                    if content[path_end] == '(':
                        paren_count += 1
                    elif content[path_end] == ')':
                        paren_count -= 1
                    if paren_count > 0:
                        path_end += 1

                if paren_count == 0:
                    path = content[path_start:path_end]
                    results.append((description, path))
                    i = path_end + 1
                else:
                    i += 1
            else:
                i += 1
        return results

    image_matches = find_image_links(content)
    print(f"找到 {len(image_matches)} 個圖片標記:")
    for i, (desc, path) in enumerate(image_matches, 1):
        print(f"  {i}. 描述: '{desc}', 路徑: '{path}'")

    # 使用手動解析進行替換
    def safer_replace(content):
        """安全地替換圖片路徑"""
        result = content
        # 從後往前替換，避免位置偏移
        matches_with_pos = []

        i = 0
        while i < len(result):
            if result[i:i+2] == '![':
                # 找到描述的結束
                desc_start = i + 2
                desc_end = result.find('](', desc_start)
                if desc_end == -1:
                    i += 1
                    continue

                description = result[desc_start:desc_end]

                # 找到路徑的開始
                path_start = desc_end + 2

                # 手動找到匹配的結束括號
                paren_count = 1
                path_end = path_start
                while path_end < len(result) and paren_count > 0:
                    if result[path_end] == '(':
                        paren_count += 1
                    elif result[path_end] == ')':
                        paren_count -= 1
                    if paren_count > 0:
                        path_end += 1

                if paren_count == 0:
                    path = result[path_start:path_end]
                    matches_with_pos.append((i, path_end + 1, description, path))
                    i = path_end + 1
                else:
                    i += 1
            else:
                i += 1

        # 從後往前替換
        for start, end, desc, path in reversed(matches_with_pos):
            # 創建一個模擬的 match 物件
            class MockMatch:
                def __init__(self, desc, path):
                    self._groups = ['', desc, path]
                def group(self, n):
                    return self._groups[n]

            mock_match = MockMatch(desc, path)
            new_link = replace_image_path(mock_match)
            result = result[:start] + new_link + result[end:]

        return result

    processed_content = safer_replace(content)

    # 處理可能的截斷路徑殘留
    # 清理截斷的檔名片段
    truncated_patterns = [
        r'[_-]+[A-Z0-9_-]*\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d+\.(gif|png|jpg|jpeg)\)',
        r'\w+_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d+\.(gif|png|jpg|jpeg)$'
    ]

    for pattern in truncated_patterns:
        cleaned = re.sub(pattern, '', processed_content)
        if cleaned != processed_content:
            print(f"清理截斷路徑: {pattern}")
            processed_content = cleaned

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