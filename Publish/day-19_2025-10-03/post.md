---
title: "敵人脫離效果（ 10% AI）"
date: 2025-10-03
category: ironman-2025
slug: post-2025_10_03-day19-敵人脫離效果-10-ai
day: 19
---

# Day 19 - 敵人脫離效果（< 10% AI）


被串到武器上的敵人還是有機會脫離，畢竟設定上主角是真的拿武器把串起來，所以敵人就算在武器上也還是活著的。

所以也可能在某個時機被噴回場地上，憤怒的攻擊玩家？

考慮到遊戲畫面的喜感，我希望敵人噴飛有更誇張的表現，整隻武器的敵人會往上炸開之類的。

原本要直接加在敵人的主腳本，但腳本其實有點職責混雜了，不好維護，最後決定多包一層容器物件用來釋放敵人。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-19_2025-10-03/images/image_3.png)

當敵人從武器脫離時，不會直接恢復敵人的活動，而是會先放入另一個有 Collider 與 Rigidbody 的容器，並隨機往上施力丟出。我還有給容器施加額外的 Toque 力量，讓敵人噴飛的時候有更誇張的旋轉效果。

![圖片.png](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-19_2025-10-03/images/image_4.png)

在「當前」的設計中，玩家武器串越多敵人，行動時敵人就有更高的機率從武器脫離，算是一種武器變強導致的風險（但這樣設計有問題，後面改掉了）。

![Movie_019_0.gif](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-19_2025-10-03/images/image_1.gif)

除了意外脫離之外，玩家也可以用重擊把武器上的敵人甩出去，會對砸到的目標造成傷害 ww

![STUST_Project_4-1 - AllIntegrateTest - Windows, Mac, Linux - Unity 6 (6000.0.34f1) _DX11_ 2025-09-07 19-59-25 - Trim_0 (1).gif](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-19_2025-10-03/images/image_2.gif)