---
title: "模板"
date: 2026-03-06T21:42:50+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/bogywyli"
luogu_id: "bogywyli"
---

免得找不到了。

------------------
### SPFA
```cpp
memset(dst, 0x3f, sizeof dst);
queue<int> q;
q.push(s), dst[s] = 0;
while (!q.empty()) {
  int x = q.front();
  q.pop(), vst[x] = 0;
  for (auto [y, z] : es[x])
    if (dst[y] > dst[x] + z) {
      dst[y] = dst[x] + z, len[y] = len[x] + 1;
      if (len[y] == n) return 0;
      if (!vst[y]) vst[y] = 1, q.push(y);
    }
}
```
#### 二进制分组优化多重背包
```cpp
for (int i = 1; i <= n; ++i) {
  for (int d = 1, j = 0; j < c[i]; j += d, d = min(d << 1, c[i] - j)) {
    for (int k = V; k >= d * w[i]; --k) f[k] = max(f[k], f[k - d * w[i]] + d * v[i]);
  }
}
```
### 最小费用最大流（spfa + 单路增广）
```cpp
template<size_t N, size_t M> struct mcmf {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cst[M * 2], tot = 1, dst[N], vst[N], fr[N], flw[N];
  void add(int x, int y, int z, int c) {
    nxt[++tot] = hd[x], hd[x] = tot, to[tot] = y, cap[tot] = z, cst[tot] = c;
    nxt[++tot] = hd[y], hd[y] = tot, to[tot] = x, cap[tot] = 0, cst[tot] = -c;
  }
  pair<int, int> calc(int s, int t) {
    int flow = 0, cost = 0;
    while (true) {
      memset(dst, 0x3f, sizeof dst);
      queue<int> q;
      q.push(s), dst[s] = 0, flw[s] = 0x3f3f3f3f;
      while (!q.empty()) {
        int x = q.front();
        q.pop(), vst[x] = 0;
        for (int i = hd[x]; i; i = nxt[i]) {
          if (cap[i] && dst[x] + cst[i] < dst[to[i]]) {
            dst[to[i]] = dst[x] + cst[i], fr[to[i]] = i, flw[to[i]] = min(flw[x], cap[i]);
            if (!vst[to[i]]) vst[to[i]] = true, q.push(to[i]);
          }
        }
      }
      if (dst[t] > 1e9) return {flow, cost};
      flow += flw[t], cost += dst[t] * flw[t];
      for (int u = t; u != s; u = to[fr[u] ^ 1]) cap[fr[u]] -= flw[t], cap[fr[u] ^ 1] += flw[t];
    }
  }
};
```
### 最小费用最大流（spfa + 多路增广）
```cpp
template<size_t N, size_t M> struct mcmf {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cst[M * 2], tot = 1, dst[N], cur[N], vst[N];
  void add(int x, int y, int z, int c) {
    nxt[++tot] = hd[x], hd[x] = tot, to[tot] = y, cap[tot] = z, cst[tot] = c;
    nxt[++tot] = hd[y], hd[y] = tot, to[tot] = x, cap[tot] = 0, cst[tot] = -c;
  }
  pair<int, int> dfs(int x, int t, int w) {
    if (x == t) return {w, 0};
    vst[x] = 1;
    int flow = 0, cost = 0;
    for (int i = cur[x]; i && w; i = nxt[i]) {
      cur[x] = i;
      if (vst[to[i]]) continue;
      int cp = min(cap[i], w);
      if (cp > 0 && dst[x] + cst[i] == dst[to[i]]) {
        auto [f, cs] = dfs(to[i], t, cp);
        flow += f, w -= f, cost += f * cst[i] + cs;
        cap[i] -= f, cap[i ^ 1] += f;
      }
    }
    vst[x] = 0;
    return {flow, cost};
  }
  pair<int, int> calc(int s, int t) {
    int flow = 0, cost = 0;
    while (true) {
      memset(dst, 0x3f, sizeof dst);
      memcpy(cur, hd, sizeof cur);
      queue<int> q;
      q.push(s), dst[s] = 0;
      while (!q.empty()) {
        int x = q.front();
        q.pop(), vst[x] = false;
        for (int i = hd[x]; i; i = nxt[i]) {
          if (cap[i] > 0 && dst[x] + cst[i] < dst[to[i]]) {
            dst[to[i]] = dst[x] + cst[i];
            if (!vst[to[i]]) vst[to[i]] = true, q.push(to[i]);
          }
        }
      }
      if (dst[t] > 1e9) return {flow, cost};
      auto [x, y] = dfs(s, t, inf);
      flow += x, cost += y;
    }
  }
};
```
### 最小费用最大流（原始对偶 + 多路增广）
```cpp
template<size_t N, size_t M> struct mcmf {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cst[M * 2], tot = 1, dst[N], len[N], cur[N], h[N], vst[N], s, t, n, flg;
  void add(int x, int y, int w, int c) {
    if (c < 0) flg = true;
    to[++tot] = y, nxt[tot] = hd[x], hd[x] = tot, cap[tot] = w, cst[tot] = c;
    to[++tot] = x, nxt[tot] = hd[y], hd[y] = tot, cap[tot] = 0, cst[tot] = -c;
  }
  bool dij() {
    for (int i = 0; i <= n; ++i) dst[i] = inf;
    priority_queue<pair<int, int>> q;
    q.push({dst[s] = 0, s});
    while (!q.empty()) {
      auto [d, x] = q.top();
      d = -d, q.pop();
      if (d != dst[x]) continue;
      for (int i = hd[x]; i; i = nxt[i]) {
        if (cap[i] > 0 && dst[to[i]] > dst[x] + cst[i] + h[x] - h[to[i]]) {
          dst[to[i]] = dst[x] + cst[i] + h[x] - h[to[i]];
          q.push({-dst[to[i]], to[i]});
        }
      }
    }
    return dst[t] != inf;
  }
  bool spfa() {
    queue<int> q;
    for (int i = 0; i <= n; ++i) h[i] = inf;
    q.push(s), h[s] = 0, vst[s] = 1;
    while (!q.empty()) {
      int x = q.front();
      q.pop(), vst[x] = 0;
      for (int i = hd[x]; i; i = nxt[i]) {
        if (cap[i] > 0 && h[to[i]] > h[x] + cst[i]) {
          h[to[i]] = h[x] + cst[i];
          if (!vst[to[i]]) vst[to[i]] = 1, q.push(to[i]);
        }
      }
    }
    return h[t] != inf;
  }
  int dfs(int x, int w) {
    if (x == t) return w;
    int flow = 0;
    for (int i = cur[x]; i && w; i = nxt[i]) {
      cur[x] = i;
      int cp = min(cap[i], w);
      if (cp > 0 && len[to[i]] == len[x] + 1 && cst[i] + h[x] - h[to[i]] == 0) {
        int f = dfs(to[i], cp);
        flow += f, w -= f, cap[i] -= f, cap[i ^ 1] += f;
      }
    }
    if (!flow) len[x] = -1;
    return flow;
  }
  bool bfs() {
    queue<int> q;
    for (int i = 0; i <= n; ++i) len[i] = -1, cur[i] = hd[i];
    q.push(s), len[s] = 0;
    while (!q.empty()) {
      int x = q.front();
      q.pop();
      for (int i = hd[x]; i; i = nxt[i]) {
        if (cap[i] > 0 && len[to[i]] == -1 && cst[i] + h[x] - h[to[i]] == 0) {
          len[to[i]] = len[x] + 1;
          q.push(to[i]);
        }
      }
    }
    return len[t] != -1;
  }
  pair<int, int> calc(int S, int T) {
    s = S, t = T;
    int cost = 0, flow = 0;
    if (flg) {
      if (!spfa()) return {0, 0};
    }
    while (dij()) {
      for (int i = 0; i <= n; ++i) if (dst[i] != inf) h[i] += dst[i];
      while (bfs()) {
        int f = dfs(s, inf);
        flow += f, cost += f * h[t];
      }
    }
    return {flow, cost};
  }
};
```
### 最小费用最大流（原始对偶）
```cpp
template<size_t N, size_t M> struct mcmf {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cst[M * 2], tot = 1, dst[N], vst[N], fr[N], flw[N], h[N], n;
  void add(int x, int y, int z, int c) {
    nxt[++tot] = hd[x], hd[x] = tot, to[tot] = y, cap[tot] = z, cst[tot] = c;
    nxt[++tot] = hd[y], hd[y] = tot, to[tot] = x, cap[tot] = 0, cst[tot] = -c;
  }
  bool dij(int s, int t) {
    for (int i = 0; i <= n; ++i) dst[i] = inf;
    priority_queue<pair<int, int>> q;
    q.push({dst[s] = 0, s}), flw[s] = inf;
    while (!q.empty()) {
      auto [d, x] = q.top();
      d = -d, q.pop();
      if (d != dst[x]) continue;
      for (int i = hd[x]; i; i = nxt[i]) {
        if (cap[i] > 0 && dst[to[i]] > dst[x] + cst[i] + h[x] - h[to[i]]) {
          dst[to[i]] = dst[x] + cst[i] + h[x] - h[to[i]], fr[to[i]] = i, flw[to[i]] = min(flw[x], cap[i]);;
          q.push({-dst[to[i]], to[i]});
        }
      }
    }
    return dst[t] != inf;
  }
  pair<int, int> calc(int s, int t) {
    int flow = 0, cost = 0;
    while (dij(s, t)) {
      for (int i = 0; i <= n; ++i)
        if (dst[i] != inf) h[i] += dst[i];
      flow += flw[t], cost += h[t] * flw[t];
      for (int u = t; u != s; u = to[fr[u] ^ 1]) cap[fr[u]] -= flw[t], cap[fr[u] ^ 1] += flw[t];
    }
    return {flow, cost};
  }
};
```
### 最大流（dinic）
```cpp
template<size_t N, size_t M> struct dinic {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cur[N], tot = 1, dst[N];
  void add(int x, int y, int z) {
    nxt[++tot] = hd[x], hd[x] = tot, to[tot] = y, cap[tot] = z;
    nxt[++tot] = hd[y], hd[y] = tot, to[tot] = x, cap[tot] = 0;
  }
  int dfs(int x, int w, int t) {
    if (x == t) return w;
    int flow = 0;
    for (int i = cur[x]; i && w; i = nxt[i]) {
      cur[x] = i;
      int c = min(w, cap[i]);
      if (dst[x] + 1 == dst[to[i]] && c) {
        int k = dfs(to[i], c, t);
        flow += k, w -= k;
        cap[i] -= k, cap[i ^ 1] += k;
      }
    }
    if (!flow) dst[x] = -1;
    return flow;
  }
  int calc(int s, int t) {
    int flow = 0;
    while (true) {
      memset(dst, -1, sizeof dst);
      memcpy(cur, hd, sizeof hd);
      queue<int> q;
      q.push(s), dst[s] = 0;
      while (!q.empty()) {
        int x = q.front();
        q.pop();
        for (int i = hd[x]; i; i = nxt[i]) {
          if (cap[i] && dst[to[i]] == -1) dst[to[i]] = dst[x] + 1, q.push(to[i]);
        }
      }
      if (dst[t] == -1) return flow;
      flow += dfs(s, inf, t);
    }
  }
};
```
### 有源汇上下界最小费用可行流
```cpp
template<size_t N, size_t M> struct mcmf {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cst[M * 2], tot = 1, dst[N], vst[N], fr[N], flw[N];
  void add(int x, int y, int z, int c) {
    nxt[++tot] = hd[x], hd[x] = tot, to[tot] = y, cap[tot] = z, cst[tot] = c;
    nxt[++tot] = hd[y], hd[y] = tot, to[tot] = x, cap[tot] = 0, cst[tot] = -c;
  }
  pair<int, int> calc(int s, int t) {
    int flow = 0, cost = 0;
    while (true) {
      memset(dst, 0x3f, sizeof dst);
      queue<int> q;
      q.push(s), dst[s] = 0, flw[s] = 0x3f3f3f3f;
      while (!q.empty()) {
        int x = q.front();
        q.pop(), vst[x] = 0;
        for (int i = hd[x]; i; i = nxt[i]) {
          if (cap[i] && dst[x] + cst[i] < dst[to[i]]) {
            dst[to[i]] = dst[x] + cst[i], fr[to[i]] = i, flw[to[i]] = min(flw[x], cap[i]);
            if (!vst[to[i]]) vst[to[i]] = true, q.push(to[i]);
          }
        }
      }
      if (dst[t] > 1e9) return {flow, cost};
      flow += flw[t], cost += dst[t] * flw[t];
      for (int u = t; u != s; u = to[fr[u] ^ 1]) cap[fr[u]] -= flw[t], cap[fr[u] ^ 1] += flw[t];
    }
  }
};
template<size_t N, size_t M> struct hlmcmf {
  int cnt, u[M], v[M], cap[M], low[M], w[N], cst[M];
  mcmf<N, N + M> e;
  void add(int x, int y, int z, int l, int c) { u[++cnt] = x, v[cnt] = y, cap[cnt] = z, low[cnt] = l, cst[cnt] = c; }
  int calc(int n, int s, int t) {
    int flow = 0;
    for (int i = 1; i <= cnt; ++i) {
      w[u[i]] -= low[i], w[v[i]] += low[i], flow += cst[i] * low[i];
      e.add(u[i], v[i], cap[i] - low[i], cst[i]);
    }
    int tot = 0;
    for (int i = 1; i <= n; ++i) {
      if (w[i] > 0) e.add(0, i, w[i], 0), tot += w[i];
      else if (w[i] < 0) e.add(i, n + 1, -w[i], 0);
    }
    e.add(t, s, 0x3f3f3f3f, 0);
    auto [x, y] = e.calc(0, n + 1);
    return x == tot ? flow + y : -1;
  }
};
```
### 无源汇有上下界可行流
```cpp
template<size_t N, size_t M> struct dinic {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cur[N], tot = 1, dst[N];
  void add(int x, int y, int z) {
    nxt[++tot] = hd[x], hd[x] = tot, to[tot] = y, cap[tot] = z;
    nxt[++tot] = hd[y], hd[y] = tot, to[tot] = x, cap[tot] = 0;
  }
  int dfs(int x, int w, int t) {
    if (x == t) return w;
    int flow = 0;
    for (int i = cur[x]; i && w; i = nxt[i]) {
      cur[x] = i;
      int c = min(w, cap[i]);
      if (dst[x] + 1 == dst[to[i]] && c) {
        int k = dfs(to[i], c, t);
        flow += k, w -= k;
        cap[i] -= k, cap[i ^ 1] += k;
      }
    }
    if (!flow) dst[x] = -1;
    return flow;
  }
  int calc(int s, int t) {
    int flow = 0;
    while (true) {
      memset(dst, -1, sizeof dst);
      memcpy(cur, hd, sizeof hd);
      queue<int> q;
      q.push(s), dst[s] = 0;
      while (!q.empty()) {
        int x = q.front();
        q.pop();
        for (int i = hd[x]; i; i = nxt[i]) {
          if (cap[i] && dst[to[i]] == -1) dst[to[i]] = dst[x] + 1, q.push(to[i]);
        }
      }
      if (dst[t] == -1) return flow;
      flow += dfs(s, inf, t);
    }
  }
};
template<size_t N, size_t M> struct hlflow {
  int cnt, u[M], v[M], cap[M], low[M], w[N];
  dinic<N, N + M> e;
  void add(int x, int y, int z, int l) { u[++cnt] = x, v[cnt] = y, cap[cnt] = z, low[cnt] = l; }
  bool calc(int n) {
    for (int i = 1; i <= cnt; ++i) {
      w[u[i]] -= low[i], w[v[i]] += low[i];
      e.add(u[i], v[i], cap[i] - low[i]);
    }
    int tot = 0;
    for (int i = 1; i <= n; ++i) {
      if (w[i] > 0) e.add(0, i, w[i]), tot += w[i];
      else if (w[i] < 0) e.add(i, n + 1, -w[i]);
    }
    return e.calc(0, n + 1) == tot;
  }
};
```
### 有源汇上下界最大流
```cpp
template<size_t N, size_t M> struct dinic {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cur[N], tot = 1, dst[N];
  void add(int x, int y, int z) {
    nxt[++tot] = hd[x], hd[x] = tot, to[tot] = y, cap[tot] = z;
    nxt[++tot] = hd[y], hd[y] = tot, to[tot] = x, cap[tot] = 0;
  }
  int dfs(int x, int w, int t) {
    if (x == t)
      return w;
    int flow = 0;
    for (int i = cur[x]; i && w; i = nxt[i]) {
      cur[x] = i;
      int c = min(w, cap[i]);
      if (dst[x] + 1 == dst[to[i]] && c) {
        int k = dfs(to[i], c, t);
        flow += k, w -= k;
        cap[i] -= k, cap[i ^ 1] += k;
      }
    }
    if (!flow)
      dst[x] = -1;
    return flow;
  }
  int calc(int s, int t) {
    int flow = 0;
    while (true) {
      memset(dst, -1, sizeof dst);
      memcpy(cur, hd, sizeof hd);
      queue<int> q;
      q.push(s), dst[s] = 0;
      while (!q.empty()) {
        int x = q.front();
        q.pop();
        for (int i = hd[x]; i; i = nxt[i]) {
          if (cap[i] && dst[to[i]] == -1)
            dst[to[i]] = dst[x] + 1, q.push(to[i]);
        }
      }
      if (dst[t] == -1)
        return flow;
      flow += dfs(s, inf, t);
    }
  }
};
template<size_t N, size_t M> struct hlflow {
  int cnt, u[M], v[M], cap[M], low[M], w[N];
  dinic < N, N + M > e;
  void add(int x, int y, int z, int l) {
    u[++cnt] = x, v[cnt] = y, cap[cnt] = z, low[cnt] = l;
  }
  int calc(int n, int s, int t) {
    for (int i = 1; i <= cnt; ++i) {
      w[u[i]] -= low[i], w[v[i]] += low[i];
      e.add(u[i], v[i], cap[i] - low[i]);
    }
    int tot = 0;
    for (int i = 1; i <= n; ++i) {
      if (w[i] > 0)
        e.add(0, i, w[i]), tot += w[i];
      else if (w[i] < 0)
        e.add(i, n + 1, -w[i]);
    }
    e.add(t, s, inf);
    if (e.calc(0, n + 1) != tot)
      return -1;
    int flow = e.cap[e.hd[s]];
    e.hd[s] = e.nxt[e.hd[s]], e.hd[t] = e.nxt[e.hd[t]];
    return flow + e.calc(s, t);
  }
};
```
### 猫树
```cpp
template<class T, size_t N> struct cattree {
  T ct[__lg(N) + 2][N];
  void build(int n, const T a[]) { // 0-index
    for (int h = 0, s = 1; s <= n; ++h, s <<= 1) {
      for (int i = s; i <= n; i += s << 1) {
        ct[h][i - 1] = a[i - 1];
        for (int j = i - 1; j > i - s; --j) ct[h][j - 1] = a[j - 1] + ct[h][j];
        if (i == n) break;
        ct[h][i] = a[i];
        for (int j = i + 1; j < i + s && j < n; ++j)
          ct[h][j] = ct[h][j - 1] + a[j];
      }
    }
  }
  T query(int l, int r) {
    if (l == r) return ct[0][l];
    int h = __lg(l ^ r);
    return ct[h][l] + ct[h][r];
  }
};
```
### SA
```cpp
int n, sa[N], id[N], rk[N], buc[N], h[N];
void bucsort(const auto &key, int m) {
  memset(buc + 1, 0, m * sizeof(int));
  for (int i = 1; i <= n; ++i) ++buc[rk[i]];
  for (int i = 1; i <= m; ++i) buc[i] += buc[i - 1];
  for (int i = n; i >= 1; --i) sa[buc[rk[id[i]]]--] = id[i];
  id[sa[1]] = 1;
  for (int i = 2; i <= n; ++i) id[sa[i]] = id[sa[i - 1]] + (key(sa[i - 1]) != key(sa[i]));
  memcpy(rk + 1, id + 1, n * sizeof(int));
}
void build() {
  rk[n + 1] = 0;
  for (int i = 1; i <= n; ++i) sa[i] = id[i] = i, rk[i] = s[i] - 'a' + 1;
  bucsort([&](int x) -> int { return rk[x]; }, 26);
  for (int w = 1, p = 0, m = rk[sa[n]]; w < n; w <<= 1, p = 0, m = rk[sa[n]]) {
    for (int i = n - w + 1; i <= n; ++i) id[++p] = i;
    for (int i = 1; i <= n; ++i)
      if (sa[i] > w) id[++p] = sa[i] - w;
    bucsort([&](int x) -> pair<int, int> { return make_pair(rk[x], x + w <= n ? rk[x + w] : -1); }, m);
    if (rk[sa[n]] == n) break;
  }
  for (int i = 1, k = 0; i <= n; ++i) {
    if (k) --k;
    while (s[i + k] == s[sa[rk[i] - 1] + k]) ++k;
    h[rk[i]] = k;
  }
}
```
### ST
并没有很快的 st 表。
```cpp
template<size_t U = 20, size_t Z = 64, class T = int> struct ST {
  int n;
  vector<size_t> f;
  array<vector<T>, U> st;
  vector<T> pr, sf, arr;
  function<bool(T, T)> comp;
  void set(const function<bool(T, T)> &cmp) { comp = cmp; }
  T get(const T &x, const T &y) { return comp(x, y) ? x : y; }
  void build(vector<T> &vec, int sz) {
    n = sz, st.fill(vector<T>((n / Z) + 1));
    f.resize(n + 1);
    arr.swap(vec), pr = sf = arr;
    for (int i = 1; i <= n; ++i) {
      st[0][i / Z] = get(st[0][i / Z], arr[i]);
      if (i / Z == (i - 1) / Z) pr[i] = get(pr[i - 1], pr[i]);
    }
    for (int i = n - 1; i >= 1; --i)
      if ((i + 1) / Z == i / Z) sf[i] = get(sf[i + 1], sf[i]);
    for (int i = 1; i < U; ++i)
      for (int j = 1; j + (1 << i) - 1 <= n / Z; ++j) st[i][j] = get(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
    vector<int> stk(n);
    int tp = 0;
    for (int i = 1; i <= n; ++i) {
      if (i / Z != (i - 1) / Z) tp = 0;
      else f[i] = f[i - 1];
      while (tp && comp(arr[i], arr[stk[tp]])) f[i] &= ~(1LL << (stk[tp--] & (Z - 1)));
      stk[++tp] = i, f[i] |= 1LL << (i & (Z - 1));
    }
  }
  T query(int l, int r) {
    if (l / Z == r / Z) return arr[l + __builtin_ctzll(f[r] >> (l & (Z - 1)))];
    T ret = get(pr[r], sf[l]);
    l /= Z, r /= Z, ++l, --r;
    if (l <= r) {
      int d = __lg(r - l + 1);
      ret = get(ret, get(st[d][l], st[d][r - (1 << d) + 1]));
    }
    return ret;
  }
};
```

