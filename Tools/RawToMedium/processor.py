from pathlib import Path

from .config import init_directories, PUBLISH_DIR
from .metadata_extractor import extract_metadata_from_filename, generate_frontmatter
from .content_cleaner import clean_content, process_image_paths, format_for_medium
from .image_handler import find_image_folder, copy_images_to_publish

def process_single_file(md_path):
    """處理單個 Markdown 檔案"""
    md_path = Path(md_path)

    if not md_path.exists():
        raise FileNotFoundError(f"找不到檔案: {md_path}")

    print(f"\n開始處理: {md_path.name}")

    # 1. 提取元數據
    metadata = extract_metadata_from_filename(md_path)
    print(f"提取元數據: {metadata['title']} (Day {metadata['day_number']})")

    # 2. 讀取檔案內容
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except UnicodeDecodeError:
        with open(md_path, 'r', encoding='utf-8-sig') as f:
            raw_content = f.read()

    # 3. 清理內容
    cleaned_content = clean_content(raw_content)

    # 4. 尋找和處理圖片
    image_folder = find_image_folder(md_path)
    image_mapping = {}

    if image_folder:
        print(f"找到圖片資料夾: {image_folder}")

        # 建立目標資料夾 - 使用新的命名格式 day-{index}_{date}
        if metadata['day_number']:
            folder_name = f"day-{metadata['day_number']}_{metadata['date']}"
        else:
            folder_name = metadata['slug']
        target_post_folder = PUBLISH_DIR / folder_name
        target_images_folder = target_post_folder / "images"

        # 複製圖片
        image_mapping = copy_images_to_publish(image_folder, target_images_folder)
    else:
        print("未找到對應的圖片資料夾")
        # 使用新的命名格式 day-{index}_{date}
        if metadata['day_number']:
            folder_name = f"day-{metadata['day_number']}_{metadata['date']}"
        else:
            folder_name = metadata['slug']
        target_post_folder = PUBLISH_DIR / folder_name

    # 5. 處理內容中的圖片路徑
    processed_content = process_image_paths(
        cleaned_content,
        image_mapping,
        folder_name
    )

    # 6. 格式化為 Medium 格式
    medium_content = format_for_medium(processed_content)

    # 7. 生成最終內容
    frontmatter = generate_frontmatter(metadata)
    final_content = frontmatter + medium_content

    # 8. 寫入目標檔案
    target_post_folder.mkdir(parents=True, exist_ok=True)
    output_path = target_post_folder / "post.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"轉換完成: {output_path}")
    return output_path, metadata

def process_multiple_files(md_paths):
    """批次處理多個 Markdown 檔案"""
    results = []
    failed_files = []

    for md_path in md_paths:
        try:
            result = process_single_file(md_path)
            results.append(result)
        except Exception as e:
            print(f"處理檔案失敗 {md_path}: {e}")
            failed_files.append((md_path, str(e)))

    return results, failed_files

def setup_environment():
    """設置處理環境"""
    init_directories()
    print("環境設置完成")