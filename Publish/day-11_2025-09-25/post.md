---
title: "自動載入和注入（95% AI）"
date: 2025-09-25
category: ironman-2025
slug: post-2025_09_25-day11-自動載入和注入95-ai
day: 11
---

# Day11 - 自動載入和注入（95% AI）


遊戲有時會需要一個全域共用的系統，像輸入檢測、音效播放或 GameManager 等等，而其中又有部分需要場景實例才能運作，剛開始學到的方法就是 Prefab + Don't Destroy on Load + Singleton 吧，但以現在的程度已經~~看不上~~不適合這種方案了。

我比較喜歡用多場景管理共用系統，測試時只要記得把一個初始化系統的場景拉進 Hierarchy 就好，這樣我在很多痾…手動的單元測試？場景就能共用這些系統。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_10.png)

但要自己拉場景還是好麻煩==

所以也讓 GPT 給我搞了自動場景載入，用 [RuntimeInitializeOnLoadMethod] 在初始化階段觸發 static 函式，抓資料夾中的配置 ScriptableObject，然後用 Additive 模式載入要求的場景。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_2.png)

這樣就算我直接進 Play Mode，系統也會自動載入我要求的場景。一個簡單的 QOL 系統，GPT 幾分鐘就生好了，但我還是多花了一些時間修重複載入或啥的 bug。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_3.png)

接著是 DI 半自動注入。

從大量用 Interface 抽象化和依賴注入後，我就在想要不要學 Zenject 之類的自動注入框架，不然每次手動注入也是真的麻煩。

不過 Zenject 是一個蠻大的系統，雖然功能很完善但相對要學的東西就更多。

現階段好像也沒必要到一定要學？

所以我轉念一想，反正需求也還不複雜，不如讓 GPT 給我個簡單的方案試水溫。總之先要求了幾種方案，然後指定我要的方向深入解釋。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_4.png)

剛開始的方案有嚴重過度設計，所以也要他簡化。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_5.png)

但 DI 自動注入是在目前能力邊界之外的知識 ，所以我追問了一些問題，然後要 GPT 給我解釋完整的自動注入流程。總之就是透過反射查找帶有 [Inject] Attribute 的變數，然後讓某個注入器傳入參考。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_6.png)

看完解釋思路就清楚多了，也知道怎麼使用這個簡易注入器。（對，原本是在連用都不會的知識邊界外）

最終用法很簡化，首先在系統初始化把全域的服務註冊進一個 DI 容器，像是各種 Factory, Feedback 或 InputSystem。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_7.png)

然後物件初始化時，把要注入的物件跟 DI 容器傳入注入器，反射會自動抓有 [Inject] 的欄位，根據先前註冊的 Interface 傳入實例，達成自動註冊。（也有針對 GameObject 實做一個注入所有子物件 Component 的腳本）

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_8.png)

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_1.png)

也可以直接繼承一個自動注入 MonoBehavior，他會在基底 Start 自動注入，子類可以繼承 override  然後調用 base.Start()。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-11_2025-09-25/images/image_9.png)

雖然這樣好像跟手動調用 Inject 沒區別就是了==

至於為什麼不是在 Awake 注入？

因為場景載入時機的問題，雖然最上面搞了一個編輯器模式下的自動場景載入，但額外載入的場景「無論如何」都會比預設的 Active Scene 還晚初始化。

所以進入 Play mode 的當下，測試場景的物件會比自動載入的初始化場景早 Awake …

這在有正常遊戲流程的情況下不會發生，但我不想老早處理整個流程，所以乾脆維持在 Start 注入。

也有嘗試修過，但找到的方案反而都會失去自動載入的便利性，像是整個 Hierarchy 被摺疊起來之類的 ) :

所以算了，反正夠用 :P