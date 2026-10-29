---
title: "记录 续 续 续"
date: 2025-11-05T16:09:57+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/fl5ccfv8"
luogu_id: "fl5ccfv8"
---

[记录 续 续](https://www.luogu.com.cn/article/0zt6kmcr) 又炸了。

### *P14380
写成一坨了，有空再来重构。

首先考虑这个问题等价于求 $[l_0, r_0]$ 的个数满足 $l \le l_0 \le r_0 \le r$ 的 $f(l, r) = f(l_0, r_0)$。

那么容易发现这等价于 $l_0, r_0$ 均为叶子。

考虑维护 $rht_i, lft_i$ 表示以 $i$ 为左右端点最远可以扩展的点。

那么我们可以发现，以 $i$ 为根，这个区间中的所有点都在一个子树内，于是我们把每个子树内最小最大的编号取出来，所有子树的次大次小即为所求。

于是一个区间 $[l, r]$ 满足条件等价于 $lft_r \le l \le r \le rht_l$。

考虑扫描线，当前扫描到 $i$，维护 $f_l$ 表示 $r \le i$ 的区间数量。

每次只需考虑有哪些右端点为 $i$ 的合法区间即可，即 $i \le rht_l$，这个可以在扫描线同时维护，于是用一颗线段树维护这个东西和 $f$，每次将 $f$ 加上这个，第一次知道可以用线段树维护。

$O(n \log n)$

写了依托，开了 $3$ 个线段树。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 5e5 + 9;
int n, q, dfn[N], idx, id[N], sz[N], lft[N], rht[N], sgt[N << 2], ans[N];
vector<int> es[N];
int dfs(int x, int ff) {
  id[dfn[x] = ++idx] = x;
  for (int y : es[x])
    if (y ^ ff) sz[x] += dfs(y, x);
  return ++sz[x];
}
void build(int u, int l, int r) {
  if (l == r) return sgt[u] = id[l], void();
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
  sgt[u] = min(sgt[u << 1], sgt[u << 1 | 1]);
}
void build1(int u, int l, int r) {
  if (l == r) return sgt[u] = id[l], void();
  int m = (l + r) >> 1;
  build1(u << 1, l, m), build1(u << 1 | 1, m + 1, r);
  sgt[u] = max(sgt[u << 1], sgt[u << 1 | 1]);
}
int query(int u, int l, int r, int x, int y) {
  if (x > y) return n + 1;
  if (x <= l && r <= y) return sgt[u];
  int m = (l + r) >> 1, res = n + 1;
  if (m >= x) cmin(res, query(u << 1, l, m, x, y));
  if (m < y) cmin(res, query(u << 1 | 1, m + 1, r, x, y));
  return res;
}
int query1(int u, int l, int r, int x, int y) {
  if (x > y) return 0;
  if (x <= l && r <= y) return sgt[u];
  int m = (l + r) >> 1, res = 0;
  if (m >= x) cmax(res, query1(u << 1, l, m, x, y));
  if (m < y) cmax(res, query1(u << 1 | 1, m + 1, r, x, y));
  return res;
}
void update1(int u, int l, int r, int x, int y) {
  if (l == r) return sgt[u] = y, void();
  int m = (l + r) >> 1;
  if (m >= x) update1(u << 1, l, m, x, y);
  else update1(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = max(sgt[u << 1], sgt[u << 1 | 1]);
}
void update(int u, int l, int r, int x, int y) {
  if (l == r) return sgt[u] = y, void();
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x, y);
  else update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = min(sgt[u << 1], sgt[u << 1 | 1]);
}
struct info {
  int f, flg;
  info operator+(const info &x) const {
    return {f + x.f, x.flg + flg};
  }
} sgt1[N << 2];
int tg[N << 2];
void build2(int u, int l, int r) {
  if (l == r) return sgt1[u] = {0, 0}, void();
  int m = (l + r) >> 1;
  build2(u << 1, l, m), build2(u << 1 | 1, m + 1, r);
  sgt1[u] = sgt1[u << 1] + sgt1[u << 1 | 1];
}
void apply(int u, int x) {
  tg[u] += x;
  sgt1[u].f += x * sgt1[u].flg;
}
void down(int u) {
  if (tg[u]) {
    apply(u << 1, tg[u]), apply(u << 1 | 1, tg[u]);
    tg[u] = 0;
  }
}
void update2(int u, int l, int r, int x, int y) {
  if (x <= l && r <= y) return apply(u, 1);
  int m = (l + r) >> 1;
  down(u);
  if (m >= x) update2(u << 1, l, m, x, y);
  if (m < y) update2(u << 1 | 1, m + 1, r, x, y);
  sgt1[u] = sgt1[u << 1] + sgt1[u << 1 | 1];
}
void update3(int u, int l, int r, int x, int y) {
  if (l == r) return sgt1[u].flg = y, void();
  int m = (l + r) >> 1;
  down(u);
  if (m >= x) update3(u << 1, l, m, x, y);
  else update3(u << 1 | 1, m + 1, r, x, y);
  sgt1[u] = sgt1[u << 1] + sgt1[u << 1 | 1];
}
info query2(int u, int l, int r, int x, int y) {
  if (x <= l && r <= y) return sgt1[u];
  int m = (l + r) >> 1;
  down(u);
  if (m >= x && m < y) return query2(u << 1, l, m, x, y) + query2(u << 1 | 1, m + 1, r, x, y);
  else if (m >= x) return query2(u << 1, l, m, x, y);
  else return query2(u << 1 | 1, m + 1, r, x, y);
}
vector<int> vc[N];
vector<pair<int, int>> qry[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  for (int i = 1, x, y; i < n; ++i) {
    cin >> x >> y;
    es[x].push_back(y), es[y].push_back(x);
  }
  dfs(1, 0);
  build(1, 1, n);
  for (int i = 1; i <= n; ++i) {
    vector<int> vec;
    update(1, 1, n, dfn[i], n + 1);
    for (int j : es[i]) {
      if (dfn[j] < dfn[i]) continue;
      int t = query(1, 1, n, dfn[j], dfn[j] + sz[j] - 1);
      vec.push_back(t);
      // cerr << j << ' ' << t << '\n';
    }
    int t = min(query(1, 1, n, 1, dfn[i] - 1), query(1, 1, n, dfn[i] + sz[i], n));
    // cerr << t << '\n';
    vec.push_back(t);
    sort(vec.begin(), vec.end());
    // cerr << vec[1] << ' ' << vec[0] << '\n';
    if (vec.size() < 2) rht[i] = n;
    else rht[i] = vec[1] - 1;
  }
  build1(1, 1, n);
  for (int i = n; i >= 1; --i) {
    vector<int> vec;
    update1(1, 1, n, dfn[i], 0);
    for (int j : es[i]) {
      if (dfn[j] < dfn[i]) continue;
      int t = query1(1, 1, n, dfn[j], dfn[j] + sz[j] - 1);
      vec.push_back(t);
    }
    int t = max(query1(1, 1, n, 1, dfn[i] - 1), query1(1, 1, n, dfn[i] + sz[i], n));
    vec.push_back(t);
    sort(vec.begin(), vec.end(), greater<int>());
    // cerr << vec[0] << '\n';
    if (vec.size() < 2) lft[i] = 1;
    else lft[i] = vec[1] + 1;
  }
  // for (int i = 1; i <= n; ++i) cerr << lft[i] << ' ' << rht[i] << '\n';
  for (int i = 1; i <= n; ++i) vc[rht[i]].push_back(i);
  for (int i = 1; i <= q; ++i) {
    int l, r;
    cin >> l >> r;
    qry[r].emplace_back(l, i);
  }
  build2(1, 1, n);
  for (int i = 1; i <= n; ++i) {
    update3(1, 1, n, i, 1);
    update2(1, 1, n, lft[i], i);
    for (auto [j,  k] : qry[i]) ans[k] = query2(1, 1, n, j, i).f;
    for (int j : vc[i]) update3(1, 1, n, j, 0);
  }
  for (int i = 1; i <= q; ++i) cout << ans[i] << '\n';
}

/*


i, j
f[i]


lft[i] <= j, i <= rht[j] 

lft[i] <= j <= i <= rht[j]

i <= rht[j]

*/
```
----------------
2025.11.8

### P9378
考虑贪心，显然越小的优先选。

于是我们枚举 $1\le i \le n$，考虑把 $i$ 加入能否满足条件。

考虑如何判断一个集合是否可以，首先枚举每条宇宙射线，那么我们按顺序去枚举每个 $p_{i, j}$。如果已经被选掉了就跳过；如果没有被选并且不在集合中，我们直接摧毁然后 break，如果在那么一定要在 $a_i$ 前完成，所以把所有要提前完成的存一下，如果数量多于 $a_i$ 那么就不合法。

$O(n^3)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 609;
int n, m, a[N], p[N][N];
bool vst[N], pk[N];
vector<int> check() {
  vector<int> res;
  memset(vst, 0, sizeof vst);
  for (int i = 1; i <= m; ++i) {
    for (int j = 1; j <= n; ++j) {
      if (vst[p[i][j]]) continue;
      vst[p[i][j]] = 1;
      if (!pk[p[i][j]]) break;
      res.push_back(p[i][j]);
    }
    if (res.size() > a[i]) return {};
  }
  for (int i = 1; i <= n; ++i)
    if (pk[i] && !vst[i]) res.push_back(i);
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= m; ++i) cin >> a[i];
  for (int i = 1; i <= m; ++i) {
    for (int j = 1; j <= n; ++j) cin >> p[i][j];
  }
  for (int i = 1; i <= n; ++i) {
    pk[i] = 1;
    vector<int> res = check();
    if (res.empty()) {
      pk[i] = 0;
      continue;
    }
    if (res.size() == n - m) {
      for (int j : res) cout << j << ' ';
      return 0;
    }
  }
}
```

### AT_abc254_h
不会贪心。

操作一等价于对 $b$ 做操作二，要求是偶数。

于是直接取 $a, b$ 最大的两个，相同就判掉，不同就把大的做操作二。

如果做不了就是无解。

$O(n\log n)$

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
int n, a[N], b[N], res;
priority_queue<int> q1, q2;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i], q1.push(a[i]);
  for (int i = 1; i <= n; ++i) cin >> b[i], q2.push(b[i]);
  while (!q1.empty() && !q2.empty()) {
    int x = q1.top(), y = q2.top();
    q1.pop(), q2.pop();
    if (x == y) continue;
    if (x > y) q1.push(x / 2), q2.push(y);
    else {
      if (y & 1) return cout << -1, 0;
      q1.push(x), q2.push(y / 2);
    }
    ++res;
  }
  cout << res;
}
```

### *P7519
首先由于 $b_i \le b_{i + 1}$，对于一个排名序列 $p_i$，如果 $a_{p_i} < a_{p_{i + 1}}$ 那么 $b_i = b_{i + 1}$；如果 $a_{p_i} = a_{p_{i + 1}}$ 那么 $b_{i + 1} = b_i + [p_i < p_{i + 1}]$，因为编号小的排在前面；如果 $a_{p_i} > a_{p_{i + 1}}$，那么 $b_{i + 1} = b_{i} + a_{p_{i + 1}} - a_{p_i}$。

综上 $b_i = b_{i - 1} + \max(0, a_{p_i} - a_{p_{i - 1}} + [p_{i - 1} < p_i])$。

直接枚举 $p$，然后计算 $b$，如果 $\sum b_i \le m$ 那么就可以。

暴力 $O(n!n)$。

显然这种可以状压 dp，但是由于贡献与 $b_{i - 1}$ 有关所以还要枚举，复杂度至少是 $O(2^n m^2)$。

考虑把 $\sum b_i$ 转化为只和 $a_{p_i}, a_{p_{i - 1}}$ 有关的，注意到是前缀和形式，于是 $\sum b_i = \max(0, a_{p_i} - a_{p_{i - 1}} + [p_{i - 1} < p_i]) \times (n - i + 1)$。

这样就可以 dp，令 $f_{i, j, k}$ 表示已经选掉了 $i$ 集合中的点，上一个是 $j$，已经过了 $k$ 题。

那么每次 $n^2$ 枚举即可计算出过题的贡献，$O(2^nn^2m)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 13;
int n, m, a[N], p[N], mx, f[1 << 13][13][509];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 0; i < n; ++i) cin >> a[i], cmax(mx, a[i]) && (p[0] = i, 0);
  // do {
  //   int k = 0;
  //   for (int i = 1; i <= n; ++i) {
  //     k += max(a[p[i - 1]] - a[p[i]] + (p[i - 1] < p[i]), 0) * (n - i + 1);
  //     if (k > m) break;
  //   }
  //   if (k <= m) {
  //     // for (int i = 1; i <= n; ++i) cerr << p[i] << ' ';
  //     // cerr << '\n';
  //     ++ans;
  //   }
  // } while (next_permutation(p + 1, p + n + 1));
  f[0][p[0]][0] = 1;
  for (int i = 0; i < 1 << n; ++i) {
    int pc = __builtin_popcount(i);
    for (int j = 0; j < n; ++j) {
      if (i > 0 && (i >> j & 1 ^ 1)) continue;
      for (int k = 0; k <= m; ++k) {
        for (int l = 0; l < n; ++l) {
          if (i >> l & 1) continue;
          int t = max(a[j] - a[l] + (j < l), 0ll) * (n - pc);
          if (k + t > m) continue;
          f[i ^ 1 << l][l][k + t] += f[i][j][k];
        }
      }
    }
  }
  int ans = 0;
  for (int i = 0; i < n; ++i)
    for (int j = 0; j <= m; ++j) ans += f[(1 << n) - 1][i][j];
  cout << ans;
}
```

