---
title: "重構狀態機（30% AI）"
date: 2025-10-07
category: ironman-2025
slug: post-2025_10_07-day23-重構狀態機30-ai
day: 23
---

# Day 23 - 重構狀態機（30% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

再來是狀態機重構，但不是先前讓 GPT 寫的模組化框架，而是我對遊戲進行的實施，就是角色相關的狀態實作要重構。

一樣先打包給 GPT 看，要他提供建議。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_1.png)

是基於 DDD 的原則，我的狀態機實施不應該直接依賴「第三方」模組（雖然也是我的模組），所以後面的對話中 GPT 提供了多一層 Application 包裝的方案。

但這樣本末倒置了，原本那個狀態機框架就是要直接用的，其實就跟 Domain, Application 層級用途相同，沒必要再多包一層。

所以我把框架也給 GPT 看，他就修正建議，讓專案的實施直接跟狀態機框架對接。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_2.png)

然後就是重構，一樣建立四層結構，Domain, Application, infrastructure, Presentation，這次改名叫 Character。

Domain 中就是狀態的基礎定義，包括狀態本體、轉換條件、配置參數和動態參數。然後把裡面對 Untiy Component 或變數的依賴排除掉。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_3.png)

原本的 Addon 機制改放到 Application 層級，當做狀態機與外部世界的轉接，包括實際執行移動、攻擊、將輸入與 AI 資訊傳入狀態機，以及視覺相關處理。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_4.png)

但 Application 仍然不應該直接依賴外部解決方案，所以裡面也定義了轉接用的抽象 Ports，包括執行移動的接口、取得 Input 資訊的接口等等。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_5.png)

直到 Infrastructure 層才有對 Unity 功能的實施與對遊戲中其他系統的依賴，還有工廠、組裝規格實施方案，最後提供一個讓外部訪問的 Controller。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_6.png)

目前新的 Controller 就是組裝角色而已，先呼叫依賴注入，然後初始化相關的 Infrastructure 與 Presentation，最後組裝狀態機。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_7.png)

Infrastructure 會負責註冊 Addon 需要的各種 Port ，例如對 Rigidbody 轉接的 IMovementPort 或是其他遊戲系統的轉接和初始化。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_8.png)

Presentation 也類是，只是負責註冊跟視覺相關的 Port。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_9.png)

當工廠要組裝 Addon 時就會建立需要的 Port 注入，我先用比較暴力的方式寫 Addon 與 Port 的對應，之後可能要搞個自動檢測比較好。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_10.png)

這部份的重構也沒什麼破壞性，大部分的舊實施直接轉移到對應層級就好了，只是要把一些直接依賴改成抽象接口，等後續補上其他系統就能恢復功能了。

原本的除錯視窗也能直接沿用，我還要 AI 多補了一個顯示有哪些 Addon （和註冊內容）的欄位。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-23_2025-10-07/images/image_11.png)