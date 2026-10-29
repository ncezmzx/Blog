---
title: "2026.10.29 | k-简并图"
date: 2026-10-29T18:39:52+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/6aqykgs6"
luogu_id: "6aqykgs6"
---

### T3
神秘 MO 题。

给定一张简单无向图，所有点度数 $\leq 6$，图是 k-简并图*，$k\leq 5$。

构造一种点集划分 $V_1, V_2, V_3, V_4$，使得 $V_1, V_2$ 是独立集，$V_3, V_4$ 的所有联通块均为链。


*k-简并图：对于图的任意一个导出子图，均存在一个点其度数 $\leq k$。

#### 做法

首先考虑 k-简并图 的性质。

我们考虑一种类似拓扑序的东西，每次找到图中度数最小的点，其度数必然 $\leq k$，假如序列 $v$，删去这个点，重复直到删除所有点。

容易发现 $v_i$ 与 $v_{i +1}\sim v_{n}$ 的连边数量 $\leq k$，反过来存在这样的序列 $v$ 也可以证明原图为 k-简并图，两者是等价的。

于是有结论：
- 一个图 $G = (V, E)$ 是 k-简并图，当且仅当存在一个 $V$ 的排列 $v$，满足 $\#\{i < j \mid (v_i, v_j) \in E\}\leq k$。

然后根据这个结论，我们按 $v$ 从后往前染色，每个点最多与 $k$ 个已染色的点相邻，于是又有结论：
- 任意 k-简并图 都可以用 $k + 1$ 种颜色染色，使得任意一条边连接的两点颜色不同。

于是 $k \le 3$ 是简单的，直接 $4$ 染色，然后划 $4$ 个独立集即可。

考虑 $k = 5$ 怎么做。

又有结论：
- 对于任意 $(p + q +1)$-简并图 $G=(V, E)$，都可以将其点集划分为两个子集 $A, B$，其导出子图分别是 $p$-简并图 和 $q$-简并图。

证明：

依然在 $v$ 上从后往前划分点集，对于 $v_i$，若其与 $A$ 的连边数量 $\leq p$，则加入 $A$ 中，否则其与 $A$ 的连边至少为 $p + 1$，则与 $B$ 的连边至多为 $q$，加入 $B$ 即可，证毕。

于是我们可以将 5-简并图，划分成两个 0-简并图 $V_1, V_2$ 和两个 1-简并图 $V_3, V_4$。

但是 1-简并图 是森林，而我们要的是一堆链，考虑调整。

对于一个点 $u\in V_3$（$V_4$ 同理），其在导出子图中的度数 $\ge 3$，即不构成链，那么由于原图度数 $\leq 6$，则令 $d_i = \#\{v\in V_i \mid (u, v) \in E\}$，$d_1 + d_2 + d_4 \leq 3$。

若 $d_1 = 0$ 或 $d_2 = 0$，直接将 $u$ 加入 $V_1, V_2$ 即可，仍为独立集。

否则 $d_4 \leq 1$，直接加入 $V_4$ 即可。

按照这种方式调整 $V_3, V_4$ 后，显然满足条件。