------------
2025.11.07
### P5749
贪心还在发力。

首先每对鞋子都是相邻匹配，于是开 $2n$ 个 vector，存一下位置，然后每次找最近的。用树状数组维护每个点上是否已经被移动掉了。

$O(n \log n)$，一定不要先对 $n$ 乘 $2$！！！

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e5 + 9;
int n, a[N], c[N], ans, vst[N];
vector<int> q[N];
void update(int x, int y) { for (; x <= n * 2; x += x & -x) c[x] += y; }
int query(int x, int r = 0) { for (; x > 0; x -= x & -x) r += c[x]; return r; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= 2 * n; ++i) cin >> a[i];
  for (int i = 2 * n; i >= 1; --i) q[a[i] + n].push_back(i), update(i, 1);
  for (int i = 1; i <= n * 2; ++i) {
    if (vst[i]) continue;
    while (q[n - a[i]].back() < i) q[n - a[i]].pop_back();
    int j = q[n - a[i]].back();
    q[n - a[i]].pop_back();
    vst[i] = vst[j] = 1;
    ans += query(j) - query(i) - (a[i] < 0);
    update(j, -1);
  }
  cout << ans;
}
```

### *P7482
$(max, +)$ 矩阵对于加法没有分配律！！！！！

一开始想了个线段树，大概是维护 $f_l$ 表示以 $l$ 为左端点的区间之和，然后用矩阵维护。

但是广义矩阵没有分配律，所以假了。

接下来说正解。

所有子区间，显然还可以分治（为什么没想到？）。

考虑跨过 $mid$ 的部分如何计算。

显然可以通过 dp，求出 $f_{0/1, i}$（$l \le i \le mid$）表示 $i\sim mid$ 这段选/不选 $mid$ 的最大值，$g_{0/1, j}$（$mid < j \le r$）同理。

于是可以容易得到 $f(i, j) = \max(f_{0, i} + g_{0, j}, f_{0, i} + g_{1, j}, f_{1, i} + g_{0, j}) = \max(f_{0, i} + \max(g_{0, j}, g_{1, j}), f_{1, i} + g_{0, j})$。

令 $h_j = \max(g_{0, j}, g_{1, j})$，那么 $f(i, j) = \max(f_{0, i} + h_j, f_{1, i} + g_{0, j})$。

分类讨论一下：
- $f_{0, i} + h_j > f_{1, i} + g_{0, j} \Rightarrow f_{0, i} - f_{1, i} > g_{0, j} - h_j$，对于这些 $j$ 贡献为 $\sum h_j + f_{0, i}$。
- $f_{0, i} - f_{1, i} \le g_{0, j} - h_j$，贡献为 $\sum g_{0, j} + f_{1, i}$。
直接按 $f_{0, i} - f_{1, i}$ 和 $g_{0, j} - h_j$ 排序，然后枚举 $i$，双指针容易得出 $j$，前缀和一下即可计算贡献。

$O(n\log^2 n)$，跑得飞快。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T& x, const T& y) { if (x < y) { x = y; return true; } return false; }
template<class T> inline bool cmin(T& x, const T& y) { if (x > y) { x = y; return true; } return false; }
constexpr int N = 1e5 + 9, md = 1e9 + 7, inf = 0x3f3f3f3f3f3f;
int n, a[N], ans, f[N][2], f0[N], f1[N], g0[N], g1[N], h[N], p[N], q[N], sh[N], sg[N];
void dfs(int l, int r) {
  if (l == r) return ans += a[l], void();
  int m = (l + r) >> 1;
  dfs(l, m), dfs(m + 1, r);
  for (int i = m + 1; i <= r; ++i) {
    f[i][0] = max(f[i - 1][0], f[i - 1][1]);
    f[i][1] = f[i - 1][0] + a[i];
    if (i == m + 1) f[i][1] = a[i], f[i][0] = -inf;
    g1[i] = max(f[i][0], f[i][1]);
  }
  for (int i = m + 1; i <= r; ++i) {
    f[i][0] = max(f[i - 1][0], f[i - 1][1]);
    f[i][1] = f[i - 1][0] + a[i];
    if (i == m + 1) f[i][0] = 0, f[i][1] = -inf;
    g0[i] = max(f[i][0], f[i][1]);
    h[i] = max(g0[i], g1[i]);
  }
  for (int i = m; i >= l; --i) {
    f[i][0] = max(f[i + 1][0], f[i + 1][1]);
    f[i][1] = f[i + 1][0] + a[i];
    if (i == m) f[i][1] = a[i], f[i][0] = -inf;
    f1[i] = max(f[i][0], f[i][1]);
  }
  for (int i = m; i >= l; --i) {
    f[i][0] = max(f[i + 1][0], f[i + 1][1]);
    f[i][1] = f[i + 1][0] + a[i];
    if (i == m) f[i][0] = 0, f[i][1] = -inf;
    f0[i] = max(f[i][0], f[i][1]);
  }
  iota(p + m + 1, p + r + 1, m + 1);
  sort(p + m + 1, p + r + 1, [&](int x, int y) -> bool { return g0[x] - h[x] < g0[y] - h[y]; });
  iota(q + l, q + m + 1, l);
  sort(q + l, q + m + 1, [&](int x, int y) -> bool { return f0[x] - f1[x] < f0[y] - f1[y]; });
  sh[m] = sg[m] = 0;
  for (int i = m + 1; i <= r; ++i) sh[i] = (sh[i - 1] + h[p[i]]) % md, sg[i] = (sg[i - 1] + g0[p[i]]) % md;
  for (int i = l, j = m; i <= m; ++i) {
    while (j < r && f0[q[i]] - f1[q[i]] > g0[p[j + 1]] - h[p[j + 1]]) ++j;
    (ans += f0[q[i]] * (j - m) + sh[j]) %= md;
    (ans += f1[q[i]] * (r - j) + sg[r] - sg[j] + md) %= md;
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  dfs(1, n);
  cout << ans;
}
```
---------------
2025.11.08
### P6406

