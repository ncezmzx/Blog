---
title: "数论"
date: 2025-08-26T21:07:29+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/jxykezke"
luogu_id: "jxykezke"
---

#### 互质
##### 快速判断较小数互质
快速判断两个数 $a, b\leq V$ 是否互质，$V\leq 5\times 10^4$。

考虑 $\leq \sqrt V$ 的质因子，数量不超过 $64$，直接状压。

大于 $\sqrt V$ 的质因子个数 $\leq 1$，直接存。

判断时大的直接判相等，小的与一下即可。

时间复杂度 $O(V)-O(1)$，实测 $10^7$ 时 1 s，$\gcd$ 要 1.7 s。
#### GCD
比较重要的性质（$x < y$）:
1. $\gcd(x, y) = \gcd(x, y - x)\leq y - x$
2. $\gcd(x, y)^k = \gcd(x^k, y^k)$
3. $p \mid \gcd(x, y) \Leftrightarrow p \mid x, p \mid y$

对于两个数 $x, y$（$x < y$），显然 $\gcd(x, y) = \gcd(x, y - x) \leq y - x$。

因此 $x, y$ 所共同包含的质因子 $p \leq y - x$。

考场上没想到然后炸了。
