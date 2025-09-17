---
title: "中間點"
date: 2025-09-30
category: ironman-2025
slug: post-2025_09_30-day16-中間點
day: 16
---

# Day16 - 中間點


今天是第 16 天，剛好是活動文章的中間點，目前為止的部份都是在暑假末尾製作的，大概花了三週（8/14 ~ 9/4），而在備稿的當下，大四新學期的第一週 （9/8）也開始了，再幾週後就要繳交畢專一審資料，時間過的飛快啊。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-16_2025-09-30/images/image_6.png)

三週的時間應該不算長，原本在這種時間壓力下可能只做的出拋棄式的屎山，就是 GameJame 會寫的那種，但這次不是拋棄式的程式，而是一開始就有照顧維護性、擴展性的架構。

目前我把把程式分成兩大部份，一部分是相互獨立的可重用框架，另一部分則是針對專案需求的實作與整合。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-16_2025-09-30/images/image_1.png)

可重用框架包括狀態機、回饋、帳簿與技能系統。名稱後綴 .Core 代表純 C# 的核心程式碼，.Unity 代表有對 Unity 的依賴，.Test 代表單元測試，其他名稱 (MMFeelFeedback) 代表對某些外部模組或插件的依賴。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-16_2025-09-30/images/image_2.png)

可重用框架的重點是框架本身，用一系列抽象接口定義系統架構，但不提供「具體」實作，尤其是 Core。

可能會補充一些常用或好用的方案（像 Feel 插件的串接），但最重要的是，無論這裡怎麼提供方案，每個專案都可以替換或實作自己需要的方案，框架只是指引而非限制。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-16_2025-09-30/images/image_3.png)

目前為止， AI 程式碼與手工程式碼大約各占 50%，AI 主要負責各種相互獨立的模組系統「框架」，自己則是針對遊戲需求進行實做與各系統的整合，不同項目標註的比例也能反映出這點。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-16_2025-09-30/images/image_4.png)

左半部更加單元化、模組化的工作可以讓 AI 表現的很精準，因為目標跟解決方案都很明確，需要的前提資訊不複雜，失敗重來的成本也更低。

右半整合工作因為是專案的課製化需求，並且涉及多個系統的交互，光是把必要資訊告訴 AI 之後 Context 就會到達不穩定的長度了，所以還是自己來比較可靠。（至少我目前是這樣，之後更熟說不定能找到方式克服）

專案的程式沒什麼特別架構，因為...嗯…一方面是能力問題，目前正在學習 DDD 或 Clean Code ，但了解程度還不夠。另一方面則是需求，因為目前的遊戲設計並不完整，我只是先做出目前方向確定的部分而已。

我們現在甚至連一份文件都還沒寫，只有 Mrio 上的討論紀錄而已，專案管理也是超簡陋的 Excel 表隨便列。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-16_2025-09-30/images/image_5.png)

啊企劃是誰，怎麼該做的沒做好

哈哈也是我啦 (´・ω・`)

雖然文書工作分攤給組員了，但一些企劃、遊戲設計還是得我來做，有些設計也還要試玩才知道好不好。

所以在設計方向不確定的情況我也不敢架構主程式，至少 AI 的部分沒什麼問題，現有的屎山都是自己拉的，等方向穩定之後還得大重構一次。

至於接下來的目標，就是先繼續做確定的部分，然後用臨時腳本做出一審的可玩原型，確認戰鬥的核心機制是好玩的。

然後想辦法寫到到三十篇文www