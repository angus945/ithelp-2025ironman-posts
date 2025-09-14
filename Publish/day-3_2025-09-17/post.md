---
title: "玩家輸入方案（95% AI）"
date: 2025-09-17
category: ironman-2025
slug: post-2025_09_17-day3-玩家輸入方案95-ai
day: 3
---

# Day3 - 玩家輸入方案（95% AI）


date: 2025/09/17

index: 3

輸入系統，化成灰都能認得的需求，每個專案都要做一次的功能，但解決方案各有不同，要用新舊版的 InputSystem？還是用經典的 Input.GetKey 方案？要支援把手嗎？鍵位要怎麼擺放？

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-3_2025-09-17/images/image_5.png)

具體的做法其實不重要，因為無論用哪種方案，輸入跟遊戲之間都應該擋一個接口做抽象化。比較好的做法是讓遊戲系統依賴抽象的接口，而非某個具體的解決方案。

所以，我直接把討論時列的操作需求（上面那張圖）複製貼給 ChatGPT，要他生了遊戲用的輸入接口，裡面包括玩家需要的基本操作，如移動、翻滾、攻擊等。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-3_2025-09-17/images/image_1.png)

接著要他補充補充輸入系統的框架，包括抽象接口、按鈕判斷邏輯、攝影機來源、游標點擊（因為鍵鼠操作要透過滑鼠控制角色攻擊方向）和工廠等。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-3_2025-09-17/images/image_2.png)

然後是具體的輸入方案實現，有接口之後也讓 GPT 生成各種輸入方案的實作，有一個舊版鍵鼠 Input 和三個使用 NewInputSystem 的方案，分別是硬編碼鍵盤、硬編碼搖桿與 InputAsset 配置。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-3_2025-09-17/images/image_3.png)

最後然後讓 GPT 生成一個能顯示輸入狀態的 GUI 做手動測試，這樣不用任何玩家角色就能測各種輸入方案是否正常運作了。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-3_2025-09-17/images/image_4.png)

有這個接口，之後要用其他方案、改變鍵位或串接外部的插件都不是問題 :D