直接维护即可，$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1e5 + 9;
using vec = vector<int>;
int n, m;
vector<pair<int, int>> e;
pair<vec, vec> split(const vec &pt, int p, int q) {
  vec tmp(n), deg(n), col(n), a, b;
  vector<vec> es(n);
  for (int i : pt) tmp[i] = 1;
  vector<pair<int, int>> E;
  for (auto [x, y] : e)
    if (tmp[x] && tmp[y]) {
      E.emplace_back(x, y);
      es[x].push_back(y), es[y].push_back(x);
      ++deg[x], ++deg[y];
    }
  priority_queue<pair<int, int>> Q;
  for (int i : pt) {
    Q.push({-deg[i], i});
  }
  vec v;
  while (!Q.empty()) {
    auto [d, x] = Q.top();
    Q.pop(), d = -d;
    if (d != deg[x]) continue;
    v.push_back(x), deg[x] = 0;
    for (int y : es[x])
      if (deg[y]) {
        --deg[y];
        Q.push({-deg[y], y});
      }
  }
  int m = v.size();
  assert(v.size() == pt.size());
  for (int i = m - 1; i >= 0; --i) {
    int P = 0, Q = 0;
    for (int y : es[v[i]]) {
      if (!col[y]) continue;
      P += col[y] == 1, Q += col[y] == 2;
    }
    if (P <= p) col[v[i]] = 1, a.push_back(v[i]);
    else col[v[i]] = 2, b.push_back(v[i]);
  }
  return make_pair(a, b);
}
void adjust(vec &a, vec &b, vec &c, vec &d) {
  vec col(n, 3);
  vector<vec> es(n);
  for (auto [x, y] : e) es[x].push_back(y), es[y].push_back(x);
  for (int i : b) col[i] = 0;
  for (int i : c) col[i] = 1;
  for (int i : d) col[i] = 2;
  vec na;
  for (int i : a) {
    int cnt[4] = {0, 0, 0, 0};
    for (int y : es[i]) {
      ++cnt[col[y]];
    }
    // cnt[0] + cnt[1] + cnt[2] <= 6
    if (cnt[3] <= 2) na.push_back(i);
    else if (cnt[0] == 0) b.push_back(i);
    else if (cnt[1] == 0) c.push_back(i);
    else assert(cnt[2] <= 2), d.push_back(i);
  }
  a.swap(na);
}
void print(const vec &u) {
  cout << u.size() << '\n';
  for (int i : u) cout << i + 1 << ' ';
  cout << '\n';
}
signed main() {
#ifndef LOCAL
  freopen("quattuor.in", "r", stdin);
  freopen("quattuor.out", "w", stdout);
#endif
  cin.tie(nullptr)->sync_with_stdio(false);
  int cid, tt;
  cin >> cid >> tt;
  while (tt--) {
    cin >> n >> m;
    e.clear();
    for (int i = 1, x, y; i <= m; ++i) {
      cin >> x >> y, --x, --y;
      e.emplace_back(x, y);
    }
    vec p(n);
    iota(p.begin(), p.end(), 0);
    auto [V1, _1] = split(p, 0, 4);
    auto [V2, _2] = split(_1, 0, 3);
    auto [V3, V4] = split(_2, 1, 1);
    adjust(V3, V1, V2, V4);
    adjust(V4, V1, V2, V3);
    print(V1), print(V2), print(V3), print(V4);
  }
}
```

### T4

维护一个序列 $a$，支持插入、删除、查询最大配对数。每对 $(x, y)$ 合法当且仅当 $x + y \leq M$。

$n, Q \leq 4 \times 10^5$。

#### 考场做法

考虑不带修怎么做。

排序，令 $p_i = \max_{a_i + a_j \leq M} j$。

二分答案 $m$ ，则 $1\sim m$ 与 $2 * m\sim m + 1$ 两两配对，等价于 $p_i\ge 2 \times m - i + 1$。

考虑离线后离散化，用权值线段树维护 $p_i +i$，考虑每次插入一个数 $a_k$ ，对 $p$ 的影响是单点修改和区间加，可以维护。

考场写唐了，写了一堆 hyw 的东西快 200 行。

赛后调出来了。

$O(n\log^2 n)$

```cpp
#include <bits/stdc++.h>
using namespace std;
char buf[1 << 20], *p1, *p2;
#define gc (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 1 << 20, stdin), p1 == p2) ? EOF : *p1++)
template<class T> void read(T &x) {
  x = 0;
  char c = gc;
  for (; c < '0' || '9' < c; c = gc);
  for (; '0' <= c && c <= '9'; c = gc) x = (x << 1) + (x << 3) + (c & 15);
}
constexpr int N = 8e5 + 9;
int n, m, q, cnt, len;
pair<int, int> b[N], a[N];
struct Q {
  int o, x, y;
} qs[N];
int tg[N << 2];
struct info {
  int cnt, mn;
  info(int x = 0, int y = 0x3f3f3f3f) : cnt(x), mn(y) {}
  info operator+(const info &rhs) const {
    return {cnt + rhs.cnt, min(mn, rhs.mn)};
  }
  info operator+(const int &rhs) const {
    return {cnt, mn + rhs};
  }
} sgt[N << 2];
void build(int u, int l, int r) {
  if (l == r) return ;
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
}
void apply(int u, int x) {
  tg[u] += x, sgt[u] = sgt[u] + x;
}
void down(int u) {
  if (tg[u]) apply(u << 1, tg[u]), apply(u << 1 | 1, tg[u]), tg[u] = 0;
}
void update(int u, int l, int r, int x, int y, int z) {
  if (x > y) return ;
  if (x <= l && r <= y) return apply(u, z);
  int m = (l + r) >> 1;
  down(u);
  if (m >= x) update(u << 1, l, m, x, y, z);
  if (m < y) update(u << 1 | 1, m + 1, r, x, y, z);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
int find(int u, int l, int r, int x) {
  if (l > x) return 0;
  if (r <= x) return sgt[u].cnt;
  int m = (l + r) >> 1;
  down(u);
  int res = find(u << 1, l, m, x);
  if (m < x) res += find(u << 1 | 1, m + 1, r, x);
  return res;
}
void update(int u, int l, int r, int x, int y) {
  if (x > r || x < l) return ;
  if (l == r) {
    tg[u] = 0;
    if (y == 0x3f3f3f3f) sgt[u] = {0, y};
    else sgt[u] = {1, y + find(1, 1, cnt, l - 1) + 1};
    return ;
  }
  int m = (l + r) >> 1;
  down(u);
  if (m >= x) update(u << 1, l, m, x, y);
  else update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
int query(int u, int l, int r, int x) {
  if (x == sgt[u].cnt) return sgt[u].mn;
  if (l == r) return 0x3f3f3f3f;
  int m = (l + r) >> 1;
  down(u);
  if (sgt[u << 1].cnt >= x) return query(u << 1, l, m, x);
  else return min(sgt[u << 1].mn, query(u << 1 | 1, m + 1, r, x - sgt[u << 1].cnt));
}
void ins(int x) {
  int mb = upper_bound(b + 1, b + cnt + 1, make_pair(m - b[x].first, 0x3f3f3f3f)) - b - 1;
  update(1, 1, cnt, 1, mb, 1);
  int p = find(1, 1, cnt, mb) + (b[x].first * 2 <= m);
  update(1, 1, cnt, x, p);
  update(1, 1, cnt, x + 1, cnt, 1);
  ++len;
}
void ers(int x) {
  int mb = upper_bound(b + 1, b + cnt + 1, make_pair(m - b[x].first, 0x3f3f3f3f)) - b - 1;
  update(1, 1, cnt, x, 0x3f3f3f3f);
  update(1, 1, cnt, 1, mb, -1);
  update(1, 1, cnt, x + 1, cnt, -1);
  --len;
}
signed main() {
  // freopen("report.err", "w", stderr);
#ifndef LOCAL
  freopen("relay.in", "r", stdin);
  freopen("relay.out", "w", stdout);
#endif
  cin.tie(nullptr)->sync_with_stdio(false);
  read(n), read(m);
  for (int i = 1; i <= n; ++i) read(a[i].first), a[i].second = i;
  read(q);
  for (int i = 1; i <= q; ++i) {
    read(qs[i].o);
    if (qs[i].o == 1) read(qs[i].x), read(qs[i].y), a[qs[i].x] = make_pair(qs[i].y, i + n);
    else if (qs[i].o == 2) read(qs[i].x);
  }
  for (int i = 1; i <= n + q; ++i)
    if (a[i].second > 0) b[++cnt] = a[i];
  sort(b + 1, b + cnt + 1);
  for (int i = 1; i <= n + q; ++i) {
    if (a[i].second > 0) a[i].first = lower_bound(b + 1, b + cnt + 1, a[i]) - b;
  }
  build(1, 1, cnt);
  for (int i = 1; i <= n; ++i) ins(a[i].first);
  for (int i = 1; i <= q; ++i) {
    if (qs[i].o == 1) ins(a[qs[i].x].first);
    else if (qs[i].o == 2) ers(a[qs[i].x].first);
    else {
      int l = 0, r = len / 2;
      while (l < r) {
        int m = (l + r + 1) >> 1;
        if (query(1, 1, cnt, m) >= 2 * m + 1) l = m;
        else r = m - 1;
      }
      cout << l << '\n';
    }
  }
  return 0;
}
```

#### 题解做法

考虑匹配，$a_i \leq \frac M2$ 的部分可以两两匹配。


$a_i > \frac M2$ 的部分要和第一个部分匹配。

考虑按 $|a_i - \frac M2|$ 排序，那么每个第二部分的点只能和比他大的第一部分点配对，类似括号匹配，信息容易合并，可以直接用线段树维护。

$O(n\log n)$

这个做法全方位薄纱我的做法。

```cpp
#include <bits/stdc++.h>
using namespace std;
char buf[1 << 20], *p1, *p2;
#define gc (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 1 << 20, stdin), p1 == p2) ? EOF : *p1++)
template<class T> void read(T &x) {
  x = 0;
  char c = gc;
  for (; c < '0' || '9' < c; c = gc);
  for (; '0' <= c && c <= '9'; c = gc) x = (x << 1) + (x << 3) + (c & 15);
}
constexpr int N = 8e5 + 9;
int n, m, q, cn, a[N], b[N], c[N], cnt[N][2];
struct Q {
  int o, x, y;
} qs[N];
struct info {
  int s, ls, rs;
  info(int x = 0, int y = 0, int z = 0) : s(x), ls(y), rs(z) {}
  info operator+(const info &rhs) const {
    return {s + rhs.s + min(rs, rhs.ls), ls + rhs.ls - min(rs, rhs.ls), rs + rhs.rs - min(rs, rhs.ls)};
  }
} sgt[N << 2];
void update(int u, int l, int r, int x, const info &y) {
  if (l == r) return sgt[u] = y, void();
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x, y);
  else update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
void upd(int x, int y) {
  cnt[a[x]][c[x]] += y;
  update(1, 1, cn, a[x], {min(cnt[a[x]][0], cnt[a[x]][1]), cnt[a[x]][1] - min(cnt[a[x]][0], cnt[a[x]][1]), cnt[a[x]][0] - min(cnt[a[x]][0], cnt[a[x]][1])});
}
signed main() {
#ifndef LOCAL
  freopen("relay.in", "r", stdin);
  freopen("relay.out", "w", stdout);
#endif
  cin.tie(nullptr)->sync_with_stdio(false);
  read(n), read(m);
  for (int i = 1; i <= n; ++i) read(a[i]), c[i] = a[i] * 2 <= m, a[i] = abs(a[i] * 2 - m);
  read(q);
  for (int i = 1; i <= q; ++i) {
    read(qs[i].o);
    if (qs[i].o == 1) read(qs[i].x), read(qs[i].y), c[qs[i].x] = qs[i].y * 2 <= m, a[qs[i].x] = abs(qs[i].y * 2 - m);
    else if (qs[i].o == 2) read(qs[i].x);
  }
  for (int i = 1; i <= n + q; ++i)
    if (a[i] > 0 || c[i]) b[++cn] = a[i];
  sort(b + 1, b + cn + 1);
  cn = unique(b + 1, b + cn + 1) - b - 1;
  for (int i = 1; i <= n + q; ++i) {
    if (a[i] > 0 || c[i]) a[i] = lower_bound(b + 1, b + cn + 1, a[i]) - b;
  }
  for (int i = 1; i <= n; ++i) upd(i, 1);
  for (int i = 1; i <= q; ++i) {
    if (qs[i].o == 1) upd(qs[i].x, 1);
    else if (qs[i].o == 2) upd(qs[i].x, -1);
    else cout << sgt[1].s + sgt[1].ls / 2 << '\n';
  }
  return 0;
}
```