给定 $a$，求 $\sum_{i = 1}^n \sum_{j = i}^n (j - i + 1) \min(a_i, \cdots, a_j) \max(a_i, \cdots, a_j)$。

显然扫描线 $i$，维护 $f_l$ 表示 $r = i$ 的区间的值。

每次考虑修改。


$f(i, j) = (j - i + 1)\min\max = j\min\max - (i - 1)\min\max$

于是维护两个 $f, g$ 表示 $\min\max$ 和 $(i - 1)\min\max$。

每次新加一个点 $i$，会对 $1\sim i$ 的所有 $f, g$ 产生影响。

预处理出 $i$ 是 $\min, \max$ 的段，然后这段是需要修改的。

于是我们要维护 $a_ib_i$ 的和，支持区间将 $a, b$ 赋值。

用线段树维护 $\sum a_i, \sum b_i, \sum a_ib_i$ 即可。

$O(n\log n)$。

64 M有点卡空间。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 5e5 + 9, md = 1e9;
int n, a[N], stk[N], tp, lft[N][2], ans;
struct node {
  int sa, sb, s, tga, tgb, sc;
  node() { sa = sb = s = tga = tgb = sc = 0; }
} tr[N << 2];
void build(int u, int l, int r, int t) {
  tr[u] = node();
  if (l == r) return tr[u].sc = t ? l : 1, void();
  int m = (l + r) >> 1;
  build(u << 1, l, m, t), build(u << 1 | 1, m + 1, r, t);
  tr[u].sc = (tr[u << 1].sc + tr[u << 1 | 1].sc) % md;
}
void apply(int u, int l, int r, int a, int b) {
  tr[u].tga = a, tr[u].tgb = b;
  if (tr[u].tga) tr[u].sa = 1ll * tr[u].sc * a % md, tr[u].s = 1ll * a * tr[u].sb % md;
  if (tr[u].tgb) tr[u].sb = 1ll * tr[u].sc * b % md, tr[u].s = 1ll * b * tr[u].sa % md;
}
void down(int u, int l, int r) {
  int m = (l + r) >> 1;
  if (tr[u].tga || tr[u].tgb) apply(u << 1, l, m, tr[u].tga, tr[u].tgb), apply(u << 1 | 1, m + 1, r, tr[u].tga, tr[u].tgb);
  tr[u].tga = tr[u].tgb = 0;
}
void update(int u, int l, int r, int x, int y, int a, int b) {
  if (x <= l && r <= y) return apply(u, l, r, a, b);
  int m = (l + r) >> 1;
  down(u, l, r);
  if (m >= x) update(u << 1, l, m, x, y, a, b);
  if (m < y) update(u << 1 | 1, m + 1, r, x, y, a, b);
  tr[u].s = (tr[u << 1].s + tr[u << 1 | 1].s) % md;
  tr[u].sa = (tr[u << 1].sa + tr[u << 1 | 1].sa) % md;
  tr[u].sb = (tr[u << 1].sb + tr[u << 1 | 1].sb) % md;
  tr[u].sc = (tr[u << 1].sc + tr[u << 1 | 1].sc) % md;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i <= n; ++i) {
    while (tp && a[stk[tp]] > a[i]) tp--;
    lft[i][0] = stk[tp] + 1;
    stk[++tp] = i;
  }
  tp = 0;
  for (int i = 1; i <= n; ++i) {
    while (tp && a[stk[tp]] < a[i]) tp--;
    lft[i][1] = stk[tp] + 1;
    stk[++tp] = i;
  }
  build(1, 1, n, 0);
  for (int i = 1; i <= n; ++i) {
    update(1, 1, n, lft[i][0], i, a[i], 0);
    update(1, 1, n, lft[i][1], i, 0, a[i]);
    ans = (ans + 1ll * (i + 1) * tr[1].s) % md;
  }
  build(1, 1, n, 1);
  for (int i = 1; i <= n; ++i) {
    update(1, 1, n, lft[i][0], i, a[i], 0);
    update(1, 1, n, lft[i][1], i, 0, a[i]);
    ans = (ans + md - tr[1].s) % md;
  }
  cout << ans;
}
```
--------------------------------------------------------
2025.11.09

### P6563
每次询问一个点 $i$，相当与把问题分为了两部分。

那么记 $f(l, r)$ 表示如果电线在这个区间至少要花多少钱。

那么对于选的一个点 $l \le k \le r$，我们要花费 $a_k + \max(f(l, k), f(k + 1, r))$。

所以 $f(l, r) = \min\limits_{l \le k \le r} a_k + \max(f(l, k), f(k + 1, r))$，直接做 $O(n^3)$，先写。

OK ，没问题。

考虑优化。

$f(l, r) = \min a_k + \max(f(l, k), f(k + 1, r))$。

考虑分讨？

决策单调性？

打印一手决策点看看。

发现对于 $l, r$ 的决策点 $p(l, r)$ 满足 $p(l, r) \le p(l + 1, r)$。

也就是决策点对于 $r$ 是单调的。

显然 $f(l, k) \le f(l, k + 1), f(k, r) \le f(k + 1, r)$。

$a_i \le a_{i + 1}$ 有什么用？

假设存在一个 $m$，使得 $f(l, m) < f(m + 1, r), f(l, m + 1) \ge f(m + 2, r)$。

那么对于 $l\le k \le m$，$f(l, r) = \min a_k + f(k + 1, r)$。

由于 $a$ 单调不降，$f(k + 1, r)$ 单调不增。

所以没单调性？

$m < k \le r$，$f(l, r) = \min a_k + f(l, k)$。

$a, f(l, k)$ 都是单调不降的。

所以这部分有单调性，所以 $l \le k \le m + 1$。

由于 $f(k + 1, r) \le f(k + 1, r + 1)$，所以对于每个 $l$，我们令 $q_l = m$，则随着 $r$ 增大，$q_l$ 也增大。

于是我们可以快速求出 $m < k \le r$ 的答案。

那么 $l \le k \le m$ 的呢。

由于 $f(l, m) \le f(l - 1, m)$，所以 $q_{l - 1}\le q_l$。

但是是从大到小枚举 $l$，所以 $m$ 是单调不增的。

那么我们要求的是 $\min\limits_{l \le k \le m} a_k + f(l, k)$。

每次询问的区间左右端点都是单调的，所以直接用单调队列优化。

$O(n^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 7109, inf = 0x3f3f3f3f3f3f3f3f;
int n, a[N], f[N][N], hd, tl, p[N], q[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    a[0] = a[n + 1] = a[n + 2] = inf;
    for (int i = 0; i <= n + 2; ++i)
      for (int j = 0; j <= n + 2; ++j) f[i][j] = inf;
    for (int i = 1; i <= n; ++i) q[i] = i, f[i][i] = 0;
    for (int r = 1; r <= n; ++r) {
      p[hd = tl = 1] = r;
      for (int l = r - 1; l >= 1; --l) {
        while (q[l] < r && f[l][q[l] + 1] < f[q[l] + 2][r]) {
          ++q[l];
          // cmin(p[l], a[q[l]] + f[q[l] + 1][r]);
          // while (tp[l] && a[stk[l][tp[l]]] + f[stk[l][tp[l]] + 1][r] > a[q[l]] + f[q[l] + 1][r])
          //   --tp[l];
          // stk[l][++tp[l]] = q[l];
        }
        // cerr << q[l] << ' ';
        f[l][r] = a[q[l] + 1] + f[l][q[l] + 1];
        while (hd <= tl && p[hd] > q[l]) ++hd;
        while (hd <= tl && a[p[tl]] + f[p[tl] + 1][r] > a[l] + f[l + 1][r]) --tl;
        p[++tl] = l;
        cmin(f[l][r], a[p[hd]] + f[p[hd] + 1][r]);
        // for (int k = l; k <= q[l]; ++k) {
        //   cmin(f[l][r], a[k] + f[k + 1][r]);
        // }
      }
      // cerr << '\n';
    }
    cout << f[1][n] << '\n';
  }
}
```

