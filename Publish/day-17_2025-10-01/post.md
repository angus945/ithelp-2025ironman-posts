---
title: "數值公式計算（80% AI）"
date: 2025-10-01
category: ironman-2025
slug: post-2025_10_01-day17-數值公式計算80-ai
day: 17
---

# Day 17 - 數值公式計算（80% AI）


數值計算，應該是所有遊戲都會有的需求，但自己做這部分功能的經驗也不多，以前就是哪裡需要計算就寫在哪，這次也問問看 GPT 有沒有接口化實現方式。（其實應該先叫他給更多種方案才對）

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-17_2025-10-01/images/image_1.png)

總之，這個方案的重點就是用泛型 <T> 指定的輸入輸出的格式，透過配對尋找需要的算法，專案可以實作自己的方案然後註冊給系統，使用者也不需要知道具體的算法是什麼。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-17_2025-10-01/images/image_2.png)

然後提供一個 Unity ScriptableObject 的基底類。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-17_2025-10-01/images/image_3.png)

再讓 AI 針對 ScriptableObject 提供一個試算結果的 CustomInspector。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-17_2025-10-01/images/image_4.png)

這樣就能方便的調整配置參數和測試試算結果了，如果試玩的時候感覺數值表現怪怪的就可以先來這裡初步除錯，看是不是算法有問題或參數填錯。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-17_2025-10-01/images/image_5.png)

至於效果嘛…我也不確定，畢竟這個做法也是第一次嘗試，等後面幾篇的串接應該就會有心得了。