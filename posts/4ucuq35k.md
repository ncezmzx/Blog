---
title: "网络流和二分图相关"
date: 2026-11-13T07:27:04+08:00
author: "Mr_Min"
category: "4"
tags: ["4", "洛谷"]
source: "https://www.luogu.com.cn/article/4ucuq35k"
luogu_id: "4ucuq35k"
---

### 费用流
有很多种费用流，复杂度都不太一样，但实际跑出来效果似乎差不多？

#### spfa + 单/多路增广

相当于把 EK 和 dinic 的 bfs 换成了 spfa，单轮瓶颈在 spfa，$O(nm)$，轮数上界是 $O(f)$，$f$ 是最大流。

所以这么做的上界是 $O(nmf)$，实际跑不满。

#### 原始对偶
首先类似 Johnson，设置 $h_i$ 作为势能，每次增广后势能变化都是容易计算的，因此每轮跑 dijkstra 即可。

如果有负费用，还要在初始跑一遍 spfa 计算 $h_i$。
##### 单路增广

单轮复杂度瓶颈在 dijkstra，轮数 $O(f)$，复杂度上界 $O(fm\log n)$，同样跑不满。

##### 多路增广

同上，只是每轮在最短路图上跑完整的 dinic，所以单轮 $O(n^2m)$，轮数好像是 $O(nc)$，$c$ 是费用上界。

于是上界是 $O(n^3mc)$，实际跑的 spfa + 单/多路增广快一倍。

```cpp
template<size_t N, size_t M> struct mcmf {
  int hd[N], nxt[M * 2], to[M * 2], cap[M * 2], cst[M * 2], tot = 1, dst[N], len[N], cur[N], h[N], vst[N], s, t, n;
  void add(int x, int y, int w, int c) {
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