---------
2025.11.10

### CF1175E
倍增维护每个用 $j$ 个区间包含 $i$ 最远可以覆盖到哪。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 5e5 + 9;
int n, m, rht[N][20];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i) {
    int l, r;
    cin >> l >> r;
    cmax(rht[l][0], r);
  }
  for (int i = 1; i < N; ++i) cmax(rht[i][0], rht[i - 1][0]);
  for (int i = 1; i < 20; ++i)
    for (int j = 0; j < N; ++j)
      rht[j][i] = rht[rht[j][i - 1]][i - 1];
  while (m--) {
    int x, y;
    cin >> x >> y;
    int res = 0;
    for (int i = 19; i >= 0; --i) {
      if (rht[x][i] >= y) continue;
      res += 1 << i, x = rht[x][i];
    }
    if (res > N) cout << -1 << '\n';
    else cout << res + 1 << '\n';
  }
}
```

-------------
2025.11.11
### P10365
很厉害 %%%%

直接对于每个区间，求出他向上可以到的最左最右端，然后差分一下，这样就可以用倍增维护一个点向上跳一段可以向左包含的区间个数，然后直接计算即可，$O(n\log n)$，非常好写（（

不想写线段树，写了 odt。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template <class T> inline bool cmax(T& x, const T& y) { if (x < y) { x = y; return true; } return false; }
template <class T> inline bool cmin(T& x, const T& y) { if (x > y) { x = y; return true; } return false; }
constexpr int N = 5e5 + 9, md = 1e9 + 7;
int n, inv[N], o[N], l[N], r[N], ans, top[N], L[N][20], R[N][20], sl[N][20], sr[N][20], c[N];
map<int, int> mp;
void update(int x, int y) {
  for (; x <= n + 1; x += x & -x) c[x] += y;
}
int query(int x, int r) { for (; x > 0; x -= x & -x) r += c[x]; return r; }
auto spl(int x) {
  auto it = prev(mp.upper_bound(x));
  return mp.insert(make_pair(x, it->second)).first;
}
void update(int x, int y, int z) {
  auto l = spl(x), r = spl(y + 1);
  while (l != r) l = mp.erase(l);
  mp[x] = z;
}
int query(int x) {
  auto it = prev(mp.upper_bound(x));
  return it->second;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> l[i] >> r[i], o[i] = top[i] = i;
  mp[0] = 0, mp[1] = 0, mp[2 * n + 1] = 0;
  inv[1] = 1;
  for (int i = 2; i <= n; ++i) inv[i] = md - md / i * inv[md % i] % md;
  for (int i = 1; i <= n; ++i) {
    L[i][0] = query(l[i]), R[i][0] = query(r[i]);
    update(l[i], r[i], i);
  }
  for (int i = n; i >= 1; --i) {
    cmax(top[L[i][0]], top[i]);
    cmax(top[R[i][0]], top[i]);
  }
  update(1, 2 * n, n + 1);
  for (int i = n; i >= 1; --i) {
    L[i][0] = query(l[i]), R[i][0] = query(r[i]);
    update(l[i], r[i], i);
  }
  sort(o + 1, o + n + 1, [&](int x, int y) -> bool { return l[x] < l[y]; });
  for (int i = 1; i <= n; ++i) {
    update(o[i], 1);
    sl[o[i]][0] = query(L[o[i]][0] - 1, 0) - query(o[i], 0);
  }
  sort(o + 1, o + n + 1, [&](int x, int y) -> bool { return r[x] < r[y]; });
  memset(c, 0, sizeof c);
  for (int i = 1; i <= n; ++i) {
    update(o[i], 1);
    sr[o[i]][0] = query(R[o[i]][0], 0) - query(o[i] - 1, 0);
  }
  for (int i = 1; i < 20; ++i) {
    for (int j = 1; j <= n; ++j) {
      L[j][i] = L[L[j][i - 1]][i - 1];
      R[j][i] = R[R[j][i - 1]][i - 1];
      sl[j][i] = sl[j][i - 1] + sl[L[j][i - 1]][i - 1];
      sr[j][i] = sr[j][i - 1] + sr[R[j][i - 1]][i - 1];
    }
  }
  for (int i = 1; i <= n; ++i) {
    int cnt = 0, x = i;
    for (int j = 19; j >= 0; --j) {
      if (R[x][j] == 0 || R[x][j] > L[top[i]][0]) continue;
      cnt += sr[x][j], x = R[x][j];
    }
    x = i;
    for (int j = 19; j >= 0; --j) {
      if (L[x][j] == 0 || L[x][j] > L[top[i]][0]) continue;
      cnt -= sl[x][j], x = L[x][j];
    }
    // cerr << x << ' ' << cnt << '\n';
    (ans += inv[cnt]) %= md;
  }
  cout << ans;
}
```

