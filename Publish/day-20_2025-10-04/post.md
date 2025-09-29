---
title: "測試競技場（ 5% AI）"
date: 2025-10-04
category: ironman-2025
slug: post-2025_10_04-day20-測試競技場-5-ai
day: 20
---

# Day 20 - 測試競技場（< 5% AI）


為了測試遊戲的核心玩法循環，我也弄了簡單的競技場，會不斷生成新的敵人在場上給玩家打，直到玩家血量歸零。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-20_2025-10-04/images/image_1.png)

然後…各種新 bug 都跑出來了，主要問題都出在我跟 Untiy 的整合的部分，例如碰撞。

我原本使用 Physics Ignore Collision 避免捉捕&串接敵人機制會發生的自我碰撞，但一些子父層級的轉移導致忽略碰撞的集合產生奇怪的結果（就是忽略了不該忽略的目標的意思）。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-20_2025-10-04/images/image_2.png)

也沒特別修，就先用一個除錯按鈕應急，還加了其他嚴重 bug 的修復按鈕，像是玩家把自己撿起來，武器、敵人穿出競技場之類的。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-20_2025-10-04/images/image_3.png)

不修主要是維護性問題，其實整合部份程式的屎山已經開始堆積了。

在中間點那篇有提到，我的程式目前沒特別架構，只有分成 AI 寫的可重用模組框架，還有我針對專案進行的實作和整合。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-20_2025-10-04/images/image_4.png)

AI 的部分沒啥問題，畢竟每個系統都是獨立的，模組間也不互相依賴。

但我的整合就沒那麼嚴謹了，所以不同系統、系統跟視覺之間有蠻多職責混雜的部分，那些碰撞問題我一時也想不到怎麼修。

果然我才是那個造屎機器 (´・ω・`)

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-20_2025-10-04/images/image_5.png)

至少一審需要的 Demo 已經有了，也初步測試和修正完玩法問題，接下來重構一下整合腳本就好。

天啊這篇才 Day20 ，還有十篇要寫。

雖然平常日誌是月更，但也是整個月陸續寫才到最後發，每天都要一篇完整的也太難（雖然是先備稿發的）。

加上專案本身也是走一步算一步，所以這系列也很沒架構，就是我做啥就寫啥，跟巴哈的日誌一樣。

接下來應該不會有什麼新功能出現，就是寫我學 DDD 和重構的過程而已，想辦法塞滿剩下的十篇。

還有我不想做簡報，雖然發這篇的時候已經專題一審完了

但我不想做簡報 ))))):