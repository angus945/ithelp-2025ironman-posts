---
title: "整合技能系統（< 5% AI）"
date: 2025-09-27
category: ironman-2025
slug: post-2025_09_27-day13-整合技能系統-5-ai
day: 13
---

# Day13 - 整合技能系統（< 5% AI）


有技能系統框架後先進行一些測試的實作跟整合，先定義了兩個簡單的技能，Print Log 還有發射子彈。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-13_2025-09-27/images/image_4.png)

實作子彈技能，從 Context 取得施放者和目標位置，把方向資訊寫入 Context、判斷發動條件、最後發動，透過 context 中提供的工場生成子彈並發射。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-13_2025-09-27/images/image_2.png)

然後把人物狀態機補上施放技能的狀態，還有觸發技能的 Addon。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-13_2025-09-27/images/image_3.png)

最後把玩家輸入 addon 替換成隨機行為的 addon，遊戲敵人的樣子也有了。角色發射的那個大球就是技能。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-13_2025-09-27/images/image_1.gif)

啊對也補充一下，我的狀態機實作中不包括邏輯角色（AI、玩家輸入），人物或敵人的狀態機只用來管理可執行行為之間的邏輯跟轉換條件。

遊戲 AI 或邏輯可以用 Addon 掛載的方式運作，所以方案也不綁死，可以掛玩家輸入、簡單的隨機行為、另一個 AI 狀態機或是串外部的行為樹插件當決策大腦。