-----------
2025.11.12

### P14426
一开始想到扫描线上就死了。

考虑 $O(n^2)$ 暴力，可以枚举两个点，考虑分治优化。

对于跨过 $mid$ 的两点 $a, b$，我们考虑枚举 $b$，如何快速计算合法的 $a$ 的个数？

首先，由于矩形内没有其他点，所以我们按 $y$ 扫描线，容易发现如果在 $mid$ 左侧有两个点 $p, q$ 满足 $x_p < x_q, y_p < y_q$，那么 $p$ 的矩形一定会包含 $q$，必然不合法。

而对于 $mid$ 右侧同理，如果存在这样的 $q$，那么左下角的点 $lp$ 必须满足 $y_q < y_{lp} < y_p$，可以用单调栈维护左右侧，快速得到 $q$，然后在左侧单调栈上二分即可得到 $lp$ 个数。

也可以用数据结构维护，直接把必定不合法的点覆盖为 $0$，其余为 $1$ 即可。

貌似还可以直接单侧递归线段树，大概就是不分治，扫描线然后维护一个区间上升子序列长度，单侧递归合并。

场上想到了维护上升子序列的但是不会。

$O(n\log^2 n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 4e5 + 9;
int n, b[N], cn, ans, stkl[N], tpl, stkr[N], tpr;
struct pt {
  int x, y;
  bool operator<(const pt &nx) const {
    return x < nx.x;
  }
} a[N];
void dfs(int l, int r) {
  if (l == r) return ;
  int m = (l + r) >> 1;
  dfs(l, m), dfs(m + 1, r);
  tpl = tpr = 0;
  for (int i = m + 1, j = l - 1; i <= r; ++i) {
    while (j < m && a[j + 1].y < a[i].y) {
      while (tpl && a[stkl[tpl]].x < a[j + 1].x) --tpl;
      stkl[++tpl] = ++j;
    }
    while (tpr && a[stkr[tpr]].x > a[i].x) --tpr;
    int l = 0, r = tpl;
    while (l < r) {
      int mid = (l + r + 1) >> 1;
      if (a[stkl[mid]].y < a[stkr[tpr]].y) l = mid;
      else r = mid - 1;
    }
    ans += tpl - l;
    stkr[++tpr] = i;
  }
  sort(a + l, a + r + 1, [&](auto ls, auto rs) -> bool {
    return ls.y < rs.y;
  });
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> a[i].x >> a[i].y;
    b[i] = a[i].x, b[i + n] = a[i].y;
  }
  sort(b + 1, b + 2 * n + 1);
  cn = unique(b + 1, b + 2 * n + 1) - b - 1;
  for (int i = 1; i <= n; ++i) {
    a[i].x = lower_bound(b + 1, b + cn + 1, a[i].x) - b;
    a[i].y = lower_bound(b + 1, b + cn + 1, a[i].y) - b;
  }
  sort(a + 1, a + n + 1);
  dfs(1, n);
  cout << ans;
}
```

单侧递归线段树确实可做，考虑对 $x$ 做扫描线，然后相当于对于 $y$ 做 [P4198 楼房重建](https://www.luogu.com.cn/problem/P4198)。

$O(n\log^2 n)$，常数比分治大，但是会决策单调性就没有思维难度了。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 4e5 + 9;
int n, b[N], cn, ans, f[N], sgt[N << 2], hi[N << 2];
struct pt {
  int x, y;
  bool operator<(const pt &nx) const {
    return x < nx.x;
  }
} a[N];
int up(int u, int l, int r, int mx = 0) {
  if (hi[u] <= mx) return 0;
  if (l == r) return 1;
  int m = (l + r) >> 1;
  if (hi[u << 1] <= mx) return up(u << 1 | 1, m + 1, r, mx);
  else return up(u << 1, l, m, mx) + sgt[u] - sgt[u << 1];
}
void update(int u, int l, int r, int x, int y) {
  if (l == r) return hi[u] = y, sgt[u] = 1, void();
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x, y);
  else update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = sgt[u << 1] + up(u << 1 | 1, m + 1, r, hi[u << 1]);
  hi[u] = max(hi[u << 1], hi[u << 1 | 1]);
}
pair<int, int> query(int u, int l, int r, int x) {
  if (x <= l) return {sgt[u], hi[u]};
  int m = (l + r) >> 1;
  if (m >= x) {
    auto [xa, xb] = query(u << 1, l, m, x);
    return {xa + up(u << 1 | 1, m + 1, r, xb), max(xb, hi[u << 1 | 1])};
    // return query(u << 1, l, m, x) + up(u << 1 | 1, m + 1, r, hi[u << 1]);
  }
  else return query(u << 1 | 1, m + 1, r, x);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> a[i].x >> a[i].y;
    b[i] = a[i].x, b[i + n] = a[i].y;
  }
  sort(b + 1, b + n + 1);
  sort(b + n + 1, b + 2 * n + 1);
  for (int i = 1; i <= n; ++i) {
    a[i].x = lower_bound(b + 1, b + n + 1, a[i].x) - b;
    a[i].y = lower_bound(b + n + 1, b + n * 2 + 1, a[i].y) - b - n;
  }
  sort(a + 1, a + n + 1);
  for (int i = n; i >= 1; --i) {
    int res = query(1, 1, n, a[i].y).first;
    // for (int j = a[i].y, lst = 0; j <= n; ++j) {
    //   if (f[j] > lst) lst = f[j], ++res;
    // }
    ans += res;
    // cerr << n - a[i].x + 1 << ' ' << a[i].y << ' ' << res << '\n';
    f[a[i].y] = n - a[i].x + 1;
    update(1, 1, n, a[i].y, f[a[i].y]);
  }
  cout << ans;
}
```


