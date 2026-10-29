---
title: "Dinic"
date: 2025-08-15T09:38:40+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/d6beeged"
luogu_id: "d6beeged"
---

```cpp line-numbers
template <class T> struct dinic {
  vector<int> cur, hd, nxt, to, dis;
  vector<T> cap;
  static constexpr T inf = numeric_limits<T>::max();
  int tot;
  dinic(int _n, int _m) : cur(_n + 2), hd(_n + 2), nxt(_m * 2 + 2), to(_m * 2 + 2), cap(_m * 2 + 2), dis(_n + 2), tot(1) {}
  void add(int u, int v, T w) {
#ifdef DEBUG
    assert(u < hd.size() && u >= 0);
    assert(v < hd.size() && v >= 0);
    assert(tot + 2 < nxt.size());
#endif
    nxt[++tot] = hd[u], hd[u] = tot, to[tot] = v, cap[tot] = w;
    nxt[++tot] = hd[v], hd[v] = tot, to[tot] = u, cap[tot] = 0;
  }
  T dfs(int u, int t, T flow) {
    if (u == t) return flow;
    T ret = 0;
    for (int i = cur[u]; i && flow; i = nxt[i]) {
      cur[u] = i;
      T c = min(cap[i], flow);
      if (dis[to[i]] == dis[u] + 1 && c > 0) {
        T tmp = dfs(to[i], t, c);
        ret += tmp, cap[i] -= tmp, cap[i ^ 1] += tmp, flow -= tmp;
      }
    }
    if (!ret) dis[u] = -1;
    return ret;
  }
  T calc(int s, int t) {
#ifdef DEBUG
    assert(t >= 0 && t < dis.size());
    assert(s >= 0 && s < dis.size());
#endif
    T ret = 0;
    while (true) {
      dis.assign(dis.size(), -1);
      queue<int> q;
      q.push(s), dis[s] = 0;
      cur = hd;
      while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int i = hd[u]; i; i = nxt[i]) {
          if (dis[to[i]] == -1 && cap[i] > 0) {
            dis[to[i]] = dis[u] + 1;
            q.push(to[i]);
          }
        }
      }
      if (dis[t] == -1) return ret;
      ret += dfs(s, t, inf);
    }
  }
};
```
