---
title: "高位前缀和"
date: 2025-09-04T21:06:50+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/3xulybkw"
luogu_id: "3xulybkw"
---

求 $\sum_{s \subseteq S} \sum_{t \subseteq s} a_t$。
令 $n = |S|$。

#### 暴力
直接做是 $O(n^3)$。

#### 高位前缀和
我们发现这是一个类似前缀和的东西。

一共有 $n$ 维，每一维只有 $0$ 和 $1$。

这就先当于求一个 $n$ 维前缀和。

考虑二维前缀和的另一种求法：

```cpp
for (int i = 1; i <= n; ++i)
  for (int j = 1; j <= n; ++j)
    s[i][j] += s[i - 1][j];
for (int i = 1; i <= n; ++i)
  for (int j = 1; j <= n; ++j)
    s[i][j] += s[i][j - 1];
```
也就是每一维分开求。

于是高位前缀和就做完了：
```cpp
for (int j = 0; j < n; ++j)
  for (int i = 0; i < 1 << n; ++i)
    if (i >> j & 1) f[i] += f[i ^ 1 << j];
```
$j$ 就是枚举每一维。

思路挺简单的一个东西。
