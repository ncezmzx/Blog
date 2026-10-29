---
title: "题解：AT_utpc2024_p Perfect Suika Game on a Tree"
date: 2026-10-26T21:49:08+08:00
author: "Mr_Min"
category: "题解 AT_utpc2024_p"
tags: ["题解 AT_utpc2024_p", "洛谷"]
source: "https://www.luogu.com.cn/article/1svyin1u"
luogu_id: "1svyin1u"
---

注意到 $l + l \to l +1$，类似于 $2^l + 2^l = 2^{l + 1}$，于是把 $a_i$ 替换成 $2^{a_i}$ 考虑。

首先有一个必要条件 $\sum a_i = 2^k$，否则一定合不成一个点。

我们考虑一个合并策略，按等级从低到高来，每次两两合并到下一个等级。观察这个策略，我们发现其实不需要从低到高来合并，可以从叶子往上合并，两者是等价的。

于是对每个点 $x$ 的子树 $T_x$ 考虑，我们令 $s_x = \sum_{v\in T_x} a_v$，则 $s_x$ 为 $1$ 的二进制位各代表一个点。显然对于 $x$ 的两个儿子 $y, z$，若 $s_y$ 与 $s_z$ 中存在两个点等级相同，必然无法合并，这等价于 $\sum \text{popcount}(s_y) = \text{popcount}(\sum s_y)$。同时，若 $s_y$ 中出现了低于 $a_x$ 的等级，也无法合并，由于要满足上一条限制，所以可以直接判断 $\sum s_y$ 的 $\text{lowbit}$ 是否小于 $a_x$。

用可持久化线段树维护 $s_x, \sum s_y$，可以直接线段树合并做到 1log。但是我比较菜，不会线段树合并，所以可以直接 dsu on tree，暴力加点，复杂度 $O(n\log^2 n)$，时限 5 s，轻松通过。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 2e5 + 9, M = N * 300;
int n, q, V, a[N], fa[N], eu[N], ev[N], sz[N], dfn[N], idx, id[N], son[N], cntt[N], cnts[N], lb[N], fail2[N], fail3[N], c2, c3;
vector<int> es[N];
int tot, rts[N], rtt[N], ls[M], rs[M], sgt[M], tg[M];
int build(int l, int r) {
  int u = ++tot;
  if (l == r) return u;
  int m = (l + r) >> 1;
  return ls[u] = build(l, m), rs[u] = build(m + 1, r), u;
}
int apply(int u, int l, int r, int x) {
  int dir = ++tot;
  sgt[dir] = r - l + 1 - sgt[u], ls[dir] = ls[u], rs[dir] = rs[u], tg[dir] = tg[u] ^ x;
  return dir;
}
void down(int u, int l, int r) {
  if (tg[u]) {
    int m = (l + r) >> 1;
    ls[u] = apply(ls[u], l, m, tg[u]), rs[u] = apply(rs[u], m + 1, r, tg[u]);
    tg[u] = 0;
  }
}
void print(int u, int l, int r) {
  if (!u) return cerr << string(r - l + 1, '0'), void();
  if (l == r) return cerr << sgt[u], void();
  int m = (l + r) >> 1;
  down(u, l, r);
  print(ls[u], l, m), print(rs[u], m + 1, r);
}
bool found;
int update0(int u, int l, int r, int x) {
  if (x <= l && sgt[u] == r - l + 1) return apply(u, l, r, 1);
  int dir = ++tot;
  ls[dir] = ls[u], rs[dir] = rs[u], tg[dir] = tg[u];
  if (l == r) return found = true, sgt[dir] = 1, dir;
  int m = (l + r) >> 1;
  down(dir, l, r);
  if (m >= x) ls[dir] = update0(ls[dir], l, m, x);
  if (!found) rs[dir] = update0(rs[dir], m + 1, r, x);
  sgt[dir] = sgt[ls[dir]] + sgt[rs[dir]];
  return dir;
}
int update1(int u, int l, int r, int x) {
  if (x <= l && !sgt[u]) return apply(u, l, r, 1);
  int dir = ++tot;
  ls[dir] = ls[u], rs[dir] = rs[u], tg[dir] = tg[u];
  if (l == r) return found = true, sgt[dir] = 0, dir;
  int m = (l + r) >> 1;
  down(dir, l, r);
  if (m >= x) ls[dir] = update1(ls[dir], l, m, x);
  if (!found) rs[dir] = update1(rs[dir], m + 1, r, x);
  sgt[dir] = sgt[ls[dir]] + sgt[rs[dir]];
  return dir;
}
int find(int u, int l, int r) {
  if (l == r) return l;
  int m = (l + r) >> 1;
  down(u, l, r);
  if (sgt[ls[u]]) return find(ls[u], l, m);
  else return find(rs[u], m + 1, r);
}
void add(int &u, int x) { found = false, u = update0(u, 1, V, x); }
void del(int &u, int x) { found = false, u = update1(u, 1, V, x); }
void ins2(int x) { c2 += !fail2[x], fail2[x] = 1; }
void ins3(int x) { c3 += !fail3[x], fail3[x] = 1; }
void ers2(int x) { c2 -= fail2[x], fail2[x] = 0; }
void ers3(int x) { c3 -= fail3[x], fail3[x] = 0; }
void dfs(int x, int ff) {
  fa[x] = ff, sz[x] = 1, id[dfn[x] = ++idx] = x;
  for (int y : es[x])
    if (y ^ ff) {
      dfs(y, x), cnts[x] += sgt[rts[y]], sz[x] += sz[y];
      if (sz[son[x]] < sz[y]) son[x] = y;
    }
  rtt[x] = rts[son[x]];
  for (int y : es[x]) {
    if (y ^ ff && y ^ son[x]) {
      for (int i = dfn[y]; i < dfn[y] + sz[y]; ++i) add(rtt[x], a[id[i]]);
    }
  }
  cntt[x] = sgt[rtt[x]];
  if (cntt[x] != cnts[x]) ins2(x);
  add(rts[x] = rtt[x], a[x]);
  lb[x] = find(rts[x], 1, V);
  if (lb[x] < a[x]) ins3(x);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n, V = n + 20;
  for (int i = 1, x, y; i < n; ++i) {
    cin >> x >> y, eu[i] = x, ev[i] = y;
    es[x].push_back(y), es[y].push_back(x);
  }
  for (int i = 1; i <= n; ++i) cin >> a[i];
  rts[0] = build(1, V), dfs(1, 0);
  cin >> q;
  while (q--) {
    int e;
    cin >> e;
    int x = eu[e], y = ev[e];
    if (fa[y] == x) swap(x, y);
    ers2(y), ers3(x), ers3(y);
    cnts[y] -= sgt[rts[x]];
    del(rtt[y], a[x]), del(rts[x], a[x]), add(rtt[y], a[y]), add(rts[x], a[y]), swap(a[x], a[y]);
    cnts[y] += sgt[rts[x]], cntt[y] = sgt[rtt[y]], lb[x] = find(rts[x], 1, V);
    if (cntt[y] != cnts[y]) ins2(y);
    if (lb[x] < a[x]) ins3(x);
    if (lb[y] < a[y]) ins3(y);
    cout << (sgt[rts[1]] == 1 && !c2 && !c3 ? "Yes\n" : "No\n");
  }
}
```
