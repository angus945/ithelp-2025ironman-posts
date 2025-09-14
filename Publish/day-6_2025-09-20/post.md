---
title: "狀態機除錯（90% AI）"
date: 2025-09-20
category: ironman-2025
slug: post-2025_09_20-day6-狀態機除錯90-ai
day: 6
---

# Day6 - 狀態機除錯（90% AI）


昨天我們分享了遊戲中玩家角色的組裝方式，今天就講一些測試手段和運做起來的樣子。

我把需要的組件都掛到一個小方塊上，包括調用 StateMachine Tick 的 Driver、組裝測試用角色的 Agent Driver、讀取玩家輸入資訊的 Input Source Bootstrap，除錯用的 Event Sink、執行移動的行為的 RigidbodyMover 插件。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-6_2025-09-20/images/image_4.png)

還有一個讀取除錯資訊並顯示在畫面上的 GUI Debug View，這下就有了一個可以移動、衝刺和攻擊的小方塊，並且能用 DebugView 看到狀態機的運作資訊。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-6_2025-09-20/images/image_2.png)

我也有讓 GPT 寫一些單元測試，主要是針對 Builder 跟轉換條件的測試。原本還有針對 State 和 StateMachine 本體運作的測試，但後來改進架弄壞就懶得再修了。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-6_2025-09-20/images/image_3.png)

而等更後面串接更完整人物控制時，我發現 GUI 不好閱讀，所以改用 Editor window 重作了除錯視窗，能顯示更完整的除錯資訊，包括狀態資訊、轉換資訊、條件的判斷狀態等等。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-6_2025-09-20/images/image_1.gif)

特別做這個 Editor window （當然也是 AI 做的）是因為我花了半天找一個手動測試時遇到的不存在的 bug，原本以為是轉換判定有誤、Builder 沒組裝正確或狀態機流程有問題。

但單元測試全綠燈， 還仔細 Re 過幾次，檢查是不是 GPT 測試覆蓋不完全，還是有哪裡寫錯。

結果都沒錯，最後發現是「我寫的」手動測試的腳本有問題，組裝狀態機時不小心多設一條比較寬鬆的條件沒注意到==

誰說 AI 是屎山機器？我才是那個屎山機器，讓 GPT 給我做了除錯工具後找 Bug 輕鬆多了。

老實說，這是我第一次建這種複雜的狀態機，不然以前為了省事都是用 Enum Switch 方案搞定一切 www