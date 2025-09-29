---
title: "武器投擲重構（10% AI）"
date: 2025-10-13
category: ironman-2025
slug: post-2025_10_13-day29-武器投擲重構10-ai
day: 29
---

# Day 29 - 武器投擲重構（10% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

武器投擲，昨天已經做完了射彈系統，現在只要把武器投擲的東做跟射彈串接上就好。

初步的做法先省略，因為後面改掉了，總之我遇到的第一個問題是武器投擲時，生成的射彈會直接跟玩家（發射者）碰撞。

所以我先 commit 一版，然後要 Claude Code 給我解決方案看看。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_2.png)

因為武器投擲涉及四個系統，Character > Inventory > Weapon > Projectile，解決方法會有點麻煩，所以我也把關聯系統告訴 Claude Code，要他去看看整體架構。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_3.png)

雖然 Claude 是修好了，但我覺得它的方案不夠理想，他直接把 Inventory Domain 的 IThrowable 加上一個 Collider 資訊的輸入。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_4.png)

但在 DDD 中，Domain 層不應該有 Unity 的參考，所以我要 Claude 再再改方法，用另一個 Context 的 Interface 攜帶資訊。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_5.png)

但但但再修改的方案還是不理想，她用一個 context 把 collider 透過 object 傳遞給武器，再讓武器傳遞給射彈。

在 DDD 中的 Unity 參考傳遞問題蠻麻煩的，因為不同領域邊界 Bounded Context 之間要透過 Infrastructure 層訪問目標 BC 的 Application 層，但 Application 也是無 Unity 的，所以 interface 接口不能輸入或輸出 Unity 參考。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_6.png)

給 Claude 重構的過程我也同時問了 ChatGPT 一些問題，在一長串對話後我得到一種折衷？的思路，透過泛型定義一個 Context 資訊接口。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_7.png)

如果用泛型的話，就能在 Application 層不定死，但在 Infrastructure 指定 Unity 型別。這樣在 Character Infrastructure （武器投擲者）初始化時，就能把 Collider 資訊註冊給 Inventory。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_8.png)

而道具投擲或其他行為的接口，就能傳遞整個 Context，讓實做方取得自己需要的資訊，像是這裡的 Collider 參考。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_9.png)

至於 Projectile 部分就先用了簡單暴力的方式傳遞跟設置 ignore 之後再想。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_10.png)

武器投擲的視覺效果則是透過領域事件發佈，讓 WeaponView 監聽事件，並執行視覺效果，設置 Billboard 的顯示模式，或是讓武器旋轉。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_11.png)

投擲示意圖，參數什麼都還沒調就是了，所以動作看起來怪怪的，但運作邏輯是正確的。

![STUST_Project_4-1 - WeaponTest - Windows, Mac, Linux - Unity 6.2 (6000.2.0f1) _DX12_ 2025-09-22 14-01-46_0.gif](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-29_2025-10-13/images/image_1.gif)