### P9732
感觉不难啊。

首先记 $f_r = l$ 表示 $r$ 为右端点时答案最大的左端点位置。

赛时暴力打表发现 $f_{i - 1} \le f_i$，但是值不单调，不能双指针，于是直接决策单调性分治。

由于没有想到线段树，所以直接做是 $O(n^2\log n)$，考虑决策单调性分治计算贡献的 trick，容易做到 $O(n\log^2 n)$。

然后考虑第二问，赛时没细想，写了个 $O(\frac{n^2}w)$。

考虑两个区间 $l_1 \le l_2 \le r_2 \le r_1$，那么 $l_1, r_2$ 和 $l_2, r_1$ 同样是合法区间。

容易发现我们只要保留 $[l_1, r_2], [l_2, r_2], [l_2, r_1]$ 三个区间即可。

于是对于所有右端点，合法区间的左端点都是单调的，也就可以用类双指针的做法把每个区间找出来，然后 chkmin 一下区间第 $k$ 大，这是 $O(n\log n)$ 的。

$O(n\log^2 n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template <class T> bool cmax(T& x, const T& y) { if (x <= y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x >= y) return x = y, true; return false; }
constexpr int N = 5e5 + 9, inf = 0x3f3f3f3f3f3f3f3f;
int n, k, g[N], c[N], s[N], res, L, R, p[N];
multiset<int> q1, q2;
void adjust() {
  while (q1.size() > k) {
    res -= *q1.begin();
    q2.insert(*q1.begin());
    q1.erase(q1.begin());
  }
  while (q1.size() < k && !q2.empty()) {
    res += *prev(q2.end());
    q1.insert(*prev(q2.end()));
    q2.erase(prev(q2.end()));
  }
}
void add(int x) {
  q1.insert(s[x]);
  res += s[x] - c[x];
  adjust();
}
void del(int x) {
  auto it = q1.find(s[x]);
  res += c[x];
  if (it != q1.end()) return res -= *it, q1.erase(it), adjust();
  it = q2.find(s[x]);
  assert(it != q2.end());
  q2.erase(it);
}
int f(int l, int r) {
  while (r > R) add(++R);
  while (L > l) add(--L);
  while (r < R) del(R--);
  while (L < l) del(L++);
  return res;
}
void dfs(int l, int r, int pl, int pr) {
  if (l > r) return ;
  int m = (l + r) >> 1;
  g[m] = -0x3f3f3f3f3f3f3f3f;
  for (int i = pl; i <= m - k + 1 && i <= pr; ++i)
    if (cmax(g[m], f(i, m))) p[m] = i;
  dfs(l, m - 1, pl, p[m]);
  dfs(m + 1, r, p[m], pr);
}
int sgt[N << 2];
void build(int u, int l, int r) {
  sgt[u] = inf;
  if (l == r) return ;
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
}
void update(int u, int l, int r, int x, int y, int z) {
  if (x <= l && r <= y) return cmin(sgt[u], z), void();
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x, y, z);
  if (m < y) update(u << 1 | 1, m + 1, r, x, y, z);
}
void print(int u, int l, int r, int t = inf) {
  if (l == r) return cout << (min(t, sgt[u]) <= s[l]), void();
  int m = (l + r) >> 1;
  print(u << 1, l, m, min(t, sgt[u])), print(u << 1 | 1, m + 1, r, min(t, sgt[u]));
}
signed main() {
  // freopen("trade.in", "r", stdin);
  // freopen("trade.out", "w", stdout);
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> k;
  for (int i = 1; i <= n; ++i) cin >> c[i];
  for (int i = 1; i <= n; ++i) cin >> s[i];
  int ans = -0x3f3f3f3f3f3f3f3f;
  L = 1, R = 0;
  dfs(k, n, 1, n);
  cout << (ans = *max_element(g + k, g + n + 1)) << '\n';
  p[0] = 1;
  build(1, 1, n);
  for (int i = 1, lst = 0; i <= n; ++i) {
    if (g[i] != ans) continue;
    for (int j = p[lst]; j <= p[i]; ++j)
      if (f(j, i) == ans) {
        int K = *q1.begin();
        update(1, 1, n, j, i, K);
      }
    lst = i;
  }
  print(1, 1, n);
}
```

-----------
2025.11.13

### QOJ1944

序列上是容易的，可以做到 $O(n\log V + n)$。

考虑环怎么做，容易想到破环成链。

但是直接破环会漏情况，于是考虑钦定两个点 $1, n$ 不在一段，直接在原序列上 dp 即可。

这样会漏掉 $1, n$ 在一段的情况，考虑枚举 $1\sim i$ 前缀，对于每个前缀，我们可以枚举一个后缀使得两者按位与不为 $0$，那么我们可以从 $i + 1$ 开始 dp，然后求出中间一段的方案数即可。

由于只关心前缀按位与的值，所以可以存本质不同的值，容易发现只有 $O(\log V)$ 个，对于所有相同的前缀，这些位置都有可能作为端点，所以只要把这些位置 dp 值设为 $1$，然后暴力跑 dp 即可，$O(n\log V)$。

总时间复杂度是 $O(n\log V)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 2e5 + 9, inf = (1LL << 60) - 1, md = 998244353;
int n, a[N], f[N], g[N], cnt[60], pre[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  a[n + 1] = inf;
  for (int i = 1; i <= n; ++i) cin >> a[i], a[n + 1] &= a[i];
  if (a[n + 1]) {
    int pw = 1;
    for (int i = 1; i <= n; ++i) pw = pw * 2 % md;
    cout << (pw - n + md) % md;
    return 0;
  }
  memset(cnt, -1, sizeof cnt);
  for (int i = 1; i <= n; ++i) {  
    pre[i] = i;
    for (int j = 0; j < 60; ++j) {
      if (a[i] >> j & 1 ^ 1) cnt[j] = i - 1;
      cmin(pre[i], cnt[j]);
    }
  }
  f[0] = g[0] = 1;
  for (int j = 1; j <= n; ++j) {
    f[j] += (g[j - 1] - (pre[j] >= 0 ? g[pre[j]] : 0) + md) % md;
    g[j] = (g[j - 1] + f[j]) % md;
  }
  int ans = f[n];
  memset(f, 0, sizeof f);
  memset(g, 0, sizeof g);
  for (int i = 1, pr = inf, lst = 0; i <= n; ++i) {
    pr &= a[i];
    if (!pr) break;
    f[i] = 1;
    if (pr == (pr & a[i + 1])) continue;
    for (int j = 1; j <= n; ++j) {
      f[j] += (g[j - 1] - (pre[j] >= 0 ? g[pre[j]] : 0) + md) % md;
      g[j] = (g[j - 1] + f[j]) % md;
    }
    // cerr << lst + 1 << ' ' << i << ' ' << f[n] << '\n';
    for (int j = n, sf = inf; j >= 1; --j) {
      sf &= a[j];
      if (!sf) break;
      if (sf & pr) (ans += f[j - 1]) %= md;
    }
    lst = i;
    memset(f, 0, sizeof f);
    memset(g, 0, sizeof g);
  }
  cout << ans;
}
```

