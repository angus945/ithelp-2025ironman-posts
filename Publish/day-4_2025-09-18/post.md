---
title: "狀態機框架（80% AI）"
date: 2025-09-18
category: ironman-2025
slug: post-2025_09_18-day4-狀態機框架80-ai
day: 4
---

# Day4 - 狀態機框架（80% AI）


狀態機 StateMachine ，各種遊戲都會使用的模式，做法的網路上教學也有千萬種，用途包括但不限於遊戲 AI、人物控制、物體行為等。

而作為一個 2.5D 的戰鬥和動作遊戲我們當然也有，而且也是目前遊戲中最大的系統，但因為沒留到對話紀錄，所以只有之前截過的圖片。

其實剛開始是想直接做 PlayerController ，所以我把前面的 Input 腳本丟給 GPT，要他給我一些實現方案，目標是邪教羊《Cult of the Lamb》的操作手感。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_1.png)

但跟 GPT 討論之後發現需求並沒那麼單純，因瑋我想讓系統易於維護和擴展，所以目標直接轉變成一套狀態機框架，而 GPT 也因為 Context 汙染而開始爆走。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_14.png)

所以我把過程的腳本重新整理後，開新對話再讓 GPT 生成。重來一次後方向就穩定多了，目標也更明確，接著就開始擴大到把預期功能完成，目標是一個易於擴展與組裝的狀態機架構！

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_3.png)

首先是狀態的基底類別 StateBase，裡面包括可以被覆寫的 OnInitial, OnEnter, OnTick, OnExit 和 OnAlwaysTick ，後續所有狀態的實作都會繼承它。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_6.png)

註：OnTick 是只有當前 State 是自己時觸發，OnAlwaysTick 則是無論如何都會觸發。

StateBase 還實做了一個 IStateStatus 作為抽象的保護層，用來給系統的其他部分取得狀態資訊，裡面會提供自己的辨識名稱、持續時間、Tick 次數跟執行進度（如果進度是可預期的）。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_7.png)

接著是狀態間的轉換條件 ITransitionCondition，用來實作狀態間的切換邏輯，回傳 true 代表條件通過。一個 Transition 可以有多個條件，例如 StateA to StateB 可以要求 ConditionA, B, C 全通過才轉換。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_8.png)

狀態的外掛插件 IStateAddon，它不會進入狀態的 State Graph，而是用掛載的方式運行。觸發時機有很多種，可以自行選用需要的介面實作，維持介面隔離 Interface Segregation。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_9.png)

狀態機的內部溝通資訊 IStateContext ，用來給狀態、條件和插件做內部溝通，包括靜態的 Config 與動態的 Runtime 參數，還有狀態機的運作的時間資訊。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_10.png)

然後狀態機的內部「不進行任何事件廣播」，都是通過 Context 中的動態參數傳遞，Transition 條件也完全依靠動態參數判斷，跟 Unity Animator 一樣。

（暑假聽九日的 TGDF 演講也說是依靠動態參數判斷，事件在狀態機中真的太難除錯）

最後是 StateMachine 的聚合點，外部使用者提供的公開建構子、初始化、開始運作以、更新用的 Tick、Context 接口和還有除錯用的快照資訊。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_11.png)

每個狀態機的 Tick 更新流程如下：外掛插件的 BeforeTick 更新 > 當前狀態的 Tick > 所有狀態的 Always Tick > 外掛插件的 AfterTick > 檢查轉換 > 轉換流程 > 紀錄除錯快照。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_12.png)

當 Tick 的 Transition 檢查動態參數符合條件時就會進入接換流程：當前狀態的 OnExit 觸發 > Addon 的 OnExit 觸發 > 切換當前狀態 > Addon OnTransition > 當前狀態的 OnEnter > Addon 的 OnEnter。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_13.png)

這裡的 events 是廣播給狀態機外部的，組裝時可以傳入一個事件匯流排，看使用者需求實作。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_4.png)

至於組裝的部分則是透過一系列 Builder ，將狀態機的各種「零件」輸入進去，就能傳出一個組裝好的狀態機。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_5.png)

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-4_2025-09-18/images/image_2.png)

這篇是狀態機的核心架構，一套可以重用在任何專案的純 C# 模組 Package，下一篇則會介紹專案中透過這個框架實作的玩家行為和動作。