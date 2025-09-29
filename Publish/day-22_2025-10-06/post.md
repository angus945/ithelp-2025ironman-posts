---
title: "重構輸入方案（80% AI）"
date: 2025-10-06
category: ironman-2025
slug: post-2025_10_06-day22-重構輸入方案80-ai
day: 22
---

# Day 22 - 重構輸入方案（80% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

這篇就開始重構，從最初的 Input 系統開始。

![https___ugc-media.4gamers.com.tw_puku-prod-zh_anonymous-story_8ca9b29f-9244-4618-b20d-7a65d9d1e568.jpg](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_1.jpg)

但當然不是真的從頭，其實原本 GPT 生出的輸入系統架構就不錯了，只是沒有做領域分層而已 。

所以我直接把整個 Input 相關腳本給 GPT，要他提供 DDD 該有的資料夾結構。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_2.png)

在一個 Input 資料夾下分成四層，Domain, Application, Infrastructure, Presentation。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_3.png)

Domain 是最基底的資料結構，包括按鈕狀態、輸入狀態等，Application 是一些資料轉接以及抽象的接口定義。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_4.png)

Infrastructure 則是輸入系統與 Unity 對接的部分，例如 Camera, 場景的 Bootstrap, DI 初始化還有各種輸入方案的實施，Legacy Input, New Input System 等等。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_5.png)

至於 Presentation 就是除錯用的面板而已，稍微修正了面板原本對 Infrastructure 資訊的直接依賴。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_6.png)

原本 Input 就幾乎都是 GPT 做的了，所以架構沒啥問題，這次主要是把腳本轉移到正確的層級而已，然後用 Assembly Definition 管理各層的依賴，以及讓 Domain, Application 層級與 Unity 隔離。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_7.png)

不過我其實有個疑惑，輸入系統本身應該是 Presentation 相關的，但輸入系統中的實施應該放在 Infrastructure 還是 Presentation 比較好？

問了一下，GPT 說是 Infrastructure ，那就繼續維持在 Infrastructure 吧 : )

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-22_2025-10-06/images/image_8.png)