---
title: "回饋系統框架（80% AI）"
date: 2025-09-21
category: ironman-2025
slug: post-2025_09_21-day7-回饋系統框架80-ai
day: 7
---

# Day7 - 回饋系統框架（80% AI）


就是只音效、特效、震動、停頓之類的回饋，回饋也有各種方案，震動要用預設 Camera 還是 CinemaMachine？特效要不要物件池？音效怎麼播放？要有統一的時間管理器嗎？

其實跟處理 Input 時一樣，具體的實現方案都不是重點，重點是接口的規範以及要選擇不同方案時的可擴展性。

我之前的做法應該是各自實做每個系統，需要時再各自觸發吧。但這次我要改用一個統一的回饋觸發系統，接口簡化到使用者只需要傳入一個 key 就好（和可選的 Context 參數）。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_8.png)

要執行什麼效果？透過外部的配置文件定義。要怎麼執行？讓每個專案各自實做和註冊就好，擴展點有三個：定義資料格式、定義資料來源和效果執行器。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_2.png)

假設定義一個回饋為 “Hit.Crit” ，裡面包括一個音效回饋定義 (audioFeedbackData) 和震動回饋定義 (ShadeFeedbackData)，那當使用者觸發 Hit.Crit 時，系統就會檢查有沒有註冊的執行器，然後把對應 Data 交給執行器播放回饋。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_3.png)

這樣的好處是框架本身不用提供任何解決方案，也不綁死任何實做。

回饋的資料來源很自由，可以程式硬編碼、用 ScriptableObject 定義或載入 Google Sheet，需要更多種類也可以繼承 IFeedBackData 定義新回饋。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_4.png)

執行器也是，專案只要繼承 IFeedbackExecutor 介面，透過泛型 <T> 指定執行的回饋類型，就能實現不同的方案。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_5.png)

最棒的是，這套框架可以兼容幾乎任何現成的解決方案，他只規範了程式端調用的規則，專案可以根據需求實做，就算要串接插件也行。

這裡就插上了一個 AssetStore 買的插件 [Feel](https://assetstore.unity.com/packages/tools/particles-effects/feel-183370)，裡面集成了超大量的回饋效果「實做」，包括音效、震動、時間效果或 Transform 效果等等。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_6.png)

比較麻煩的是，有些情況要共用回饋執行器，像是全域的音效播放、粒子特效等等，但有些回饋是每個物件要各自執行的，像是物體震動、旋轉、拉伸等。

所以我用修飾模式（Decorator pattern）做了一個可覆寫的執行器註冊器，每個物件可以把各自執行的回饋覆寫進註冊器，執行時會優先選擇覆寫方案，找不到執行器才會使用共享的。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_7.png)

測試案例的執行，兩個方塊都觸發 “Hit.Crit” ，會播放共享的 Audio Feedback（目前只是 Print Log），但 Transform 回饋是執行各自覆寫的效果。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-7_2025-09-21/images/image_1.gif)