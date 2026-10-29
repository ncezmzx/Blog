---
title: "组合计数"
date: 2026-01-31T21:44:47+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/caoh8hih"
luogu_id: "caoh8hih"
---

[QOJ1838](https://qoj.ac/problem/1838)

很难啊，好像懂了，还没写。

首先要求三个矩形都不相交，先容斥转成一对相交和两对相交，还有都相交。

一对相交很容易，直接扫描线处理出与每个矩形 $i$ 相交的个数 $d_i$，然后由于剩下一个任选，所以方案数是 $\sum (n - 2) d_i$。

两对同理，就是 $2\sum \binom{d_i}{2}$

然后考虑都相交。容斥一下，我们求与 $i$ 相交，但是自身不交的，这个可以用线段树维护，考虑存有多少个左端点和右端点，合并时，把左侧右端点乘以右侧左端点的贡献加上即可。

然后就做完了，没看懂题解。

写完了。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 2e5 + 9;
int n, b[2 * N], c[2 * N], vec[2 * N], d[N];
struct fenwick {
  int c[2 * N];
  void update(int x, int y) { for (; x <= 2 * n; x += x & -x) c[x] += y; }
  int query(int x, int r = 0) { for (; x > 0; x -= x & -x) r += c[x]; return r; }
} adl, adr, dll, dlr, all, alr;
struct pt {
  int x1, y1, x2, y2;
} a[N];
struct info {
  int ls, rs, s;
  info operator+(const info &x) const {
    return {ls + x.ls, rs + x.rs, s + x.s + rs * x.ls};
  }
} sgt[N << 3];
void update(int u, int l, int r, int x, const info &y) {
  if (l == r) return sgt[u] = y, void();
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x, y);
  else update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
info query(int u, int l, int r, int x, int y) {
  if (x <= l && r <= y) return sgt[u];
  int m = (l + r) >> 1;
  if (m >= x && m < y) return query(u << 1, l, m, x, y) + query(u << 1 | 1, m + 1, r, x, y);
  else if (m >= x) return query(u << 1, l, m, x, y);
  else return query(u << 1 | 1, m + 1, r, x, y);
}
int C(int x) { return x * (x - 1) / 2; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> a[i].x1 >> a[i].x2 >> a[i].y1 >> a[i].y2;
    b[2 * i] = a[i].x1, b[2 * i - 1] = a[i].x2, c[2 * i] = a[i].y1, c[2 * i - 1] = a[i].y2;
  }
  sort(b + 1, b + 2 * n + 1);
  sort(c + 1, c + 2 * n + 1);
  for (int i = 1; i <= n; ++i) {
    a[i].x1 = (int) (lower_bound(b + 1, b + 2 * n + 1, a[i].x1) - b);
    a[i].x2 = (int) (lower_bound(b + 1, b + 2 * n + 1, a[i].x2) - b);
    a[i].y1 = (int) (lower_bound(c + 1, c + 2 * n + 1, a[i].y1) - c);
    a[i].y2 = (int) (lower_bound(c + 1, c + 2 * n + 1, a[i].y2) - c);
    // cerr << a[i].x1 << ' ' << a[i].y1 << ' ' << a[i].x2 << ' ' << a[i].y2 << '\n';
    vec[a[i].x1] = i, vec[a[i].x2] = -i, d[i] = -1;
  }
  int g0 = n * (n - 1) * (n - 2) / 6, g1 = 0, g2 = 0, g3 = 0;
  for (int i = 1; i <= 2 * n; ++i) {
    int x = vec[i];
    if (x > 0) {
      d[x] -= dll.query(a[x].y2) - dlr.query(a[x].y1 - 1);
      g3 += C(all.query(a[x].y2) - alr.query(a[x].y1 - 1)) - query(1, 1, 2 * n, a[x].y1, a[x].y2).s;
      all.update(a[x].y1, 1), alr.update(a[x].y2, 1);
      adl.update(a[x].y1, 1), adr.update(a[x].y2, 1);
      update(1, 1, 2 * n, a[x].y1, {1, 0, 0});
      update(1, 1, 2 * n, a[x].y2, {0, 1, 0});
    }
    else {
      x = -x, d[x] += adl.query(a[x].y2) - adr.query(a[x].y1 - 1);
      all.update(a[x].y1, -1), alr.update(a[x].y2, -1);
      dll.update(a[x].y1, 1), dlr.update(a[x].y2, 1);
      update(1, 1, 2 * n, a[x].y1, {0, 0, 0});
      update(1, 1, 2 * n, a[x].y2, {0, 0, 0});
    }
  }
  for (int i = 1; i <= n; ++i) {
    g1 += d[i], g2 += C(d[i]);
  }
  // cerr << g3 << '\n';
  cout << g0 - (n - 2) * g1 / 2 + g2 - g3;
}
```


[P7247](https://www.luogu.com.cn/problem/P7247)

垃圾的 min-max 容斥做法。

套个 min-max 容斥，$E(S) = \sum_{\varnothing  \neq T \subseteq S} (-1)^{|T| - 1}E(\min(T))$。

设 $f_T(u)$ 表示从 $u \to T$ 的最小代价。

则当 $u \in T$ 时，$f_T(u) = 0$，否则 $f_T(u) = \dfrac{\sum_{v = 1}^n f_T(v) + d_{u, v}}{n}$，其中 $d_{u, v}$ 为 $u\to v$ 的距离。

然后带换一下，得到 $E(\min(T)) = \dfrac {\frac{\sum_{u\notin T}\sum_{v = 1}^n d_{u, v}}{|T|} + \sum_{v = 1}^n d_{1, v}}{n}$。

记 $w(u) = \sum_v d_{u, v}$

带入 min-max 得到，$\sum_{\varnothing  \neq T \subseteq S} (-1)^{|T| - 1}\frac{\sum_{u\notin T}w(u)}{|T|n} + \dfrac {w(1)}{n}$。

考虑枚举 $m = |T|$，$\sum_{m = 1}^{n - 1}(-1)^m (\dbinom{n - 1}{m}\dfrac {w(1)}{n} + \sum_{|T| = m, \varnothing \neq T \subseteq S}\frac{\sum_{u\notin T}w(u)}{mn})$。

注意到，$\sum_{|T| = m, \varnothing \neq T \subseteq S}\sum_{u\notin T}w(u) = \dbinom{n - 1}{m}\dfrac {w(1)}{n} + \dbinom{n - 2}{m}\sum_{v = 2}^n w(v)$。

注意到，$\sum_{u = 1}^n w(u)$，可以拆贡献到每条边，直接 dfs 即可，$w(1)$ 单独算。

$O(n)$。

[qoj15036](https://qoj.ac/problem/15036)

考虑点边容斥，我们发现 $S_1, S_2$ 构成的连通块之间隔了一条链，而链上不属于连通块的边数比点数恰好多一。

于是我们考虑计算跨过每条边的方案数，减去不包含一个点的方案数即为答案。

考虑 dsu on tree，维护方案数。我们记录一下子树内与子树外的所有方案 $in_u, out_u$，然后对于每条边方案即为 $in_u\times out_u$，对于每个点即为其任意两条出边所连的点的方案数相乘。

$O(n\log n)$。
