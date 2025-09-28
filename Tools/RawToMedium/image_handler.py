import shutil
import urllib.parse
from pathlib import Path
from PIL import Image

from .config import RAW_DIR, SUPPORTED_IMAGE_EXTENSIONS

def find_image_folder(md_path):
    """根據 Markdown 檔案路徑找到對應的圖片資料夾"""
    # 移除檔名末尾的 hash 後綴
    clean_name = md_path.stem
    if ' ' in clean_name and len(clean_name.split()[-1]) == 32:
        # 如果最後一個部分是 32 位字符，可能是 hash
        try:
            int(clean_name.split()[-1], 16)  # 嘗試解析為十六進制
            clean_name = ' '.join(clean_name.split()[:-1])
        except ValueError:
            pass  # 不是 hash，保持原樣

    # 尋找對應的圖片資料夾
    potential_folders = []

    # 1. 先找完整名稱匹配的資料夾
    for candidate in RAW_DIR.rglob("*"):
        if candidate.is_dir():
            if candidate.name == md_path.stem:
                potential_folders.append(candidate)
            elif candidate.name == clean_name:
                potential_folders.append(candidate)

    # 2. 如果沒找到，嘗試找包含檔名主要部分的資料夾
    if not potential_folders:
        main_part = clean_name.split('-')[0].strip() if '-' in clean_name else clean_name
        for candidate in RAW_DIR.rglob("*"):
            if candidate.is_dir() and main_part in candidate.name:
                potential_folders.append(candidate)

    # 返回第一個找到的資料夾，並檢查是否包含圖片
    for folder in potential_folders:
        if has_images(folder):
            return folder

    return None

def has_images(folder_path):
    """檢查資料夾是否包含圖片檔案"""
    if not folder_path or not folder_path.exists():
        return False

    for file in folder_path.iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
            return True
    return False

def safe_filename(original_name):
    """生成安全的檔案名稱（移除特殊字符）"""
    # 解碼 URL 編碼
    decoded = urllib.parse.unquote(original_name)

    # 保留檔案擴展名
    path_obj = Path(decoded)
    name = path_obj.stem
    ext = path_obj.suffix

    # 移除或替換不安全的字符
    safe_name = ''.join(c if c.isalnum() or c in '.-_' else '_' for c in name)

    # 避免名稱過長
    if len(safe_name) > 50:
        safe_name = safe_name[:50]

    # 移除開頭結尾的下劃線和點號
    safe_name = safe_name.strip('._')

    # 如果名稱為空，使用預設名稱
    if not safe_name:
        safe_name = 'image'

    return f"{safe_name}{ext}"

def compress_image(image_path, target_path, max_bytes=2048*1024, quality=85):
    """壓縮圖片到指定大小以下"""
    try:
        with Image.open(image_path) as img:
            # 如果原檔案已經很小，直接複製
            if image_path.stat().st_size <= max_bytes:
                shutil.copy2(image_path, target_path)
                return

            # 壓縮圖片
            img.save(target_path, quality=quality, optimize=True)

            # 如果壓縮後仍然太大，繼續降低品質
            while target_path.stat().st_size > max_bytes and quality > 30:
                quality -= 10
                img.save(target_path, quality=quality, optimize=True)

            print(f"壓縮圖片: {image_path.name} -> {target_path.name}")

    except Exception as e:
        print(f"壓縮圖片失敗 {image_path}: {e}")
        # 如果壓縮失敗，直接複製原檔案
        shutil.copy2(image_path, target_path)

def copy_images_to_publish(image_folder, target_folder):
    """將圖片從來源資料夾複製到目標發布資料夾"""
    if not image_folder or not image_folder.exists():
        return {}

    target_folder.mkdir(parents=True, exist_ok=True)
    image_mapping = {}

    print(f"\n=== 開始複製圖片到發布資料夾 ===")
    print(f"來源資料夾: {image_folder}")
    print(f"目標資料夾: {target_folder}")

    # 收集所有圖片檔案並排序
    image_files = []
    for img_file in image_folder.iterdir():
        if img_file.is_file() and img_file.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
            image_files.append(img_file)
            print(f"發現圖片: {img_file.name} (大小: {img_file.stat().st_size} bytes)")

    # 按檔名排序確保一致性（先按檔名主體，再按數字後綴）
    def sort_key(file_path):
        name = file_path.stem
        # 處理類似 "圖片 1", "圖片 2" 的排序
        import re
        match = re.match(r'^(.+?)(\s+(\d+))?$', name)
        if match:
            base_name = match.group(1)
            number = int(match.group(3)) if match.group(3) else 0
            return (base_name, number)
        return (name, 0)

    image_files.sort(key=sort_key)
    print(f"排序後的圖片順序:")
    for i, img_file in enumerate(image_files, 1):
        print(f"  {i}. {img_file.name}")

    # 使用 image_{index} 命名格式
    for index, img_file in enumerate(image_files, 1):
        # 生成新的檔案名稱：image_{index}.{extension}
        ext = img_file.suffix.lower()
        new_name = f"image_{index}{ext}"
        target_path = target_folder / new_name

        print(f"\n--- 處理圖片 {index}/{len(image_files)} ---")
        print(f"原始檔名: {img_file.name}")
        print(f"新檔名: {new_name}")

        # 複製並可能壓縮圖片
        try:
            if img_file.suffix.lower() in {'.jpg', '.jpeg', '.png'}:
                print(f"壓縮圖片: {img_file.name}")
                compress_image(img_file, target_path)
            else:
                print(f"直接複製: {img_file.name}")
                shutil.copy2(img_file, target_path)

            # 建立多種檔名對應關係，包括可能的變體
            original_name = img_file.name

            # 1. 完整檔名對應
            image_mapping[original_name] = new_name

            # 2. URL 編碼版本對應
            import urllib.parse
            encoded_name = urllib.parse.quote(original_name)
            if encoded_name != original_name:
                image_mapping[encoded_name] = new_name

            # 3. 部分編碼版本（常見於 Notion 匯出）
            partial_encoded = original_name.replace(' ', '%20')
            if partial_encoded != original_name:
                image_mapping[partial_encoded] = new_name

            # 4. 檔名主體對應（不含副檔名）
            stem_name = img_file.stem
            image_mapping[stem_name] = new_name

            print(f"[OK] 建立對應關係:")
            print(f"  - {original_name} -> {new_name}")
            if encoded_name != original_name:
                print(f"  - {encoded_name} -> {new_name}")
            if partial_encoded != original_name:
                print(f"  - {partial_encoded} -> {new_name}")
            print(f"  - {stem_name} -> {new_name}")

        except Exception as e:
            print(f"[ERROR] 複製圖片失敗 {img_file}: {e}")

    print(f"\n=== 圖片複製完成 ===")
    print(f"共複製 {len(image_files)} 個圖片檔案")
    print(f"建立 {len(image_mapping)} 個檔名對應關係")
    print(f"完整對應表:")
    for orig, new in image_mapping.items():
        print(f"  {orig} -> {new}")

    return image_mapping