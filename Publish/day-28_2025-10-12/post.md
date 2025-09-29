---
title: "射彈系統（50% AI）"
date: 2025-10-12
category: ironman-2025
slug: post-2025_10_12-day28-射彈系統50-ai
day: 28
---

# Day 28 - 射彈系統（50% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

射彈 Projectile，各種遊戲中很常出現的投射物，一個俯視角動作遊戲一定也有。原本測試用的技能就是發射射彈，不過那時只是用臨時的 Prefab Instantiate 方便測試。

這次重構先設計了射彈的框架，總之也簡單描述需求，看看 GPT 有什麼看法。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_1.png)

GPT 給了蠻完整的方案，但也是很 OverDesign，所以我先挑出幾個關鍵接口，整理成我期望的框架後再給 GPT 看，然後再拿 GPT 的修正版修成我要的最終簡化版。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_2.png)

最後也是很簡化的框架，使用組件化容器 + 載荷的方案，射彈需要的組件包括碰撞檢測和移動軌跡計算，一樣全部接口化，不綁死方案，讓每個專案各自實施需要的做法。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_3.png)

擊中效果與子彈的實體（或視覺）則透過載荷 IProjectilePayload 處理，把射彈的各種活動時機也做成接口，如果載荷需要什麼效果就自己繼承實作。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_4.png)

本體就是射彈的基本屬性、組件和載荷的整合，使用前可以先設置碰撞、路徑組件、放入載荷，然後再透過 Activate 啟動射彈，用 Tick 更新活動狀態。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_5.png)

原本還想弄個工廠或物件池框架，但實做起來發現有點過度設計，所以暫時不管。

至於專案的實施，碰撞部分我先使用一個 Bridge 腳本跟 Monobehavior 的 OnCollisionEnter 檢測整合。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_6.png)

移動軌跡先用了簡單的直線移動，之後要拋物線、追蹤、抖動、軌道繞行之類的只要繼承介面實作就好，也可以用修飾模式 Decorator 組合多種移動軌跡，或是整合資料驅動的計算方案。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_7.png)

至於載荷，我實做了一個攜帶 GameObject 的載荷，如了能讓射彈的視覺特效附加在子彈上，也能把各種遊戲物件直接當射彈發射。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_8.png)

能攜帶物件也是我用載荷方案的主要原因，前面的文有提到過，遊戲目前會被投擲或發射出去的東西有三種，第一是玩家的武器、第二是從武器脫離的敵人、第三才是真正的射彈。

![Movie_019_0.gif](Day%2019%20-%20%E6%95%B5%E4%BA%BA%E8%84%AB%E9%9B%A2%E6%95%88%E6%9E%9C%EF%BC%88%2010%25%20AI%EF%BC%89%2026964707f2db800c85d3f05e6d089a93/Movie_019_0.gif)

原本三個是完全獨立的做法，現在可以全部用相同的射彈方案解決。

我做提供一個 ProjectileInstance 當做射彈與 Unity 物件的轉接，用 FixedUpdate 更新射彈，然後把位置設置給 Rigidbody，射彈就能在 Unity 場景中活動了。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_9.png)

發射的時候就可以讓射彈攜帶其他物件，武器投擲時就把武器物件當載荷、敵人脫離時就把敵人當載荷、單純的傷害射彈就用視覺特效（和擊中效果）當載荷內容。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-28_2025-10-12/images/image_10.png)

其實這篇原本是武器的重構，但開發時發現武器用狀態機也有點過度設計了，所以先做了射彈系統，這樣玩家投擲時就能直接把武器當載荷發射出去，大幅簡化武器系統的複雜度