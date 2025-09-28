---
title: "視覺容器 ( 10% AI )"
date: 2025-09-23
category: ironman-2025
slug: post-2025_09_23-day9-視覺容器-10-ai
day: 9
---

# Day9 -視覺容器 (< 10% AI )

今天的文要開始處理視覺顯示。

我們要用類似邪教羊《Cult of the Lamb》的 2.5D 紙片人顯示角色，所以讓 GPT 幫我寫了幾種紙片物件的顯示方式，無旋轉、Billboard、水平 Billboard、Z 軸朝上等等，可以根據需求切換模式。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_8.png)

然後是遊戲最~~荒唐~~核心的串起敵人部分，為了讓紙片物件的串接效果比較理想，我也手動做了一些實驗，構想物件之間的 Transform 和子父物件設置流程。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_3.png)

然後讓 GPT 寫一個讓平面根據相交軸旋轉的算法，整合進自己的 Util 方便後續調用。

![STUST_Project_4-1 - VisualContainerAttachTest - Windows, Mac, Linux - Unity 6 (6000.0.34f1)_ _DX11_ 2025-09-03 13-50-30_0.gif](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_1.gif)

剛好武器飛行時會是 Z Up，而生物會是指向攝影機的 45 度 billboard，武器可以直接插進生物的紙片 Sprite，所以只要玩家撿起來時把夾角縮小，就能維持穿刺的視覺效果。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_3.png)

補充一下，這是我另外做的 DepthWriteSpriteShader ，要有深度寫入才能做到 Sprite 穿插效果。

除此之外，視覺容器除了控制 billboard 效果之外，也是動畫播放的接口，因為有揮動武器的需求（需要有 Transform 錨點），所以動畫方案是 Unity Animation，但沒有使用 Animator 狀態機，而是直接用名稱指定播放的動畫。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_4.png)

我外掛一個動畫同步器給狀態機，他就會根據當前狀態資訊自動選擇動畫播放。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_5.png)

動畫的播放進度是這個 Addon 指定的，但因為我把狀態機設定成 FixedUpdate Tick，所以為了確保動畫播放正常，Play 要在 Monobehavior 的 Update 中調用才行。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_6.png)

順帶一提 ，雖然 State 本身要用專門的 Tick 更新，但 Addon 可以兼容 Monobehavior 的生命週期 ，Input 參數也是在 Update 寫入狀態機的。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-9_2025-09-23/images/image_7.png)
