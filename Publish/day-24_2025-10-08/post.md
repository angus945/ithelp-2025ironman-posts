---
title: "重構背包系統（30% AI）"
date: 2025-10-08
category: ironman-2025
slug: post-2025_10_08-day24-重構背包系統30-ai
day: 24
---

# Day 24 - 重構背包系統（30% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

背包系統，當下紀錄的不夠，寫的時候有點忘了，我記得好像是自己稍微重寫之後，再要 Claude Code （對我也訂閱了 Claude Code）直接幫我改成 DDD 架構，然後背包相關操作用 Usecase 的方時實作。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-24_2025-10-08/images/image_1.png)

因為原本背包就不是很大的系統了，所以整個重寫也不會怎樣（反正也不用自己寫）

Domain 層包括背包的本體相關 Entity, Event, 背包道具的介面等等。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-24_2025-10-08/images/image_2.png)

介面定義了道具 Item 能執行的各種動作，包括撿起、丟棄、投擲、使用或召回。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-24_2025-10-08/images/image_3.png)

Application 則針對各種背包操作實作 UseCase，包括前面提到的撿丟使用，還有切換背包欄位等。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-24_2025-10-08/images/image_4.png)

infrastructure 就是實施…一些東西，事件、過濾器、道具儲存方案等等，然後提供一個 InventoryController 當做外部操作的進入點。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-24_2025-10-08/images/image_5.png)

因為背包系統還不複雜，所以只有整個系統用一個 Assembly Definition 檔著，就沒讓四層各自建立了。

Presentation 還沒實作，只有先讓 Claude 寫了簡單的 CustomInspector 顯示背包內容方便看效果 :P

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-24_2025-10-08/images/image_6.png)