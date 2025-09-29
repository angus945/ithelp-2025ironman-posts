---
title: "重構視覺容器（20% AI）"
date: 2025-10-09
category: ironman-2025
slug: post-2025_10_09-day25-重構視覺容器20-ai
day: 25
---

# Day 25 - 重構視覺容器（20% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

視覺容器是重構改動比較大的部分，原本腳本的職責太混雜了，所以幾乎整個重寫。

Domain 是裡有視覺容器的顯示模式，計算用的 ValueObject 、策略接口以及策略模式算法定義。float3 是使用 Unity.Mathematics 函式庫的數學變數。（其實不應該，但為了省事就用了）

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_2.png)

Application 定義了容器需要的接口、各種 Port 接口以及各種視覺容器的 UseCase，UseCase 透過對應的 Port 執行具體行為，例如更新顯示模式、設置錨點、旋轉、翻轉等等。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_3.png)

Infrastructure 進行 Port 的 Unity Adapter 轉換實作，把攝影機資訊、Unity Aimator 等資訊轉接給 Application 的 UseCase。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_4.png)

最後 Presentation 提供一個 Monobehavior 的 Controller 提供外部操操作的進入點

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_5.png)

為了避免計算互相干擾，不同顯示功能分成不同 Transform 執行，最上層是面對攝影機的 Billboard 算法、第二層是控制中心點偏移、第三層負責旋轉和翻轉，最底下則會放入真正的視覺物件實例。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_6.png)

而要操作視覺容器的 Character 方面也增加一個 Adapter，把 VisualController 轉接成狀態機 Addon 使用的 IVisualPort 。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_7.png)

Character 的視覺幾乎是沿用舊版，由兩個 Addon 分別處理動畫播放（根據狀態）和翻轉（根據行動時面對的方向）。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_8.png)

雖然都一樣，但還是放張新動圖示意。

![STUST_Project_4-1 - SceneRenderTest - Windows, Mac, Linux - Unity 6.2 (6000.2.0f1) _DX12_ 2025-09-19 08-36-55_0 (1).gif](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_1.gif)

視覺容器也沒有用嚴謹的分層，但目前的架構已經夠好維護了，真的需要再回來改就好。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-25_2025-10-09/images/image_9.png)