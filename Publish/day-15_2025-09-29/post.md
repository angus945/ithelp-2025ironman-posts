---
title: "整合讓武器串起敵人（< 1% AI）"
date: 2025-09-29
category: ironman-2025
slug: post-2025_09_29-day15-整合讓武器串起敵人-1-ai
day: 15
---

# Day15 整合讓武器串起敵人（< 1% AI）


最後，也是最重要的，讓玩家把敵人串起來。原本是打算讓武器複製敵人的技能，還有建立一個視覺副本，但實際整合的時候發現最好的做法其實是「整碗端去」。

就是直接把整個敵人物件轉移到武器底下的意思。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-15_2025-09-29/images/image_4.png)

雖然機制還沒設計完整，但在預期構想中，被串上武器的敵人實際上還是「活著」的，除了會在玩家揮動時發動技能效果、會在武器上講一些垃圾話，還可能在某個時機被噴飛回場地中。

整個敵人捕捉的好處就是，我不用特別寫複製品的程式，敵人的行為接口都是能直接調用的，播放動畫、技能、甚至後面的講話功能。

那敵人原本的行為怎麼辦？我讓目標繼承一個 ICapturable 介面，實作被捕捉時的反應，直接把碰撞箱、物理和狀態機關閉就好了。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-15_2025-09-29/images/image_2.png)

而且，敵人被捕捉當下的動態參數也會被沿用，例如技能冷卻、施放次數之類的，如果玩家把怪物的技能次數用完，那怪物被噴回場地後也放不了技能。

至於捕捉功能就用一個管理系統，在玩家撿起卡住的武器時調用，就會把整個敵人搬起來。觸發介面的 OnCaptured，然後調用前面視覺容器寫過的功能，把敵人轉移到武器底下，並縮小顯示夾角。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-15_2025-09-29/images/image_3.png)

嗒啦，吃毒的遊戲核心架構就有了，可以看到每多黏一個敵人，玩家揮砍時射出的子彈就多一顆，每顆都是不同敵人各自技能發射的。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-15_2025-09-29/images/image_1.gif)

而且所有行為都是雙向兼容，玩家跟敵人的的運作方式是相同的。

我是說，完全相同。

意思是，如果玩家被武器丟到，敵人也能把玩家撿起來  (ﾟ∀。)