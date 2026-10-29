---
title: "review"
date: 2026-09-03T23:23:43+08:00
author: "Mr_Min"
category: "数据结构"
tags: ["数据结构", "洛谷"]
source: "https://www.luogu.com.cn/article/sywuq2b7"
luogu_id: "sywuq2b7"
---

## 数据结构
### [P8868 [NOIP2022] 比赛](https://www.luogu.com.cn/problem/P8868)
很久以前写过分治做法，现在补一下历史和，比较板的题。
#### 题意
给定长度为 $n$ 的两个数组 $a, b$，$Q$ 次询问 $[l, r]$，每次询问求 $\sum_{l\leq L \leq R \leq r} (\max_{i = L}^R a_i)(\max_{i = L}^R b_i)$。
#### 做法
扫描线，扫 $r$，令 $A_l = \max_{i = l}^r a_i, B_l = \max_{i = l}^r b_i$，则对于固定的子区间右端点 $r$，答案是 $s_l = A_lB_l$。每次 $r\to r + 1$ 时记录历史和，$\sum_{i = l}^r s_i$ 即为 $l, r$ 的答案。

然后就简单了，$A, B$ 用单调栈维护转为区间赋值，$s$ 用线段树维护，需要支持 $A_iB_i$ 历史和，$A, B$ 区间赋值。

历史和考虑直接上矩阵，线段树的 info 用向量即可，tag 用矩阵，然后考虑构造。

首先 info 要包含当前和与历史和 $s, hs$，显然赋值操作必须要 $A, B$ 的和 $X, Y$，最后赋值更新 $X, Y$ 需要区间长度 $L$：

$$
\begin{bmatrix}s & hs & X & Y & L\end{bmatrix}
$$

以对 $A$ 赋值 $v$ 为例，tag 为：

$$
\begin{bmatrix}
0 & 0 & 0 & 0 & 0\\
0 & 1 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0\\
v & 0 & 0 & 1 & 0\\
0 & 0 & v & 0 & 1
\end{bmatrix}
$$

覆盖完 $A, B$ 后记录一次历史和。

$$
\begin{bmatrix}
1 & 1 & 0 & 0 & 0\\
0 & 1 & 0 & 0 & 0\\
0 & 0 & 1 & 0 & 0\\
0 & 0 & 0 & 1 & 0\\
0 & 0 & 0 & 0 & 1
\end{bmatrix}
$$

时间复杂度 $\mathcal{O}(5^3 \ Q\log n)$。

直接这样写，是 [72 分](https://www.luogu.com.cn/record/296468234)。

注意到矩阵在运算过程中非定值的位置很少，只有 $12$ 个，于是把矩阵拆出来手写运算就可以了。

[跑的飞快](https://www.luogu.com.cn/record/296476313)。

### [P17307 [ICPC 2026 Xi'an I] Zebra Crossing](https://www.luogu.com.cn/problem/P17307)

火箭毛毛虫。

#### 题意
给定一颗 $n$ 个点的树，每个点有黑白颜色，每次可以从瞬移到边数不超过 $k$ 的点上。问从 $1$ 到其余点经过的最小黑点数。

#### 做法
有一个 $\mathcal{O}(n)$ 的贪心，但我不会。

有一个 $\mathcal{O}(n\log n)$ 的线段树优化 dp，但我还是不会。

有一个 $\mathcal{O}(n\log n)$ 的点分树优化 01 bfs，这个我会。

注意到把距离 $\leq k$ 的点对连边后，跑 01 bfs 就是答案。

所以先建出点分树，然后考虑怎么优化 01 bfs 的松弛操作。设当前点 $x$ 答案 $d_x$，我们不断往根跳，每跳到一个重心，他可以更新的点都是一个包含重心的连通块。更进一步，可以发现在一个重心下松弛过的点，不会在同一个重心下松弛第二遍，所以直接维护一个双指针即可做到 $\mathcal{O}(n\log n)$。

然后这个做法很慢，需要大力卡常，把递归改成非递归，换建图方式，手写 deque, queue 等。

[代码](https://www.luogu.com.cn/record/297155150)。

### [P8353 [SDOI / SXOI2022] 无处存储](https://www.luogu.com.cn/problem/P8353)
毒瘤。

#### 题意
树上路径加，路径求和，但是 $n \leq 7\times 10^6$，5 s，64 MB，强制在线。

#### 做法
存权值要 30 MB，存父亲要 30 MB，光读入的内容就 60 MB 了。

所以我们不能开 $\mathcal{O}(n)$ 的数组，只够开 $\mathcal{O}(\sqrt n)$ 的。

考虑树分块，然后你发现树都遍历不了，只能随机撒点，然后暴力跳每个关键点的父亲。

为了方便操作，我们对关键点建虚树，所有所有虚树上的点都是关键点。

但是开不了数组，所以为了建虚树，我们开一个 bitset，标记关键点到根的路径，有重复的点就加入虚树，$\mathcal{O}(n\sqrt n)$。

建完虚树，我们考虑操作。把 $x\to y$ 差分成 $x\to 1, y\to 1, lca(x, y)\to 1, fa_{lca(x, y)} \to 1$ 四条链。

对于一条链 $x\to 1$，我们先在原树上暴力跳到最近的关键点，然后再在虚树上跳到根，虚树要维护相邻关键点间的信息。

修改同理，暴力跳的时候直接改权值，在虚树上时，打标记。

这一部分是 $\mathcal{O}(q\sqrt n)$ 的。

现在问题是求 lca。对于同属于一个关键点的两点，直接暴力。其余情况先暴力所属关键点在虚树上的 lca。

有一点要特判，就是在虚树上是一条链时，这种情况要链顶往下走一个关键点，然后从这个关键点与原树上的 lca。

然后就做完了，比较绕，尤其是 lca。

[代码](https://www.luogu.com.cn/record/296603757)。

### [P14400 [JOISC 2016] 回转寿司 / Sushi](https://www.luogu.com.cn/problem/P14400)
经典题。
#### 题意
一个长为 $n$ 的环 $a$，$q$ 次操作，每次给定 $l, r, x$，表示从 $l$ 到 $r$，依次遍历，若 $x < a_i$ 交换两者，否则不操作，输出操作后的 $x$。
#### 做法
分块，完整经过一个块，要么不换，要么换出来是块内最大值，所以整块维护 priority_queue，每次比最大值交换即可，散块暴力，然后重构 pq。

但是整块操作后我们把 $x$ 交换进去了，于是考虑打 tag，问题在于 tag 之间怎么处理。

分析一下，可以发现 tag 顺序不影响，因为一个位置只会被更小的数交换，所以最后一定是最小的 tag。

于是考虑用 pq 维护 tag，每次直接用最小的比较然后交换。

快长取 $\mathcal{O}(\sqrt n)$，时间复杂度 $\mathcal{O}(n\sqrt n \log n)$。

[代码](https://www.luogu.com.cn/record/297375203)

用到这个思路的题：

[P2075 区间 LIS](https://www.luogu.com.cn/problem/P2075)

[P16998 【MX-S15-T4】「DLESS-5」Waking Shadows](https://www.luogu.com.cn/problem/P16998)（还没写）
