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
    import re

    def extract_complete_image_path(content, start_pos):
        """手動提取完整的圖片路徑，處理包含括號的情況"""
        # 從 ]( 後開始找
        paren_start = content.find('](', start_pos)
        if paren_start == -1:
            return None, -1

        path_start = paren_start + 2

        # 手動計數括號，找到真正的結束位置
        paren_count = 1
        pos = path_start
        while pos < len(content) and paren_count > 0:
            if content[pos] == '(':
                paren_count += 1
            elif content[pos] == ')':
                paren_count -= 1
            if paren_count > 0:
                pos += 1

        if paren_count == 0:
            return content[path_start:pos], pos
        else:
            return None, -1

    def decode_and_extract_filename(img_path):
        """解碼路徑並提取檔名"""
        print(f"\n=== 解碼路徑 ===")
        print(f"原始路徑: {img_path}")

        # 完整解碼路徑
        decoded_path = urllib.parse.unquote(img_path)
        print(f"解碼後路徑: {decoded_path}")

        # 提取檔名（路徑的最後部分）
        if '/' in decoded_path:
            filename = decoded_path.split('/')[-1]
        else:
            filename = decoded_path

        print(f"提取檔名: {filename}")
        return filename

    def find_matching_image(filename, image_mapping):
        """在圖片映射中找到匹配的檔案"""
        print(f"\n=== 尋找匹配 ===")
        print(f"目標檔名: '{filename}'")
        print(f"可用圖片:")
        for i, (orig, new) in enumerate(image_mapping.items(), 1):
            print(f"  {i}. {orig} -> {new}")

        # 1. 完全匹配
        if filename in image_mapping:
            print(f"[MATCH] 完全匹配: {filename} -> {image_mapping[filename]}")
            return image_mapping[filename]

        # 2. 解碼後匹配
        for orig_name, new_name in image_mapping.items():
            decoded_orig = urllib.parse.unquote(orig_name)
            if decoded_orig == filename:
                print(f"[MATCH] 解碼匹配: {orig_name} -> {new_name}")
                return new_name

        # 3. 部分匹配（檔名主體相同）
        filename_base = filename.split('.')[0] if '.' in filename else filename
        for orig_name, new_name in image_mapping.items():
            orig_base = orig_name.split('.')[0] if '.' in orig_name else orig_name
            orig_decoded_base = urllib.parse.unquote(orig_base)

            if (filename_base == orig_base or
                filename_base == orig_decoded_base or
                orig_base == filename_base or
                orig_decoded_base == filename_base):
                print(f"[MATCH] 檔名主體匹配: {orig_name} -> {new_name}")
                return new_name

        print(f"[NO MATCH] 找不到匹配")
        return None

    def replace_image_path(match):
        # 提取圖片描述和路徑
        img_desc = match.group(1) if match.group(1) else "圖片"
        img_path = match.group(2)

        print(f"\n--- 處理圖片 ---")
        print(f"描述: {img_desc}")
        print(f"原始路徑: {img_path}")

        # 解碼並提取檔名
        filename = decode_and_extract_filename(img_path)

        # 尋找匹配的圖片
        found_mapping = find_matching_image(filename, image_mapping)

        if found_mapping:
            github_url = f"{GITHUB_RAW_PREFIX}{post_slug}/images/{found_mapping}"
            print(f"[SUCCESS] 轉換成功: {github_url}")
            return f"![{img_desc}]({github_url})"
        else:
            print(f"[FAIL] 轉換失敗，保持原路徑")
            return match.group(0)

    print(f"\n=== 開始處理圖片路徑轉換 ===")
    print(f"可用圖片對應: {len(image_mapping)} 個")

    # 使用更準確的正則表達式，但需要手動處理括號問題
    # 先找出所有圖片標記的位置
    processed_content = content

    # 使用改進的匹配，能處理包含括號的路徑
    def safer_regex_replace(content):
        result = ""
        last_end = 0

        # 尋找所有 ![...](
        for match in re.finditer(r'!\[([^\]]*)\]\(', content):
            # 添加匹配前的內容
            result += content[last_end:match.start()]

            # 提取描述
            desc = match.group(1)

            # 手動提取完整路徑
            complete_path, path_end = extract_complete_image_path(content, match.start())

            if complete_path is not None:
                # 創建模擬的 match 對象
                class MockMatch:
                    def __init__(self, desc, path):
                        self._desc = desc
                        self._path = path
                    def group(self, n):
                        if n == 0:
                            return f"![{self._desc}]({self._path})"
                        elif n == 1:
                            return self._desc
                        elif n == 2:
                            return self._path
                        return ""

                mock_match = MockMatch(desc, complete_path)
                replacement = replace_image_path(mock_match)
                result += replacement
                last_end = path_end + 1
            else:
                # 如果無法解析路徑，保持原樣
                result += match.group(0)
                last_end = match.end()

        # 添加剩餘內容
        result += content[last_end:]
        return result

    processed_content = safer_regex_replace(content)

    # 清理可能剩餘的截斷文字
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