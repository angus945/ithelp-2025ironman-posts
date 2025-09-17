---
title: "技能系統框架（80% AI）"
date: 2025-09-26
category: ironman-2025
slug: post-2025_09_26-day12-技能系統框架80-ai
day: 12
---

# Day12 - 技能系統框架（80% AI）


今天講遊戲最核心的部分之二，也是繼狀態機之後第二大的框架？

玩家串起敵人的玩法除了視覺和數值效果外，還能使用敵人的能力（類似卡比之星那樣），所以我需要一套能在敵人、武器之間通用的技能系統。

總之先大概描述需求，然後把專案結構給 GPT 看，要他提出幾種方案，再針對比較符合的方案要求進一步解說和案例。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_9.png)

技能系統我做了三版，第一版是依據 GPT 給的方案 D 實作，但複製到專案中發現整合不了，因為跟需求有些偏差，它提的插槽概念比較像多個 Modifier ，能對技能添加額外效果。

但我只需要「整個」技能能被武器拿去用。

所以我寫了一些比較貼近預期的 interface 架構給 GPT，要他修正設計方向，然後就有了第二版。

第二版就符合需求了，貼到專案中就能實作出需要的功能，也成功實現了測試用的效果。但要整合的時候發現 OverDesign 蠻嚴重，框架到實作之間多了一層沒必要的泛型轉換。

所以我開始砍，再把簡化後的架構丟給 GPT，要他接續完成。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_1.png)

於是就有第三版的技能框架了，也是最後採用的方案。（前兩版的對話都刪了，只有一開始就截到的圖能用 QQ）

首先是技能的基本定義跟基本參數，用來讓使用者定義不同技能。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_2.png)

SkillBase 是技能效果的基底，<TDef> 代表這個技能要使用的定義類別，繼承一個 ISkillCore 作為使用接口，隱藏泛型。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_3.png)

ISkillContext 用來傳遞施放技能需要的參數、環境資訊或是工廠，例如包括施放者，施放目標位置、具體的施放目標，屬性修改器，還有針對每個專案實作註冊的施放資源跟補充資料。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_4.png)

最後是一個負責管理的 SkillHost，每個能使用技能的實例都有獨立的 Host，裡面會儲存他能用的各種 Skill 以及動態 （IDebugInfo 是方便除錯用的）

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_5.png)

施放流程會先檢查技能存不存在、是不是在冷卻，然後觸發技能的目標選擇器，最後讓技能自己檢查當前狀況符不符合發動條件

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_6.png)

用法像這樣，建立一個 Host 之後，傳入專案需要的 Context ，用工廠建立技能實例，把技能添加到 Host 中，Host 會回傳一個 id ，後面就可以透過這個 id 施放技能。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_7.png)

還有單元測試，用一系列 Dump 系統檢查框架的基本功能。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-12_2025-09-26/images/image_8.png)

框架大概像這樣，明天的文會再進行整合~