### CodeChef-YANSPP
感觉不难，但就是没想到。

首先要意识到必然会有边权为 $0$ 的环。

然后要对这些环缩点，之后直接暴力即可。

然后考虑枚举 $k^ex$，其枚举范围小于环长 $len$，$y - k^ex$ 的最小值即为 $0\to y - k^ex$ 的最小值。

于是是 $O(({\frac n{len}})^2 + qlen)$，然后平衡一下这两个做法即可。

写了 floyd。

$O((nq)^{\frac 34})$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 1e6 + 9, inf = 0x3f3f3f3f3f3f3f3f;
int p, k, q, pw[N], dst[N], len;
vector<pair<int, int>> es[N];
int vst[N], bel[N], lp, f[409][409];
void sol1() {
  memset(vst, 0, sizeof vst);
  memset(f, 0x3f, sizeof f);
  for (int i = 0; i < p; ++i) {
    if (!vst[i]) {
      int x = i; ++lp;
      while (!vst[x]) {
        bel[x] = lp, vst[x] = 1;
        x = k * x % p;
      }
    }
  }
  for (int i = 0; i < p; ++i) {
    if (k > 1) f[bel[i]][bel[(k * i + 1) % p]] = 1;
  }
  for (int i = 1; i <= lp; ++i) f[i][i] = 0;
  for (int i = 1; i <= lp; ++i)
    for (int j = 1; j <= lp; ++j)
      for (int k = 1; k <= lp; ++k) cmin(f[j][k], f[j][i] + f[i][k]);
  while (q--) {
    int x, y;
    cin >> x >> y;
    if (bel[x] == bel[y]) cout << 0 << '\n';
    else if (f[bel[x]][bel[y]] == inf) cout << -1 << '\n';
    else cout << f[bel[x]][bel[y]] << '\n';
  }
}
void sol2() {
  for (int i = 0; i < p; ++i) {
    es[i].clear();
    for (int j = 0; j < k && j < 2; ++j) es[i].emplace_back((k * i + j) % p, j);
  }
  deque<int> Q;
  memset(dst, 0x3f, sizeof dst);
  dst[0] = 0;
  Q.push_back(0);
  while (!Q.empty()) {
    int x = Q.front();
    Q.pop_front();
    for (auto [y, z] : es[x])
      if (dst[y] > dst[x] + z) {
        dst[y] = dst[x] + z;
        if (z) Q.push_back(y);
        else Q.push_front(y);
      }
  }
  while (q--) {
    int x, y;
    cin >> x >> y;
    int ans = inf;
    for (int i = 0; i < len; ++i) {
      cmin(ans, dst[(y + p - x * pw[i] % p) % p]);
    }
    if (ans == inf) cout << -1 << '\n';
    else cout << ans << '\n';
  }
}
signed main() {
  freopen("osu.in", "r", stdin);
  freopen("osu.out", "w", stdout);
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> p >> k >> q, lp = 0;
    for (int i = pw[0] = 1; i < p; ++i)
      pw[i] = pw[i - 1] * k % p;
    len = 1;
    while (pw[len] != 1) ++len;
    if (q * len < p * p * p / len / len / len) sol2();
    else sol1();
  }
}
```


----------
2025.11.14
### QOJ11318
不难想但是难写。

首先假设一个 $1\sim i$ 前缀已经翻到最优了，那么这次可以翻转 $1\sim j$，我们有两种可能：
1. 不翻，直接接在后面。
2. 先把 $1\sim i$ 翻，再翻 $1\sim j$，先当于翻 $i + 1 \sim j$ 然后放在 $1\sim i$ 的前面。

用双端队列维护这个过程，然后维护一个放在前面的数的哈希和放在后面的数的哈希，判断字典序直接二分判断。

写起来十分困难，哈希还要把两个部分拼起来，非常难写。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
#define int long long
mt19937_64 rng(random_device{}());
using u64 = unsigned long long;
using i128 = __int128;
const u64 msk = rng();
struct hash_t {
  static u64 shift(u64 x) {
    x ^= msk;
    x ^= (x << 5ull);
    x ^= (x >> 11ull);
    x ^= (x << 54ull);
    return x ^ msk;
  }
  static constexpr u64 hmod = (1LL << 61) - 1;
  u64 h;
  constexpr hash_t() : h{0} {}
  constexpr hash_t(u64 H) : h{H % hmod} {}
  hash_t& operator+=(hash_t rhs) {
    h += rhs.h, h >= hmod && (h -= hmod);
    return *this;
  }
  hash_t& operator-=(hash_t rhs) {
    h += hmod - rhs.h, h >= hmod && (h -= hmod);
    return *this;
  }
  hash_t& operator*=(hash_t rhs) {
    i128 rt = (i128) h * rhs.h;
    h = u64(rt & hmod) + u64(rt >> 61);
    if (h >= hmod) h -= hmod;
    return *this;
  }
  friend hash_t operator+(hash_t lhs, const hash_t& rhs) {
    return lhs += rhs;
  }
  friend hash_t operator-(hash_t lhs, const hash_t& rhs) {
    return lhs -= rhs;
  }
  friend hash_t operator*(hash_t lhs, const hash_t& rhs) {
    return lhs *= rhs;
  }
  bool operator==(const hash_t& rhs) const {
    return h == rhs.h;
  }
  bool operator<(const hash_t& rhs) const {
    return h < rhs.h;
  }
};
hash_t qpow(hash_t a, u64 b) {
  hash_t r = 1;
  for (; b > 0; b >>= 1, a = a * a)
    if (b & 1) r = r * a;
  return r;
}
const hash_t seed = uniform_int_distribution<u64>(hash_t::hmod >> 2, hash_t::hmod >> 1)(rng);
// const hash_t seed = 1000;
const hash_t iseed = qpow(seed, hash_t::hmod - 2);
constexpr int N = 6e5 + 9, inf = 0x3f3f3f3f, md = 20181125;
int n, m, a[N], b[N], ban[N], ps[N], ans[N], hd, tl;
hash_t hr[N], hl[N], pw[N], ipw[N];
hash_t getr(int l, int r) {
  if (l > r) return 0;
  return hr[r] - hr[l - 1] * pw[r - l + 1];
}
hash_t getl(int l, int r) {
  if (l > r) return 0;
  return (hl[r] - hl[l - 1]) * ipw[l - 1];
}
u64 get(int l, int r) {
  if (n < l) return getr(l - n, r - n).h;
  else if (r <= n) return getl(n + 1 - r, n + 1 - l).h;
  else return (getl(1, n + 1 - l) * pw[r - n] + getr(1, r - n)).h;
}
bool chk(int pl, int pr, int ql, int qr) {
  // cerr << pl << ' ' << pr << ' ' << ql << ' ' << qr << '\n';
  int l = 0, r = pr - pl + 1;
  while (l < r) {
    int m = (l + r) >> 1;
    if (get(pl, pl + m) != get(ql, ql + m)) r = m;
    else l = m + 1;
  }
  // cerr << get(pl, pl) << ' ' << get(ql, ql) << '\n';
  // for (int i = pl; i <= pr; ++i) cerr << ans[i] << ' ';
  // cerr << '\n';
  // for (int i = ql; i <= qr; ++i) cerr << ans[i] << ' ';
  // cerr << '\n';
  // cerr << l <<  '\n';
  return ans[pl + l] < ans[ql + l];
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  pw[0] = ipw[0] = 1;
  for (int i = 1; i < N; ++i) pw[i] = pw[i - 1] * seed, ipw[i] = ipw[i - 1] * iseed;
  for (int test = 1; test <= tt; ++test) {
    cin >> n >> m;
    for (int i = 1; i <= n; ++i) cin >> a[i], ban[i] = 0;
    for (int i = 1; i <= m; ++i) cin >> b[i], ban[b[i]] = 1;
    int c = 0;
    for (int i = 1; i <= n; ++i)
      if (!ban[i]) ps[++c] = i;
    hd = n + 1, tl = n;
    for (int i = 1; i <= c; ++i) {
      int pl = hd, pr = tl;
      for (int j = ps[i - 1] + 1; j <= ps[i]; ++j) {
        ans[++pr] = a[j], hr[pr - n] = hr[pr - n - 1] * seed + (a[j]);
      }
      for (int j = ps[i - 1] + 1; j <= ps[i]; ++j) {
        ans[--pl] = a[j], hl[n + 1 - pl] = hl[n - pl] + (a[j]) * pw[n - pl];
        // cerr << hl[n + 1 - pl].h << ' ' << n + 1 - pl << '\n';
        // cerr << n - pl << '\n';
      }
      // cerr << '\n';
      // cerr << hl[3].h << ' ' << hl[2].h << '\n';
      if (chk(pl, tl, hd, pr)) hd = pl;
      else tl = pr;
    }
    for (int i = ps[c] + 1; i <= n; ++i) ans[++tl] = a[i];
    int res = 0;
    for (int i = hd, w = 1; i <= tl; ++i) {
      (res += w * ans[i]) %= md;
      (w *= 37) %= md;
      // cerr << ans[i] << ' ';
    }
    // cerr << '\n';
    cout << "Case " << test << ": " << res << '\n';
  }
}
```
