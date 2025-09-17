---
title: "武器技能施放（< 10% AI）"
date: 2025-09-28
category: ironman-2025
slug: post-2025_09_28-day14-武器技能施放-10-ai
day: 14
---

# Day14 - 武器技能施放（< 10% AI）


為了使用敵人技能，武器也是跟相同的技能系統整合，所以效果都直接兼容。但整合時發現一些需求缺陷，所以也讓 GPT 提供一些修正方案。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-14_2025-09-28/images/image_4.png)

建立一個武器專用的技能 Host，可以把技能加給武器，然後註冊技能的發動時機。發動時機是狀態機的 State。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-14_2025-09-28/images/image_2.png)

再把一個發動技能的 Addon 掛到武器 StateMachine 上，每當進入新的 State 時他就會發出一個技能的訊號，如果有註冊的技能就會自動發動。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-14_2025-09-28/images/image_3.png)

玩家撿一把帶有發射技能的武器，揮擊就會發射子彈，幾次沒發射是因為在冷卻。阿子彈直接穿過怪物是因為我還沒實作真的射彈系統，現在只是測試技能用的。

![圖片](https://raw.githubusercontent.com/angus945/ithelp-2025ironman-posts/refs/heads/main/Publish/day-14_2025-09-28/images/image_1.gif)