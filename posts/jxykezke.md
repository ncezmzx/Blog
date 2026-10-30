---
title: "数论"
date: 2025-08-26T21:07:29+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/jxykezke"
luogu_id: "jxykezke"
---

### exgcd

求 $ax + by = c$ 的一组整数解。

裴蜀定理：有解当且仅当，$\gcd(a, b) \mid c$。

考虑求 $ax + by = \gcd(a, b)$，$c$ 是 gcd 的倍数，$x, y$ 同乘一个数即可。

由于 $\gcd(a, b) = \gcd(a, b \bmod a)$。

所以 $ax_1 + by_1 = \gcd(a, b) = ax_2 + (b\bmod a)y_2 = \gcd(a, b \bmod a)$。

有 $ax_1 + by_1 = a(x_2 - \lfloor\frac ba \rfloor y_2) + by_2$，于是 $x_1 = x_2 - \lfloor \frac ba\rfloor y_2, y_1 = y_2$，于是可以递归求解，直到 $b = 0$，$x = 1, y = 0$。

解的范围 $|x| \le a, |y| \le b$。

### CRT
$$
\begin{cases}
x & \equiv a_1\pmod {m_1}
\\
x &\equiv a_2 \pmod {m_2}
\\
& \ \vdots
\\
x & \equiv a_n \pmod {m_n}
\end{cases}
$$

要求 $m_i$ 互质。

令 $m = \prod m_i, M_i = \sum_{j\not = i} m_j, p_iM_i \equiv 1\pmod {m_i}$，则 $x = \sum_{i} a_ip_iM_i \bmod m$。

显然带入回原式发现，$x \equiv a_i p_i M_i \equiv a_i\pmod {m_i}$。

### exCRT

考虑合并 $x\equiv a_1 \pmod {m_1}, x\equiv a_2 \pmod {m_2}$。

$x = a_1 + pm_1 = a_2 +qm_2$，于是有 $pm_1 - qm_2 = a_2 - a_1$，直接 exgcd 解出一组 $p, q$，代回得 $x \equiv a_1 + pm_1 \pmod {\mathrm{lcm}(m_1, m_2)}$。

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
