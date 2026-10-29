---
title: "题解：P17148 [ICPC 2017 Xi'an R] Naomi with Array"
date: 2026-10-24T15:53:03+08:00
author: "Mr_Min"
category: "题解 P17148"
tags: ["题解 P17148", "洛谷"]
source: "https://www.luogu.com.cn/article/7p7xxib2"
luogu_id: "7p7xxib2"
---

相同的题 [P7650 [BalticOI 2007] Ranklist Sorting (Day 1)](https://www.luogu.com.cn/problem/P7650)。

这两题做法是完全一样的，所以直接把自己的题解搬过来了。

先对 $A$ 离散化得到 $a$，$a$ 是一个排列，然后观察发现，每个位置最多移动一次。

证明考虑反证，假设我们在 $s \to t$ 中加了一步变成 $s\to m \to t$，那么 $[s, m)$ 的人代价减小 $2$，却多加了 $2j$ 的代价，显然不优。

于是容易想到一个暴力的移动方式，把每个人从小到大放到第一个位置。记 $b_i = \sum_{j < i} [a_j > a_i]$，那么移动 $a_i$ 时，他的下标为 $a_i + b_i$，这次移动代价为 $a_i + b_i +1$，总代价 $\sum a_i + b_i +1$。

但是这样显然不优，因为我们移动了所有位置。事实上，我们可以保留任意一个下降子序列不移动。

考虑保留一个位置 $a_i$ 不动，会对总代价产生多少贡献。先把代价拆一下 $i + j = (i - 1) + (j - 1) +2$，$i - 1, j - 1$ 即移动前后的在 $a_i$ 前面的数的个数。于是我们可以把总代价里的 $(i - 1) +(j - 1)$ 拆到原序列的二元组 $(a_i, a_j)$ 上。

对一个包含被保留元素 $i$ 的二元组 $(i,j)$（$i$ 不动，$j$ 至多移动一次）：

- $j$ 移动前，$i,j$ 仍是初始相对顺序，即 $i$ 在 $j$ 前 $\iff i<j$；
- $j$ 移动后，$i,j$ 已固定在最终降序中的相对顺序，即 $i$ 在 $j$ 前 $\iff a_i>a_j$。

因此保留后该二元组的贡献为 $[i<j]+[a_i>a_j]$。原方案中两者都移动，贡献为 $2$（较大的数原本在前，即 $[a_i>a_j]=[i<j]$）或 $1$（否则）。分类讨论一下：

- $a_i > a_j, i < j$：原贡献 $2$。保留后 $[i<j]+[a_i>a_j]=2$：$j$ 最终仍移到 $i$ 后面，且移动前后 $i$ 都在 $j$ 前面，$j$ 的这次移动照样计满 $2$，贡献不变。
- $a_i < a_j, i < j$：原贡献 $1$。保留后 $j$ 移到 $i$ 前面，$[i<j]+[a_i>a_j]=1$，贡献不变。
- $a_j > a_i, j < i$：原贡献 $2$。保留后 $j$ 移到 $i$ 前面，而移动前 $i$ 也在 $j$ 后面，$[i<j]+[a_i>a_j]=0$，贡献从 $2$ 变 $0$，总代价减 $2$。
- $a_j < a_i, j < i$：原贡献 $1$。保留后 $j$ 移到 $i$ 后面，$[i<j]+[a_i>a_j]=1$，贡献不变。

因此保留 $a_i$ 使总代价减少 $2(b_i+1)$。

于是问题就变成了一个带权最长下降子序列，直接做就是 $O(n^2)$，容易用树状数组优化到 $O(n\log n)$。

第二问的话，容易发现就是最大化保留的子序列长度，容易处理。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 1e6 + 9;
int n, a[N], c[N], b[N], e[N];
pair<int, int> d[N], f[N];
void update(int x, int y) {
  for (; x > 0; x -= x & -x) c[x] += y;
}
int query(int x, int r = 0) { for (; x <= n; x += x & -x) r += c[x]; return r; }
void update1(int x, pair<int, int> y) {
  for (; x > 0; x -= x & -x) d[x] = max(d[x], y);
}
pair<int, int> query1(int x, pair<int, int> r = {0, 0}) { for (; x <= n; x += x & -x) r = max(r, d[x]); return r; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  while (cin >> n) {
    for (int i = 1; i <= n; ++i) d[i] = f[i] = {0, 0}, c[i] = 0;
    for (int i = 1; i <= n; ++i) cin >> a[i], e[i] = a[i];
    sort(e + 1, e + n + 1);
    for (int i = 1; i <= n; ++i) a[i] = lower_bound(e + 1, e + n + 1, a[i]) - e;
    int ans = 0;
    for (int i = 1; i <= n; ++i) b[i] = query(a[i]), update(a[i], 1), ans += 1 + a[i] + b[i];
    for (int i = 1; i <= n; ++i) {
      auto [x, y] = query1(a[i]);
      f[i] = {x + 2 * (b[i] + 1), y};
      update1(a[i], {x + 2 * (b[i] + 1), i});
    }
    auto [x, y] = query1(1);
    int p = y, c = 0;
    while (p) ++c, p = f[p].second;
    cout << ans - x << ' ' << n - c << '\n';
  }
}
```
