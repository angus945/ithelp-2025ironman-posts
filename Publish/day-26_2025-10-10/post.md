---
title: "資產載入器（90% AI）"
date: 2025-10-10
category: ironman-2025
slug: post-2025_10_10-day26-資產載入器90-ai
day: 26
---

# Day 26 - 資產載入器（90% AI）


開頭提醒，從 Day21 開始我開始接觸很多超過能力邊界的知識，後續內容紀錄的是我在當下的理解，所以內容可能有大量誤解或錯誤。

上篇重構了視覺容器，但有容器也還無法顯示 Character，需要有真正的視覺物件實例。

因為我們要使用 Unity Aimator 當做動畫方案，所以會用 Prefab 做好不同角色、敵人的視覺物件，遊戲物件生成時也連帶用 Instantiate 生成需要的視覺。

我把以前的 AssetLoader 框架給 Claude code CLI 看，要他重構成核心的 Core 層與針對 Unity 實現的 Unity 層，當做未來可以重用的模組。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-26_2025-10-10/images/image_2.png)

核心接口把載入過程分成多個階段，資產來源提供、資產解碼器、資產快取跟 Loader 本體接口。Unity 的部分實現了最簡單的 Resources 載入（引擎自動解碼），以及自由度較高的 StreamingAsset 載入（字定義 Byte 解碼）

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-26_2025-10-10/images/image_3.png)

但專案部分為了省事先用 Resources 當載入方案，未來要替換都行，反正接口都一樣。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-26_2025-10-10/images/image_4.png)

專案建立一個自己的 IAssetService 用來與專案的需求對接，內部則是調用 AssetLoader 模組提供的現成載入方案。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-26_2025-10-10/images/image_5.png)

還有進行全域 DI 註冊，提供一個靜態的 Installer 讓遊戲的 GameCompositionRoot 在初始化階段安裝到全域系統中。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-26_2025-10-10/images/image_6.png)

Character 的 Presentation 會在初始化時透過（自動注入的） IAsserService 生成自己的視覺實例，然後附加到視覺容器底下。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-26_2025-10-10/images/image_7.png)

好像沒什麼必要，但還是加一張視覺實例被生成的畫面。

![STUST_Project_4-1 - SceneRenderTest - Windows, Mac, Linux - Unity 6.2 (6000.2.0f1) _DX12_ 2025-09-19 09-09-44_0 (1).gif](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-26_2025-10-10/images/image_1.gif)