### 小波矩阵求静态区间第 k 小
$O(n\log V)-O(\log V)-O(n)$
```cpp
using u64 = unsigned long long;
struct Bitset {
#define pc(x) __builtin_popcountll(x)
  int n;
  vector<pair<u64, int>> v;
  Bitset() {}
  Bitset(const vector<u64> &a) {
    n = (a.size() >> 6) + 1, v.resize(n);
    for (int i = 0; i < a.size(); ++i) v[i >> 6].first |= a[i] << (i & 63);
    for (int i = 1; i < n; ++i) v[i].second = v[i - 1].second + pc(v[i - 1].first);
  }
  int query(int x) { return v[x >> 6].second + pc(v[x >> 6].first & ((1ULL << (x & 63)) - 1)); }
};
struct Wavelet {
  int n, p[30];
  Bitset s[30];
  Wavelet(int *a, int n) : n(n) { // 0-index
    vector<int> t(n);
    for (int i = 29; ~i; --i) {
      int x = 0, y = 0;
      vector<u64> c(n);
      for (int j = 0; j < n; ++j) c[j] = a[j] >> i & 1;
			for (int j = 0; j < n; ++j) (a[j] >> i & 1 ? t[y++] : a[x++]) = a[j];
      for (int j = 0; j < y; ++j) a[x + j] = t[j];
      p[i] = x, s[i] = Bitset(c);
    }
  }
  int query(int l, int r, int k) {
    --l;
    int res = 0;
    for (int i = 29; ~i; --i) {
      int ql = s[i].query(l), qr = s[i].query(r), c = (r - qr) - (l - ql);
      if (c >= k) l -= ql, r -= qr;
      else res |= 1 << i, k -= c, l = ql + p[i], r = qr + p[i];
    }
    return res;
  }
};
```

