---
title: "题解：P6908 [ICPC 2015 WF] Evolution in Parallel"
date: 2026-10-28T21:07:45+08:00
author: "Mr_Min"
category: "题解 P6908"
tags: ["题解 P6908", "洛谷"]
source: "https://www.luogu.com.cn/article/bp1ujflk"
luogu_id: "bp1ujflk"
---

先按长度排序，若 $i < j$，$s_i$ 是 $s_j$ 的子序列则连 $i\to j$ 的边，题目相当于求这个图的最小链覆盖。

最小链覆盖等于最长反链，所以存在 $i < j <k$，$s_i, s_j, s_k$ 互不为子序列则无解。

于是直接贪心，维护两条链 $p, q$，和一条延迟决策的链 $r$。枚举 $s_i$，若 $s_i$ 只能接到 $p, q$ 中一条上，就直接接；如果两条都可以，考虑接到 $r$ 上延迟决策。如果不能接到 $r$ 上，那么 $s_i$ 和 $r$ 必然在不同的链，随便接 $p, q$ 即可；如果两条都不能接，那么此时 $s_i, p, q$ 构成了长度为 $3$ 的反链，无解。

复杂度 $O(n|s|)$。


```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 5009;
int n;
string s[N];
bool cmp(const string &a, const string &b) {
  if (a.size() > b.size()) return false;
  for (int i = 0, j = 0; i < a.size(); ++i, ++j) {
    while (j < b.size() && b[j] != a[i]) ++j;
    if (j == b.size()) return false;
  }
  return true;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> s[n + 1];
  for (int i = 1; i <= n; ++i) {
    cin >> s[i];
    if (!cmp(s[i], s[n + 1])) return cout << "impossible", 0;
  }
  sort(s + 1, s + n + 1, [&](const string &ls, const string &rs) -> bool { return ls.size() < rs.size(); });
  vector<string> p[2], r;
  for (int i = 1; i <= n; ++i) {
    int t = 0;
    if (p[0].empty() || cmp(p[0].back(), s[i])) t += 1;
    if (p[1].empty() || cmp(p[1].back(), s[i])) t += 2;
    if (!t) return cout << "impossible", 0;
    if (t == 3) {
      if (r.empty() || cmp(r.back(), s[i])) {
        r.push_back(s[i]);
        continue;
      }
      t = 1;
    }
    p[t - 1].push_back(s[i]);
    for (auto &j : r) p[(t - 1) ^ 1].push_back(j);
    r.clear();
  }
  for (auto &j : r) p[0].push_back(j);
  cout << p[0].size() << ' ' << p[1].size() << '\n';
  for (auto &i : p[0]) cout << i << '\n';
  for (auto &i : p[1]) cout << i << '\n';
}
```
