---
title: "一些神秘题"
date: 2025-09-04T20:58:25+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/lbqovftx"
luogu_id: "lbqovftx"
---

### [CF1254B2](https://www.luogu.com.cn/problem/CF1254B2)
:::info[Solution]
令 $S_i = \sum_{j = 1}^i a_j$，即 $a$ 的前缀和，$k \mid a_i \Leftrightarrow k \mid S_i$。

有无解先考虑无解，显然 $k \nmid S_n$ 时无解。

那么考虑两种操作：
1. 从 $i$ 放到 $i - 1$。显然 $S_1, \cdots, S_i - 2, S_i, \cdots, S_n$ 是不会变的，只有 $S_{i - 1}$ 会加 $1$。
2. 从 $i$ 放到 $i + 1$。同理，只有 $S_i$ 减 $1$。

因此，这两种操作等价于对前缀和数组 $S$ 加减。

再考虑 $k$ 已知的做法。

先将 $S_i$ 向 $k$ 取模，然后直接贪心计算即可，$O(n)$。

再考虑怎么求 $k$。

已知 $k \mid S_n$ ，直接枚举 $O(n^2)$。

发现若 $k_1 \mid k_2$，那么 $k_1$ 的答案一定不劣于 $k_2$。

所以直接枚举 $n$ 的素因子然后取最小值就可以了。

:::
