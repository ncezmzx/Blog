---
title: "2026.10.20 | 喵喵题"
date: 2026-10-30T10:56:40+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/rgzauen6"
luogu_id: "rgzauen6"
---

T4

> 将 $a$ 中出现次数为奇数的数字按照次数为第一关键字，大小为第二关键字排序，得到 $F(a)$。
>
> 将 $a$ 中出现次数为偶数的数字按照次数为第一关键字，大小为第二关键字排序，得到 $G(a)$。
>
> 给定一个长度为 $n$ 的序列 $a$，有 $q$ 次询问，每次询问 $l, r, V, m$，求：
>
>
> 将令 $b$ 为长度为 $m$，值域为 $V$ 的序列，求 $F(a_l, \dots, a_r) = G(b)$ 的 $b$ 数量模 $2$ 的结果。
>
> $n, q\leq 10^6$

首先令 $c = |F(a_l,\dots, a_r)|$，$M = \max F(a_l, \dots, a_r)$，若 $M > V$ 答案为 $0$。

然后考虑计数 $b$ 中数字的出现次数 $cnt_i$。对于一种 $cnt$ 序列，我们只需要将偶数排序后将 $F$ 的数字依次赋值过来即可得出偶数次数对应的数，奇数随便赋值，则根据 $cnt$ 我们可以得出对应的 $b$ 的数量。不考虑每个次数对应的数，则对应的 $b$ 有 $\dbinom{m}{cnt_1, \dots, cnt_c}$ 种。

然后有一个很神的东西：Legendre 公式。

对于正整数 $n$，阶乘 $n!$ 中含有的素数 $p$ 的幂次 $\nu_p(n!)$ 为 $\nu_p(n!) = \sum_{i=1}^{\infty} \left\lfloor \dfrac{n}{p^i} \right\rfloor = \dfrac{n-S_p(n)}{p-1}$，其中，$S_p(n)$ 为 $p$ 进制下 $n$ 的各个数位的和。特别地，阶乘中 $2$ 的幂次是 $\nu_2(n!)=n-S_2(n)$。

于是乎，$\dbinom{m}{cnt_1, \dots, cnt_c} = \dfrac {m!}{\prod cnt_i!}$。

所以 $v_2(\dbinom{m}{cnt_1, \dots, cnt_c}) = v_2(m!) - \sum v_2(cnt_i!) = m - S_2(m) - \sum cnt_i - S_2(cnt_i) = \sum S_2(cnt_i) - S_2(m)$。

显然，当 $\sum S_2(cnt_i)  = S_2(m)$ 即 $cnt_i$ 刚好划分了 $m$ 的所有二进制位时，其对应的 $b$ 的数量模 $2$ 为 $1$。

于是考虑计数 $m$ 的二进制划分方案，即 $pc = \mathrm{popcount}(m)$。

- 若 $pc < c$，无解，答案为 $0$。
- 否则若 $m$ 为偶数，则方案是第二类斯特林数，$S(pc, c)$。
- 否则若 $m$ 为奇数，则我们需要枚举奇数占据了多少个二进制位，以及出现奇数次的数字是多少，方案为 $(V - c)\sum_{i = 1}^{pc} S(pc - i, c)\dbinom{pc - 1}{i - 1}$。

$pc$ 都是 $O(\log n)$ 级别，所以只要算出 $c, M$ 即可 $O(\log n)$ 求出答案。

考虑求 $c, M$，考虑可持久化线段树，每个数字随机赋权，若一个区间的权值异或和为 $0$，则这个区间中不存在出现次数为奇数的数，这样可以做到单组询问 $O(c\log V)$ 求 $c, M$。

但是 $c > pc$ 无解，所以单组 $O(\log n\log V)$。

总复杂度 $O(n\log n + \log^2 n + q\log n \log V)$。