###  哈希
```cpp
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
const hash_t seed = uniform_int_distribution<u64>(hash_t::hmod >> 2, hash_t::hmod >> 1)(rng);
struct strhash { // 1-index
  int n;
  vector<hash_t> h1, h2, pw;
  template <class T> void init(int m, T a) {
    h1.resize(m + 2), h2.resize(m + 2), pw.resize(m + 2);
    n = m, pw[0] = 1;
    for (int i = 1; i <= m; ++i) pw[i] = pw[i - 1] * seed;
    for (int i = 1; i <= m; ++i) h1[i] = h1[i - 1] * seed + hash_t::shift(a[i]);
    for (int i = m; i >= 1; --i) h2[i] = h2[i + 1] * seed + hash_t::shift(a[i]);
  }
  hash_t queryp(int l, int r) const {
    assert(1 <= l && r <= n);
    return h1[r] - h1[l - 1] * pw[r - l + 1];
  }
  u64 query1(int l, int r) const {
    return queryp(l, r).h;
  }
  hash_t querys(int l, int r) const {
    assert(1 <= l && r <= n);
    return h2[l] - h2[r + 1] * pw[r - l + 1];
  }
  u64 query2(int l, int r) const {
    return querys(l, r).h;
  }
};
```

### 手写 bitset
```cpp
struct Bitset {
  using u64 = unsigned long long;
  static constexpr u64 W = u64(-1);
  vector<u64> v;
  int n, len;
  u64 mask;
  Bitset() = default;
  Bitset(int l) : n((l >> 6) + 1), len(l), mask((1ULL << (l & 63)) - 1) { v.resize(n); }
  void trim() { v[len >> 6] &= mask; }
  Bitset& operator=(const Bitset& a) {
    v = a.v, len = a.len, n = a.n;
    return *this;
  }
  Bitset& operator&=(const Bitset &a) {
    for (int i = 0; i < n; ++i) v[i] &= a.v[i];
    return *this;
  }
  friend Bitset operator&(Bitset a, const Bitset &b) { return a &= b; }
  Bitset& operator|=(const Bitset &a) {
    for (int i = 0; i < n; ++i) v[i] |= a.v[i];
    return *this;
  }
  friend Bitset operator|(Bitset a, const Bitset &b) { return a |= b; }
  Bitset& operator^=(const Bitset &a) {
    for (int i = 0; i < n; ++i) v[i] ^= a.v[i];
    return *this;
  }
  friend Bitset operator^(Bitset a, const Bitset &b) { return a ^= b; }
  Bitset& operator-=(const Bitset &a) {
    for (int i = 0; i < n; ++i) v[i] &= ~a.v[i];
    return *this;
  }
  friend Bitset operator-(Bitset a, const Bitset &b) { return a -= b; }
  friend bool operator==(const Bitset &a, const Bitset &b) {
    return memcmp(a.v.data(), b.v.data(), sizeof(u64) * a.n) == 0;
  }
  friend bool operator!=(const Bitset &a, const Bitset &b) { return !(a == b); }
  friend bool operator<=(const Bitset &a, const Bitset &b) {
    for (int i = 0; i < a.n; ++i)
      if ((a.v[i] & b.v[i]) != a.v[i]) return false;
    return true;
  }
  friend bool operator>=(const Bitset &a, const Bitset &b) { return b <= a; }
  friend bool operator<(const Bitset &a, const Bitset &b) {
    bool neq = false;
    for (int i = 0; i < a.n; ++i)
      if (neq |= (a.v[i] != b.v[i]), (a.v[i] & b.v[i]) != a.v[i]) return false;
    return neq;
  }
  friend bool operator>(const Bitset &a, const Bitset &b) { return b < a; }
  void set(int i) {
    if (i >= len) return ;
    v[i >> 6] |= 1ULL << (i & 63);
  }
  void set(int l, int r) {
    if (l > r || r >= len) return ;
    int sl = l >> 6, sr = r >> 6;
    for (; l >> 6 == sl && l <= r; ++l) v[sl] |= 1ULL << (l & 63);
    for (; r >> 6 == sr && l <= r; --r) v[sr] |= 1ULL << (r & 63);
    for (int i = sl + 1; i < sr; ++i) v[i] = W;
  }
  void set() { fill(v.begin(), v.end(), size_t(-1)), trim(); }
  void unset(int i) {
    if (i >= len) return ;
    v[i >> 6] &= ~(1ULL << (i & 63));
  }
  void unset(int l, int r) {
    if (l > r || r >= len) return ;
    int sl = l >> 6, sr = r >> 6;
    for (; l >> 6 == sl && l <= r; ++l) v[sl] &= ~(1ULL << (l & 63));
    for (; r >> 6 == sr && l <= r; --r) v[sr] &= ~(1ULL << (r & 63));
    for (int i = sl + 1; i < sr; ++i) v[i] = 0;
  }
  void unset() { fill(v.begin(), v.end(), 0); }
  void flip(int i) {
    if (i >= len) return ;
    v[i >> 6] ^= 1ULL << (i & 63);
  }
  void flip(int l, int r) {
    if (l > r || r > len) return ;
    int sl = l >> 6, sr = r >> 6;
    for (; l >> 6 == sl && l <= r; ++l) v[sl] ^= 1ULL << (l & 63);
    for (; r >> 6 == sr && l <= r; --r) v[sr] ^= 1ULL << (r & 63);
    for (int i = sl + 1; i < sr; ++i) v[i] ^= W;
  }
  void flip() {
    for (int i = 0; i < n; ++i) v[i] ^= size_t(-1);
    trim();
  } 
  bool none() const {
    for (int i = 0; i < n; ++i)
      if (v[i] > 0) return false;
    return true;
  }
  bool any() const { return !none(); }
  bool all() const {
    for (int i = 0; i + 1 < n; ++i) if (v[i] != W) return false;
    return v[n - 1] == mask;
  }
  void swap(Bitset &a) {
    ::swap(n, a.n), ::swap(len, a.len), ::swap(mask, a.mask), v.swap(a.v);
  }
  int find0(int p) const {
    if (p >= len) return len;
    int sp = p >> 6;
    u64 msk = ~((1ULL << (p & 63)) - 1), cur = (~v[sp]) & msk;
    if (cur) return min(len, sp * 64 + __builtin_ctzll(cur));
    for (int i = sp + 1; i < n; ++i)
      if (v[i] != W) return min(len, i * 64 + __builtin_ctzll(~v[i]));
    return len;
  }
  int find1(int p) const {
    if (p >= len) return len;
    int sp = p >> 6;
    u64 msk = ~((1ULL << (p & 63)) - 1), cur = v[sp] & msk;
    if (cur) return min(len, sp * 64 + __builtin_ctzll(cur));
    for (int i = sp + 1; i < n; ++i)
      if (v[i] != W) return min(len, i * 64 + __builtin_ctzll(v[i]));
    return len;
  }
  bool operator[](const int i) const { return i >= len ? false : v[i >> 6] >> (i & 63) & 1; }
  int count() const {
    int res = 0;
    for (int i = 0; i < n; ++i) res += __builtin_popcountll(v[i]);
    return res;
  }
  int size() const { return len; }
  Bitset& operator<<=(int s) {
    if (s >= len) return unset(), *this;
    int k = s >> 6, t = s & 63;
    if (k > 0) {
      copy_backward(v.begin(), v.end() - k, v.end());
      fill(v.begin(), v.begin() + k, 0);
    }
    if (t) {
      u64 nxt = 0;
      for (int i = k; i < n; ++i) {
        u64 nx = v[i] >> (64 - t);
        v[i] = v[i] << t | nxt, nxt = nx;
      }
    }
    return trim(), *this;
  }
  Bitset& operator>>=(int s) {
    if (s >= len) return unset(), *this;
    int k = s >> 6, t = s & 63;
    if (k > 0) {
      copy(v.begin() + k, v.end(), v.begin());
      fill(v.end() - k, v.end(), 0);
    }
    if (t) {
      u64 nxt = 0;
      for (int i = n - k - 1; i >= 0; --i) {
        u64 nx = v[i] & ((1ULL << t) - 1);
        v[i] = v[i] >> t | (nxt << (64 - t)), nxt = nx;
      }
    }
    return trim(), *this;
  }
  friend Bitset operator<<(Bitset a, int s) { return a <<= s; }
  friend Bitset operator>>(Bitset a, int s) { return a >>= s; }
  friend ostream& operator<<(ostream &os, const Bitset &a) {
    for (int i = 0; i + 1 < a.n; ++i) {
      for (int j = 0; j < 64; ++j) os << (a.v[i] >> j & 1);
    }
    for (int i = 0; i < (a.len & 63); ++i) os << (a.v[a.n - 1] >> i & 1);
    return os;
  }
  vector<Bitset> split(int k) const {
    vector<Bitset> res(len / k + 1, Bitset(k));
    int c = 0, s = 0;
    while (s < len) {
      int le = min(len - s, k), p = 0, sp = s >> 6, st = s & 63, rem = le;
      while (rem > 0) {
        u64 cur = v[sp];
        if (st) cur = cur >> st | ((sp + 1 < n ? v[sp + 1] : 0) << (64 - st));
        if (rem < 64) cur &= (1ULL << rem) - 1;
        res[c].v[p++] = cur, rem -= 64, ++sp;
      }
      res[c++].trim(), s += le;
    }
    return res;
  }
};
```
