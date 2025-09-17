---
title: "背包和武器（< 5% AI）"
date: 2025-09-24
category: ironman-2025
slug: post-2025_09_24-day10-背包和武器-5-ai
day: 10
---

# Day10 - 背包和武器（< 5% AI）


背包系統，或稱庫存系統，讓玩家能把某些物件撿起來保存和使用。

剛開始有用 AI ，但後來發現遊戲好像不用太複雜的背包系統，所以還是自己寫了個簡化的。就是一個很簡單的背包，能撿起所有實做 IPickable 的物體，然後切換當前選取的欄位。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-10_2025-09-24/images/image_7.png)

掛一個撿物件的 Addon 給狀態機，當 IntentPick = true 時，進行簡單的 physics overlap 檢查週圍有沒有可以檢的物件，有的話就撿起來放進背包。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-10_2025-09-24/images/image_3.png)

對，就是這麼簡單的背包，如果後續需求變複雜再重作吧 :P

然後是關鍵的武器，因為涉及很多整合工作，所以也是自己寫。

原本要寫新的武器腳本，但想一下發現能直接沿用狀態機框架，給武器閒置、飛行、撿起、卡住、揮動跟拿著的狀態，透過狀態機管理武器的行為。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-10_2025-09-24/images/image_4.png)

用幾個 Addon 處理武器的特殊行為，例如投擲時忽略投擲者的碰撞、飛行時改變視覺顯示方式（武器也有 VisualContainer）以及在被撿起來時觸發視覺容器的串接效果。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-10_2025-09-24/images/image_5.png)

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-10_2025-09-24/images/image_2.png)

最後整合玩家行為狀態機，加上撿武器跟投擲的狀態，然後呼叫背包把中有 IPickable 的武器丟出去。IPickable 的道具可以自己實作被撿起、丟、使用時的行為。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-10_2025-09-24/images/image_6.png)

武器撞到有 IStuckable 的目標會卡在對方身上，如果玩家這時去撿武器，就會連敵人一起拿起來。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-10_2025-09-24/images/image_1.gif)

做這類整合工作的速度就降低很多，畢竟是自己進行的，沒辦法像 AI 一分鐘幾百行。

但也是必要的，可能是需求更加客製化、系統交互更複雜了，把所有前提資訊跟 AI 說清楚可能導致 Context 過長爆走，但不說清楚 AI 又沒辦法正確整合，所以自己來還是比較穩妥。