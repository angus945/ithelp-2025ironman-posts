# RawToMedium - Raw 到 Medium 格式轉換工具

這是一個專為鐵人賽文章設計的轉換工具，能夠直接將 Raw 資料夾中的 Markdown 檔案轉換成適合 Medium 發布的格式。

## 特色功能

- **簡化流程**：跳過複雜的 Converter + Publisher 兩階段流程
- **自動化處理**：從檔名自動提取日期、標題等元數據
- **圖片處理**：自動找到對應圖片、壓縮並轉換為 GitHub URL
- **格式清理**：移除 Notion 導出的 metadata，格式化為 Medium 友好格式
- **鐵人賽特化**：專門針對 "Day1 - 標題" 格式設計

## 安裝需求

確保已安裝相關依賴：
```bash
pip install Pillow PyYAML
```

## 使用方式

### 1. 轉換單個檔案

```bash
# 使用完整路徑
python -m Tools.RawToMedium.converter "Raw/Day1 - 用 Vibe Coding 協助開發畢專遊戲原型.md"

# 使用相對路徑（會在 Raw 資料夾中查找）
python -m Tools.RawToMedium.converter "Day1 - 用 Vibe Coding.md"
```

### 2. 批次轉換所有檔案

```bash
python -m Tools.RawToMedium.converter --all
```

### 3. 列出可用檔案

```bash
python -m Tools.RawToMedium.converter --list
```

### 4. 程式化使用

```python
from Tools.RawToMedium.processor import process_single_file

result_path, metadata = process_single_file("Raw/Day1 - 標題.md")
print(f"轉換完成: {result_path}")
print(f"標題: {metadata['title']}")
```

## 輸出結構

轉換後的檔案會放在 `Diary-Publish/medium-posts/` 目錄下：

```
Diary-Publish/
└── medium-posts/
    └── post-2025_09_14-day1-vibe-coding/
        ├── post.md           # Medium 格式文章
        └── images/           # 相關圖片（如果有）
            ├── image_1.jpg
            └── image_2.gif
```

## 元數據提取規則

### Day 格式檔案
檔名格式：`Day1 - 標題 [hash].md`

提取結果：
- **標題**：`標題`
- **日期**：根據 Day 數字計算（從 2025-09-14 開始）
- **Slug**：`post-2025_09_14-day1-標題`
- **分類**：`ironman-2025`

### 一般檔案
使用當前日期和檔名作為基礎生成元數據。

## 圖片處理

1. **自動查找**：根據 MD 檔名找到對應的圖片資料夾
2. **安全檔名**：將特殊字符轉換為安全的檔名
3. **壓縮處理**：大於 2MB 的圖片會自動壓縮
4. **URL 轉換**：本地路徑轉換為 GitHub Raw URL

生成的圖片 URL 格式：
```
https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/medium-posts/post-slug/images/image.jpg
```

## 內容清理

- 移除 Notion 導出的 `Status: Draft` 等 metadata
- 清理多餘的空行
- 確保標題和段落有適當的空行分隔
- 保持 Markdown 格式的完整性

## Frontmatter 格式

生成的文章會包含以下 frontmatter：

```yaml
---
title: "文章標題"
date: 2025-09-14
category: ironman-2025
slug: post-2025_09_14-day1-title
day: 1
---
```

## 錯誤處理

- 找不到圖片資料夾時會給出警告但不中斷處理
- 圖片壓縮失敗時會使用原檔案
- 批次處理時會顯示失敗的檔案和原因

## 模組結構

- `config.py` - 設定檔案和路徑管理
- `metadata_extractor.py` - 從檔名提取元數據
- `content_cleaner.py` - 內容清理與格式化
- `image_handler.py` - 圖片處理功能
- `processor.py` - 主要處理邏輯
- `converter.py` - 命令行介面

## 注意事項

- 確保 Raw 資料夾存在且包含 Markdown 檔案
- 圖片資料夾應該與 MD 檔案名稱對應
- 支援的圖片格式：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`
- 輸出的 GitHub URL 指向 `ithelp-2025ironman-posts` 倉庫

## 疑難排解

### 找不到圖片資料夾
確認圖片資料夾名稱與 MD 檔案名稱匹配（去除 hash 後綴）。

### 轉換失敗
檢查檔案編碼是否為 UTF-8，或嘗試使用完整路徑。

### 圖片無法顯示
確認 GitHub 倉庫是公開的，且圖片已正確上傳。