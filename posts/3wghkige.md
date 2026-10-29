---
title: "题解：P6958 [NEERC 2017] The Great Wall"
date: 2026-10-28T18:25:05+08:00
author: "Mr_Min"
category: "题解 P6958"
tags: ["题解 P6958", "洛谷"]
source: "https://www.luogu.com.cn/article/3wghkige"
luogu_id: "3wghkige"
---

令 $B_i = b_i - a_i$，$C_i = c_i - b_i$。

那么对于一组 $x, y$，$\sum h_i$ 等于 $\sum a_i$ 加上两个区间并的 $B$ 和两个区间交的 $C$。

对 $B, C$ 做前缀和，令 $s = \sum a_i$ 分相交和相离两种情况讨论：

- 相交。$x + r - 1 \ge y$，则 $\sum h_i = s + B_{y + r - 1} - B_{x - 1} +C_{x +r - 1} - C_{y - 1} = s +B_{y +r - 1} - C_{y - 1}+C_{x + r - 1} - B_{x - 1}$。
- 相离。$x + r - 1 < y$，则 $\sum h_i = s +B_{x + r - 1} - B_{x - 1} +B_{y +r - 1} - B_{y - 1}$。

先二分答案 $w$，考虑求 $\sum h_i \leq w$ 的数量。

根据上面的讨论，令 $o_i = B_{i +r - 1} - B_{i - 1}, p_i = B_{i + r - 1} - C_{i - 1}, q_i = C_{i + r - 1} - B_{i - 1}$。

则 $\sum h_i$ 分别为 $s + p_y + q_x$（$x + r - 1 \ge y$） 和 $s + o_x + o_y$（$x +r - 1 < y$）。

先对 $q, o$ 离散化，然后直接对 $y$ 做扫描线，用树状数组维护 $q_x, o_x$ 即可，$O(n\log n \log V)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 2e5 + 9;
int n, len, k, a[N], b[N], c[N], s, o[N], q[N], co, cq, c1[N], c2[N], u1[N], u2[N], tg1, tg2, d[N], e[N];
void update1(int x, int y) { for (; x <= co; x += x & -x) u1[x] != tg1 && (u1[x] = tg1, c1[x] = 0), c1[x] += y; }
int query1(int x, int r = 0) { for (; x > 0; x -= x & -x) u1[x] != tg1 && (u1[x] = tg1, c1[x] = 0), r += c1[x]; return r; }
void update2(int x, int y) { for (; x <= cq; x += x & -x) u2[x] != tg2 && (u2[x] = tg2, c2[x] = 0), c2[x] += y; }
int query2(int x, int r = 0) { for (; x > 0; x -= x & -x) u2[x] != tg2 && (u2[x] = tg2, c2[x] = 0), r += c2[x]; return r; }
bool chk(int x) {
  x -= s;
  int cnt = 0;
  ++tg1, ++tg2;
  for (int i = 1; i <= n - len + 1; ++i) {
    if (i - len >= 1) update1(d[i - len], 1), update2(e[i - len], -1);
    cnt += query1(upper_bound(o + 1, o + co + 1, x - b[i + len - 1] + b[i - 1]) - o - 1);
    cnt += query2(upper_bound(q + 1, q + cq + 1, x - b[i + len - 1] + c[i - 1]) - q - 1);
    update2(e[i], 1);
  }
  return cnt < k;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> len >> k;
  for (int i = 1; i <= n; ++i) cin >> a[i], s += a[i];
  for (int i = 1; i <= n; ++i) cin >> b[i];
  for (int i = 1; i <= n; ++i) cin >> c[i], c[i] -= b[i], b[i] -= a[i];
  for (int i = 1; i <= n; ++i) b[i] += b[i - 1], c[i] += c[i - 1];
  int m = n - len + 1;
  for (int i = 1; i <= m; ++i) {
    o[i] = b[i + len - 1] - b[i - 1];
    q[i] = c[i + len - 1] - b[i - 1];
  }
  sort(o + 1, o + m + 1);
  sort(q + 1, q + m + 1);
  co = unique(o + 1, o + m + 1) - o - 1;
  cq = unique(q + 1, q + m + 1) - q - 1;
  for (int i = 1; i <= m; ++i) {
    d[i] = lower_bound(o + 1, o + co + 1, b[i + len - 1] - b[i - 1]) - o;
    e[i] = lower_bound(q + 1, q + cq + 1, c[i + len - 1] - b[i - 1]) - q;
  }
  int l = 0, r = 1e6 * n;
  while (l < r) {
    int m = (l + r) >> 1;
    if (chk(m)) l = m + 1;
    else r = m;
  }
  cout << l;
}
```
