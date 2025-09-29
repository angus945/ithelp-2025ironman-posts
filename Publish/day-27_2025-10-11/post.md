---
title: "戰鬥系統框架（80% AI）"
date: 2025-10-11
category: ironman-2025
slug: post-2025_10_11-day27-戰鬥系統框架80-ai
day: 27
---

# Day 27  - 戰鬥系統框架（80% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

戰鬥相關的系統，也是原型中比較混亂的部分，傷害、血量什麼的很零碎，而且敵我辨識方案也是先應急寫的，這次重構也要完全打掉重來。

我先給 GPT 舊腳本，要他提出架構範例，然後要他把某個些地方修正成比較貼近我想法的方案，最後再轉存成一份 md 文件。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_1.png)

我把文件給 Claude 閱讀，要他計畫一下怎麼重構成可重用模組，我沒特別要求，但 claude 讀了我的模組化資料夾，主動參考相似的格式做計畫。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_2.png)

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_3.png)

後續的對話我找不到去哪了==

沒記錯的話，當時就是先讓 claude 寫了這個戰鬥框架，但還是太 Overdesign，所以我又重新簡化過一次。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_4.png)

抽象接口的 ICombatEntity 代表所有能參與戰鬥的實體，裡面帶有陣營辨識符 IFactionIdentifier 和戰鬥用的屬性參數 ICombatStats 。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_5.png)

ITargetingFilter 作為戰鬥目標的過濾器，根據自身與目標的資訊，判斷是不是一個合法的但鬥行為的指定對象。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_6.png)

ICombatOperation 和 Data 用來定義一個戰鬥的行為和輸入參數。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_7.png)

戰鬥需要的資訊會透過一個 Context 傳遞，帶有一個 <T> 為戰鬥的參數輸入。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_8.png)

戰鬥行為則透過 CombatService 和 TargetingService 進行，透過泛型 <T> 指定要進行的戰鬥行為或目標過慮方式。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_9.png)

上面就是一個不涉及任何任何實作的戰鬥框架，具體戰鬥行為會再根據專案需求實作。例如定義一個造成傷害的戰鬥行為，Data 需要指定傷害量，戰鬥行為就會從目標身上扣除指定血量。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_10.png)

一個簡單的碰撞傷害器，如果 Collision 目標為 ICombatEntity，就在確認目標合法後造成指定傷害。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_11.png)

提供一個 Controller 當外部的操作入口，初始化需要注入一個 ICobmatStats，作為戰鬥實體的屬性參數來源。（但 Controller 內容還沒實作完）

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_12.png)

Character Infrastructure 初始化時會透過一個 Adapter 把通用的 Stats 轉接成 ICombatStats 讓戰鬥系統使用。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_13.png)

Stats  原本 Day8 有做過，是用一個通用帳簿系統 Ledger 管理的，但後來使用發現有點 OverDesign 了，所以做了簡化和重新命名，StatsController 就是 Stats 的操作入口。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-27_2025-10-11/images/image_14.png)

總之，這個戰鬥的框架不在乎 stats 的來源，也不定死能進行的戰鬥行為和敵我辨識方案，全看專案怎麼實施。