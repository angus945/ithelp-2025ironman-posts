---
title: "帳簿系統 （90% AI）"
date: 2025-09-22
category: ironman-2025
slug: post-2025_09_22-day8-帳簿系統-90-ai
day: 8
---

# Day8 - 帳簿系統 （90% AI）


就是血量、屬性、資源或其他啥的數值管理系統，跟 GPT 討論後決定做一個更通用的「數值帳簿」，裡面只做最基礎的加減紀錄，具體用途交給每個專案自己決定。

這個其實討論蠻長的，好像捨棄了四五次討論後開始上軌道吧，也沒留到對話紀錄 DDD:

系統的核心就是負責管理單一數值資源的 Account ，以及負責管理多個 Account 的 Ledger 。裡面有註冊參數、設置範圍和修改數值的功能。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-8_2025-09-22/images/image_5.png)

也有事件監聽功能，可以訂閱某個 Accout 內容發生變化時發佈廣播。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-8_2025-09-22/images/image_1.png)

一樣讓 GPT 補了除錯面板，可以看到看到註冊的 Account 內容，還有監聽中的事件。（我都不知道可以用 [CallerMemberName] 追蹤函式的調用者）

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-8_2025-09-22/images/image_2.png)

單元測試，就是一些基本操作，註冊、設置範圍、修改數值，批次操作和事件監聽的測試。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-8_2025-09-22/images/image_3.png)

然後是跟使用這套帳簿系統實做的狀態參數 Stats 系統，但因為企劃部分還沒設計完整，所以就先加個血量意思意思。後續要補上金錢、魔力或啥的都很簡單，多註冊一個就好。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-8_2025-09-22/images/image_4.png)

不過…

後來正式串接角色的各種 Stats 發現這套帳簿系統有不少問題，所以又被我砍了，重做了另一套，具體內容就等後續的篇章再分享吧 :P