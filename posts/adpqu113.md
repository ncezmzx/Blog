---
title: "DP 优化"
date: 2025-07-24T20:34:20+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/adpqu113"
luogu_id: "adpqu113"
---

### 数据结构优化 DP
无非就是快速修改和查询一个范围的 DP 值。
### 分治优化 DP
用于优化 2D/1D。

要求状态在相邻层之间转移，即 $f_i\to f_{i + 1}$。

所以一般层数会比较小。

分治优化会优化转移 $O(n)\to O(\log n)$。

一般这类 DP 都长成这样 $f_{k, i} \leftarrow f_{k - 1, p_i} + w(i, p_i)$。

其中 $p_i$ 为 $i$ 的决策点。

决策单调性即指决策点单调。

如果 $w(i, j)$ 满足四边形不等式，那么 $f$ 具有决策单调性。

四边形不等式（假设我们要最小化贡献）：

- 若 $a < b < c < d$ 则 $w(a, d) + w(b, c) \geq w(a, c) + w(b, d)$。

如果转移满足决策单调性，那么就可以用分治来优化。

由于转移具有决策单调性，那么假设我们已知 $i$ 的决策点为 $p$，那么对于 $j < i$，其决策点必然小于等于 $p$，反之大于等于。

于是考虑分治，每次将区间 $[l, r]$ 分为 $[l, mid)$ 和 $(mid, r]$。设当前区间决策点的范围为 $[pl, pr]$，$mid$ 的决策点为 $p$，则 $[l, mid)$ 的决策范围为 $[pl, p]$。

每一层我们暴力枚举 $mid$ 的决策点 $p$，复杂度 $O(n)$，分治最多 $\log n$ 层，总复杂度 $O(n \log n)$。

注意这是一层之间的转移，如果有 $k$ 层要转移 $k$，复杂度为 $O(nk \log n)$。

#### 计算贡献
有时候贡献很难算，比如区间不同数的个数，我们可以用类似莫队的方法。

```cpp
int calc(int l, int r) {
  while (x < l) del(x++);
  while (x > l) add(--x);
  while (y < r) add(++y);
  while (y > r) del(y--);
  return ret;
}
```

每次暴力移动指针，设从 $i$ 拓展到 $i \pm 1$ 的复杂度为 $O(m)$，总复杂度为 $O(nm \log n)$。

#### CF833B The Bakery
模板
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 3.5e4 + 9, K = 59;
int f[K][N], n, k, a[N], x = 1, y, cnt[N], ret;
void add(int x) {
  ret += ++cnt[a[x]] == 1;
}
void del(int x) {
  ret -= --cnt[a[x]] == 0;
}
int calc(int l, int r) {
  while (x < l) del(x++);
  while (x > l) add(--x);
  while (y < r) add(++y);
  while (y > r) del(y--);
  return ret;
}
void dfs(int l, int r, int pl, int pr, int j) {
  if (l > r) return ;
  int m = (l + r) >> 1, p = m;
  for (int i = pl; i <= min(pr, m - 1); ++i) {
    if (f[j - 1][i] + calc(i + 1, m) > f[j][m]) p = i, f[j][m] = f[j - 1][i] + calc(i + 1, m);
  }
  dfs(l, m - 1, pl, p, j), dfs(m + 1, r, p, pr, j);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> k;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i <= k; ++i) dfs(1, n, 0, n, i);
  cout << f[k][n];
  return 0;
}
```
### 斜率优化

1D/1D 的最优化 DP。

$i$ 从 $j$ 转移来，那么把 DP 方程化成 $y = kx + b$ 的形式。

其中 $k$ 仅与 $i$ 相关，且已经求出，$b$ 仅与 $dp_i$ 相关，可以由 $b$ 推出 $dp_i$，$x, y$ 仅与 $j$ 相关，且已经求出。

那么这就变成最小/最大化一条经过已知点的直线在 $y$ 轴上的截距。

最小化维护下凸壳，最大化维护上凸壳。

每次找到凸壳上第一条斜率大于/小于等于当前直线斜率的边，这条边的左端点就是直线与凸壳的切点，也就是最优决策点。

用单调队列优化这一过程，时间复杂度 $O(n)$，需要满足每次加点 $x$ 是有序的且斜率 $k$ 是有序的。

如果 $k$ 不单调，就不能用单调队列而应用单调栈维护凸包，每次二分出决策点。

$k, x$ 均单调的时候，满足决策单调性，否则不一定满足。

有一点需要注意的是，如果两点为 $(x, y_1),(x, y_2)$ 即横坐标相等，斜率应根据 $y_2 - y_1$ 的正负赋为极大/极小值。

#### P2900 [USACO08MAR] Land Acquisition G
DP 方程：$dp_i = \min_{j = 1}^{i - 1} dp_j + w_ih_{j + 1}$。

转换后 $dp_j = w_i \times (-h_{j + 1}) + dp_i$。

$k = w_i, b = dp_i, x = -h_{j + 1}, y = dp_j$。

由于要最小化 $dp_i$，所以维护下凸壳，事先对 $w_i$ 排序后，把所有 $w_j \leq w_i$ 且 $h_j \leq h_i$ 的 $j$ 删了，于是变成了 $w$ 升序，$h$ 降序。
```
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 5e4 + 9;
int n, m, q[N], l = 1, r, dp[N];
struct node {
  int w, h;
  bool operator<(const node &x) const { return w == x.w ? h < x.h : w < x.w; }
} a[N], b[N];
int getx(int x) {
  return -b[x + 1].h;
}
int gety(int x) {
  return dp[x];
}
double slope(int x, int y) {
  return 1. * (gety(y) - gety(x)) / (getx(y) - getx(x));
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i].w >> a[i].h;
  sort(a + 1, a + n + 1);
  for (int i = 1; i <= n; ++i) {
    while (m && a[i].h >= b[m].h) --m;
    b[++m] = a[i];
  }
  q[++r] = 0;
  for (int i = 1; i <= m; ++i) {
    while (l < r && slope(q[l], q[l + 1]) <= b[i].w) ++l;
    dp[i] = b[i].w * b[q[l] + 1].h + dp[q[l]];
    // cerr << q[l] << ' ' << dp[i] << '\n';
    while (l < r && slope(q[r - 1], q[r]) >= slope(q[r], i)) --r;
    q[++r] = i;
  }
  cout << dp[m];
  return 0;
}
```
