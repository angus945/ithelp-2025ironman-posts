---
title: "串接數值計算（ 10% AI）"
date: 2025-10-02
category: ironman-2025
slug: post-2025_10_02-day18-串接數值計算-10-ai
day: 18
---

# Day 18 - 串接數值計算（< 10% AI）


上篇用 AI 做了一個數值計算方案，今天要來串接進遊戲需要計算的部分。在「當前」的設計中，需要計算的大概有這些項目：

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_1.png)

敵人的捕捉阻擋值，代表敵人有多難被玩家串起來，數值是血量百分比。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_2.png)

捕捉判斷，判斷玩家能不能把敵人串到武器上，判斷條件是武器的捕捉力量是否大於目標阻擋值。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_3.png)

攻擊力提供計算，根據被串敵人提供的基礎值 * 血量百分比 * 曲線，代表玩家串起的敵人可以提供多少額外攻擊力。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_4.png)

抵抗值，代表被串起來的敵人脫離武器的可能性有多高，也是血量百分比  * 曲線。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_5.png)

武器的捕捉力量，由一個基礎值開始，玩家每多串一個敵人就會越來越低。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_6.png)

武器攻擊力，基礎值 + 串起敵人提供的總額外攻擊力。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_7.png)

被串敵人脫離武器的計算，根據串起敵人的數量查陣列配置的機率參數。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_8.png)

武器血量損失，玩家攻擊時會讓上面串的敵人扣百分比血量，歸零會讓敵人死亡並脫落。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_9.png)

要計算的時候就透過接口，將指定格式的輸入傳入，然後取得輸出結果。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-18_2025-10-02/images/image_10.png)

這樣核心戰鬥需要的計算都有了 :D

至於感想嗎…

雖然算法被抽象隔離出來了，但調用計算接口的地方還是四散在各處，有些寫在敵人身上、有些在捕捉系統，有些則在武器腳本裡，不知道有沒有辦法統一處理？

另一點是輸入、輸出的格式不好修改，因為調用方需要手動填入參數，有時改算法需要不同的輸入就會影響到調用處的程式碼要一起修。

而解決方案、或需不需要解決就再觀察吧 :P