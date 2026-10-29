---
title: "？？？？？"
date: 2026-02-05T21:29:59+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/bqe58gq8"
luogu_id: "bqe58gq8"
---

模拟赛题
> 给定一个长为 $n$ 的序列 $a$，求出 $(i, j)$（$1\leq i\leq j \leq n$）的个数，满足 $\min(a_i, \dots ,a_j) \leq a_i\oplus a_j \leq \max(a_i, \dots, a_j)$。

正难则反，求 $a_i\oplus a_j < \min(a_i, \dots, a_j)$ 和 $\max(a_i, \dots, a_j) < a_i\oplus a_j$。

两个本质相同，以前者为例。

后者是 [GYM 104068 K](https://codeforces.com/gym/104068/problem/K)。

最值分治或者建笛卡尔树，然后维护大的一边的 01trie，枚举小的一侧，固定 $x, z$ 查询 $x\oplus y < z$ 的 $y$ 的数量。

这是简单的，在 01trie 上随便做，trie 的维护可以直接合并。

$O(n\log n\log V)$，不是很想写。

这题放 noip 模拟赛 T2？
