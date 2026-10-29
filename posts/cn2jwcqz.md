---
title: "记录 续"
date: 2025-10-16T10:26:37+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/cn2jwcqz"
luogu_id: "cn2jwcqz"
---

[记录](https://www.luogu.com.cn/article/nxgwm1e4) 要炸了，所以写这来了。

2025.10.16
### CF149D
显然区间 dp，令 $f_{l, r, p, q}$（$p, q\in \{ 0, 1, 2\}$） 表示 $[l, r]$ 左右端点为 $p, q$ 颜色的方案数。

转移分讨一下：

- 如果 $l, r$ 匹配，那么 $[l + 1, r - 1]$ 也是合法序列，我们直接从 $f_{l + 1, r - 1, p^{'}, q^{'}}$ 转移过来。由于相邻括号不能染同色，所以要判掉。
- 如果不匹配，那么我们预处理 $nxt_i$ 表示与 $i$ 匹配的右括号位置，这样我们可以从 $[l, nxt_l]$ 和 $[nxt_l + 1, r]$ 两个转移过来，同样把不满足限制的判掉即可。

因为比较懒所以直接写了记搜。

$O(n^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 709, md = 1e9 + 7;
int n, f[N][N][3][3], nxt[N], stk[N], tp;
string s;
int dfs(int l, int r, int p, int q) {
  if (l + 1 == r) return (p > 0) + (q > 0) == 1;
  if (~f[l][r][p][q]) return f[l][r][p][q];
  auto &res = f[l][r][p][q] = 0;
  if (nxt[l] == r) {
    if ((p > 0) + (q > 0) != 1) return res;
    for (int i = 0; i < 3; ++i)
      for (int j = 0; j < 3; ++j) {
        if (i > 0 && i == p) continue;
        if (j > 0 && j == q) continue;
        (res += dfs(l + 1, r - 1, i, j)) %= md;
      }
    return res;
  }
  for (int i = 0; i < 3; ++i) {
    for (int j = 0; j < 3; ++j) {
      if (i > 0 && i == j) continue;
      (res += dfs(l, nxt[l], p, i) * dfs(nxt[l] + 1, r, j, q)) %= md;
    }
  }
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> s, n = s.size(), s = ' ' + s;
  for (int i = 1; i <= n; ++i) {
    if (tp && s[stk[tp]] == '(' && s[i] == ')') nxt[stk[tp--]] = i;
    else stk[++tp] = i;
  }
  memset(f, -1, sizeof f);
  int ans = 0;
  for (int i = 0; i < 3; ++i)
    for (int j = 0; j < 3; ++j) (ans += dfs(1, n, i, j)) %= md;
  cout << ans;
}
```

### UVA1629
rmj 炸了，不知道过没过，vjudge 也交不了。

设 $f_{lx, ly, rx, ry}$ 表示一个矩形的答案，然后每次枚举横切竖切即可。

$O(n^5)$

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 29;
int n, m, k, s[N][N], f[N][N][N][N];
int get(int lx, int ly, int rx, int ry) {
  return s[rx][ry] - s[lx - 1][ry] - s[rx][ly - 1] + s[lx - 1][ly - 1];
}
int dfs(int lx, int ly, int rx, int ry) {
  if (get(lx, ly, rx, ry) == 0) return 0x3f3f3f3f;
  if (get(lx, ly, rx, ry) == 1) return 0;
  auto &res = f[lx][ly][rx][ry];
  if (res != 0x3f3f3f3f) return res;
  for (int i = lx; i < rx; ++i) {
    cmin(res, dfs(lx, ly, i, ry) + dfs(i + 1, ly, rx, ry) + ry - ly + 1);
  }
  for (int i = ly; i < ry; ++i) {
    cmin(res, dfs(lx, ly, rx, i) + dfs(lx, i + 1, rx, ry) + rx - lx + 1);
  }
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt = 0;
  while (cin >> n >> m >> k) {
    memset(s, 0, sizeof s);
    for (int i = 1; i <= k; ++i) {
      int x, y;
      cin >> x >> y;
      ++s[x][y];
    }
    memset(f, 0x3f, sizeof f);
    for (int i = 1; i <= n; ++i)
      for (int j = 1; j <= m; ++j) s[i][j] += s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1];
    cout << "Case " << ++tt << ": " << dfs(1, 1, n, m) << '\n';
  }
}
```

### P5851
区间 dp，令 $f_{l, r}$ 表示 $l, r$ 的答案，转移我们枚举 $i$，令本次的牛强制吃掉 $i$，也就是 $f_{l, r} = \max f_{l, i - 1} + f_{i + 1, r} + g_{l, r, i}$，这里 $g_{l, r, i} = \max\limits_{l \le l_i \le i \le r_i \le r} w_i$ 也就是能吃掉 $i$ 的最重的牛。

$g$ 同样可以转移 $g_{l, r, i} = \max (g_{l + 1, r, i}, g_{l, r - 1, i})$。

$O(n^3)$。

注意一下 $g$ 转移的枚举顺序。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 309;
int n, m, w[N * N], l[N * N], r[N * N], f[N][N], g[N][N][N];
int dfs(int x, int y) {
  if (~f[x][y]) return f[x][y];
  if (x > y) return 0;
  auto &res = f[x][y] = 0;
  for (int j = x; j <= y; ++j) {
    cmax(res, dfs(x, j - 1) + dfs(j + 1, y) + g[x][y][j]);
  }
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    cin >> w[i] >> l[i] >> r[i];
    for (int j = l[i]; j <= r[i]; ++j) cmax(g[l[i]][r[i]][j], w[i]);
  }
  for (int k = 1; k <= n; ++k) {
    for (int x = k; x >= 1; --x) {
      for (int y = k; y <= n; ++y) {
        cmax(g[x][y][k], g[x + 1][y][k]);
        cmax(g[x][y][k], g[x][y - 1][k]);
      }
    }
  }
  memset(f, -1, sizeof f);
  cout << dfs(1, n);
}
```

### P2851

做两次背包即可，每次上界均为 $t + \max v_i^2$。

当老板要找的钱多于 $\max v_i^2$ 时，则其找的硬币数量必然 $> \max v_i$，假设其每个硬币找了 $p_i$ 个，对其求前缀和 $s_i$，由于序列长度 $> \max v_i$，而取模结果只有 $\max v_i$ 种，所以必然有 $i < j, s_i\equiv s_j \pmod {\max v_i}$，于是可以把这一段压成 $\dfrac {s_j - s_i}{\max v_i}$ 个 $\max v_i$，显然更优，因此不会超过 $\max v_i^2$。

同理，也不会付超过 $t + \max v_i^2$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 40009;
int n, t, v[N], c[N], f[N], g[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> t;
  for (int i = 1; i <= n; ++i) cin >> v[i];
  for (int i = 1; i <= n; ++i) cin >> c[i];
  int mxv = *max_element(v + 1, v + n + 1) + 4;
  mxv *= mxv;
  memset(f, 0x3f, sizeof f);
  f[0] = 0;
  for (int i = 1; i <= n; ++i) {
    for (int j = 1, p = 1; j <= c[i]; j += p, p = min(c[i] - j + 1, p << 1)) {
      for (int k = t + mxv; k >= p * v[i]; --k) cmin(f[k], f[k - v[i] * p] + p);
    }
  }
  memset(g, 0x3f, sizeof g);
  g[0] = 0;
  for (int i = 1; i <= n; ++i)
    for (int j = v[i]; j <= t + mxv; ++j) cmin(g[j], g[j - v[i]] + 1);
  int ans = 0x3f3f3f3f;
  for (int i = t; i <= t + mxv; ++i) {
    cmin(ans, f[i] + g[i - t]);
  }
  if (ans == 0x3f3f3f3f) cout << -1;
  else cout << ans;
}
```

### P2224
学到了！

考虑 dp，令 $f_{i, j}$ 表示做完前 $i$ 个，A 花了 $j$ 的时间，$B$ 所需的最小时间。

转移很简单，$f_{i, j} = \min(f_{i - 1, j} + t_2, f_{i - 1, j - t_1}, f_{i - 1, j - t_3} + t_3)$，滚动掉 $i$ 就可以了。

$O(n^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 3e4 + 9;
int n, t[3][N], f[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  int up = 0;
  for (int i = 1; i <= n; ++i) {
    cin >> t[0][i] >> t[1][i] >> t[2][i];
    up += max({t[0][i], t[1][i], t[2][i]});
  }
  memset(f, 0x3f, sizeof f);
  f[0] = 0;
  for (int i = 1; i <= n; ++i) {
    for (int j = up; j >= 0; --j) {
      if (t[1][i] == 0) f[j] = 0x3f3f3f3f;
      else f[j] += t[1][i];
      if (j >= t[0][i] && t[0][i] > 0) cmin(f[j], f[j - t[0][i]]);
      if (j >= t[2][i] && t[2][i] > 0) cmin(f[j], f[j - t[2][i]] + t[2][i]);
    }
  }
  int ans = 0x3f3f3f3f;
  for (int i = 0; i <= up; ++i) cmin(ans, max(f[i], i));
  cout << ans;
}
```

### P4170
dp，令 $f_{l, r}$ 表示 $[l, r]$ 的答案，显然有 $f_{l, r} = \min_{l \le k < r} f_{l, k} + f_{k + 1, r}$。

显然，上面的转移并没有包含全部涂一个色的情况，所以我们再手动转移一下即可。

具体地，直接记录一下每个区间内是否有某个颜色，然后考虑这次操作的颜色是和左右端点相同，如果我要的颜色已经涂过了就不用 $+1$，否则要。

$O(n^3)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 59;
int n, f[N][N], had[N][N][26];
string s;
int dfs(int l, int r) {
  if (l > r) return 0;
  if (l == r) return 1;
  auto &res = f[l][r];
  if (res < 0x3f3f3f3f) return f[l][r];
  for (int i = l; i < r; ++i) cmin(res, dfs(l, i) + dfs(i + 1, r));
  cmin(res, dfs(l + 1, r) + (had[l + 1][r][s[l] - 'a'] == 0));
  cmin(res, dfs(l, r - 1) + (had[l][r - 1][s[r] - 'a'] == 0));
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> s, n = s.size(), s = ' ' + s;
  for (int i = 1; i <= n; ++i)
    for (int j = i; j <= n; ++j) {
      for (int k = 0; k < 26; ++k) had[i][j][k] = had[i][j - 1][k];
      ++had[i][j][s[j] - 'a'];
    }
  memset(f, 0x3f, sizeof f);
  cout << dfs(1, n);
}
```

### P4158
容易发现我们只关心每一行涂了几次，具体怎么涂的不重要。于是考虑先对每一行 dp，令 $f_{i, j, k}$ 表示第 $i$ 行第 $j$ 列，涂了 $k$ 次的答案，转移直接找一个 $l < j$，然后假设把 $l + 1, j$ 全涂了的贡献即可。

对于所有行，我们再设一个 dp，$g_{i, j}$，表示涂完前 $i$ 行，涂了 $j$ 次的答案，每次转移枚举一下这一行涂了几次即可。

因为 $t$ 与 $n^2$ 同阶，所以是 $O(n^4)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 59;
int n, m, t, f[N][N][N], g[N][N * N];
int a[N][N];
int get(int l, int r, int p) { return max(a[p][r] - a[p][l - 1], r - l + 1 + a[p][l - 1] - a[p][r]); }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> t;
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
      char c;
      cin >> c;
      a[i][j] = c - '0' + a[i][j - 1];
    }
  }
  for (int i = 1; i <= n; ++i) {
    auto &dp = f[i];
    memset(dp, -0x3f, sizeof dp);
    dp[0][0] = 0;
    for (int j = 1; j <= m; ++j) {
      for (int k = 0; k <= m; ++k) {
        cmax(dp[j][k], dp[j - 1][k]);
        if (k == 0) continue;
        for (int l = 0; l < j; ++l)
          cmax(dp[j][k], dp[l][k - 1] + get(l + 1, j, i));
      }
    }
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= t; ++j) {
      for (int k = 0; k <= j && k <= m; ++k)
        cmax(g[i][j], g[i - 1][j - k] + f[i][m][k]);
    }
  }
  cout << g[n][t];
}
```

### P4095
首先这个最优化的背包，它不支持撤销，所以考虑维护前后缀背包，由于已知最大体积，所以合并两个背包是 $O(V)$ 的。

时间复杂度 $O(nV\log V + qV)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1009;
int n, a[N], b[N], c[N], f[N][N], g[N][N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i)
    cin >> a[i] >> b[i] >> c[i];
  for (int i = 1; i <= n; ++i) {
    memcpy(f[i], f[i - 1], sizeof f[i]);
    for (int j = 1, p = 1; j <= c[i]; j += p, p = min(p << 1, c[i] - j + 1)) {
      for (int k = N - 1; k >= p * a[i]; --k)
        cmax(f[i][k], f[i][k - p * a[i]] + p * b[i]);
    }
  }
  for (int i = n; i >= 1; --i) {
    memcpy(g[i], g[i + 1], sizeof g[i]);
    for (int j = 1, p = 1; j <= c[i]; j += p, p = min(p << 1, c[i] - j + 1)) {
      for (int k = N - 1; k >= p * a[i]; --k)
        cmax(g[i][k], g[i][k - p * a[i]] + p * b[i]);
    }
  }
  int q;
  cin >> q;
  while (q--) {
    int d, e;
    cin >> d >> e, ++d;
    int ans = 0;
    for (int i = 0; i <= e; ++i)
      cmax(ans, f[d - 1][i] + g[d + 1][e - i]);
    cout << ans << '\n';
  }
}
```

### P1772
点数很少，考虑状压。

首先，一共只有 $2^m$ 种码头状态，我们用 $O(2^m m\log m)$ 的时间把所有情况下 $1\to m$ 最短路求出来，也就是这种状态下的答案 $w_i$。

然后预处理出 $i$ 天有哪些码头是可以用的，然后开始 dp。

$f_{i, j}$ 表示第 $i$ 天，码头状态为 $j$ 的答案，$g_i$ 表示第 $i$ 天的答案。显然 $g_i = \min f_{i, j}$，转移可以选择不改变，$f_{i, j} = f_{i - 1, j} + w_j$；也可以选择上一次的最小答案 $f_{i, j} = g_{i - 1} + k + w_j$，这里不用管 $g_{i - 1}$ 是否和 $j$ 一样，如果一样会被前一半转移到。

$O((n + m\log m)2^m)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 109;
int n, m, k, e, been[N], dst[29], val[1 << 20], f[N], g[1 << 20], h[1 << 20];
vector<pair<int, int>> es[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> k >> e;
  for (int i = 1; i <= e; ++i) {
    int x, y, z;
    cin >> x >> y >> z;
    --x, --y;
    es[x].emplace_back(y, z), es[y].emplace_back(x, z);
  }
  for (int i = 1; i <= n; ++i) been[i] = (1 << m) - 1;
  int d;
  cin >> d;
  for (int i = 1; i <= d; ++i) {
    int a, b, p;
    cin >> p >> a >> b;
    for (int j = a; j <= b; ++j) been[j] ^= 1 << (p - 1);
  }
  for (int i = 0; i < 1 << m; ++i) {
    priority_queue<pair<int, int>> q;
    memset(dst, 0x3f, sizeof dst);
    dst[0] = 0;
    q.push({0, 0});
    while (!q.empty()) {
      auto [d, x] = q.top();
      d = -d, q.pop();
      if (dst[x] != d || (i >> x & 1 ^ 1)) continue;
      for (auto [y, z] : es[x]) {
        if (dst[x] + z < dst[y]) {
          dst[y] = dst[x] + z;
          q.push({-dst[y], y});
        }
      }
    }
    val[i] = dst[m - 1];
  }
  memset(f, 0x3f, sizeof f);
  memset(g, 0x3f, sizeof g);
  memset(h, 0, sizeof h);
  f[0] = 0;
  for (int i = 1; i <= n; ++i) {
    for (int j = been[i]; j; j = been[i] & (j - 1)) {
      cmin(g[j], min(h[j], f[i - 1] + k) + val[j]);
      cmin(f[i], g[j]);
    }
    memcpy(h, g, sizeof g);
    memset(g, 0x3f, sizeof g);
  }
  cout << f[n];
}
```

### P2518
水题，直接 $0 \sim 9$ 的出现次数压成状态，最多有 $5^{10} \approx 9\times 10^6$ 种，于是直接数位 dp。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 59;
int len;
array<int, 10> cnt;
string n;
map<array<int, 10>, int> dp[N];
int dfs(int p, bool top) {
  if (p > len) return true;
  if (!top && dp[p].count(cnt)) return dp[p][cnt];
  int res = 0, up = top ? n[p] - '0' : 9;
  for (int i = 0; i <= up; ++i) {
    if (cnt[i] == 0) continue;
    --cnt[i];
    res += dfs(p + 1, top && i == up);
    ++cnt[i];
  }
  if (!top) dp[p][cnt] = res;
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n, len = n.size(), n = ' ' + n;
  for (int i = 1; i <= len; ++i) ++cnt[n[i] - '0'];
  cout << dfs(1, true) - 1;
}
```

### P1800
显然答案具有单调性，考虑二分答案，然后我们 dp，令 $f_{i, j}$ 表示前 $i$ 个人，软件 $1$ 做了 $j$ 个，做多可以做多少软件 $2$。

$O(nm^2\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 109;
int n, m, d1[N], d2[N], f[N];
bool chk(int x) {
  memset(f, -0x3f, sizeof f);
  f[0] = 0;
  for (int i = 1; i <= n; ++i) {
    for (int k = m; k >= 0; --k) {
      for (int j = 0; j <= k && j * d1[i] <= x; ++j) {
        cmax(f[k], f[k - j] + (x - j * d1[i]) / d2[i]);
      }
    }
  }
  return f[m] >= m;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i) cin >> d1[i] >> d2[i];
  int l = 1, r = 1e5;
  while (l < r) {
    int mid = (l + r) >> 1;
    if (chk(mid)) r = mid;
    else l = mid + 1;
  }
  cout << l;
}
```

### CF1132F
就是 P4170 涂色。
### UVA1437
P4170 加强。

把空串染色是好做的，而非空串我们肯定是一个一个区间的染。

于是可以 dp，$f_i$ 表示染了 $A$ 的前 $i$ 个，$f_i = \min f_j + w_{j + 1, i}$，$w_{l, r}$ 就是把 $l, r$ 当空串的染色次数。

$O(n^3)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 109;
int f[N][N], g[N];
string s, t;
int dfs(int l, int r) {
  if (l == r) return 1;
  if (f[l][r] < 0x3f3f3f3f) return f[l][r];
  auto &res = f[l][r];
  for (int i = l; i < r; ++i)
    cmin(res, dfs(l, i) + dfs(i + 1, r));
  if (t[l] == t[r]) cmin(res, min(dfs(l + 1, r), dfs(l, r - 1)));
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  while (cin >> s >> t) {
    int n = s.size();
    s = ' ' + s, t = ' ' + t;
    memset(f, 0x3f, sizeof f);
    memset(g, 0x3f, sizeof g);
    g[0] = 0;
    for (int i = 1; i <= n; ++i) {
      g[i] = g[i - 1] + (s[i] != t[i]);
      for (int k = 0; k < i; ++k) {
        cmin(g[i], g[k] + dfs(k + 1, i));
      }
    }
    cout << g[n] << '\n';
  }
}
```

### CF280C
期望考虑拆贡献。

首先每个点最多被选择一次，记 $f_i = 0/1$ 表示 $i$ 是否被选，那么答案即为 $E(\sum f_i) = \sum E(f_i)$，而 $E(f_i)$ 即为 $i$ 被选的概率。

考虑把所有选择构成一个排列 $p$，每次相当于从中选择第一个没有删去的。

那么显然 $f_i = 1$ 当且仅当其祖先晚于其被选择，即在 $p$ 中排名大于 $i$。

由于除此之外的点没有限制，所以我们只考虑 $i$ 和其祖先共 $dep_i$ 个点，那么 $i$ 排在第一个的概率即为 $\dfrac {(dep_i - 1)!}{dep_i!} = \dfrac 1{dep_i}$。

答案即为 $\sum \dfrac 1{dep_i}$。

$O(n)$

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
#define d64 long double
d64 ans;
int n, dep[N];
vector<int> es[N];
void dfs(int x, int ff) {
  dep[x] = dep[ff] + 1;
  ans += 1. / dep[x];
  for (int y : es[x])
    if (y ^ ff) dfs(y, x);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1, x, y; i < n; ++i)
    cin >> x >> y, es[x].push_back(y), es[y].push_back(x);
  dfs(1, 0);
  cout << fixed << setprecision(20) << ans;
}
```

### CF547C
模拟赛场切了。

显然我们可以每次加入或删除时维护这个数与其它数的贡献，于是问题就变成求一个集合中与某个数 $x$ 互质的数。

然后这个东西显然可以容斥，我们考虑枚举 $x$ 的质因子的子集。由于值域很小 $V \leq 6\times 10^5$，所以本质不同的质因子个数 $\leq 7$，这就意味着我们可以 $2^7$ 次枚举子集做容斥。因为我们没有管一个质因子的指数，所以要预处理每个数的倍数个数。

但是这个做法细节多，比较唐，我们发现 $\sum_i [\gcd(x, a_i) = 1] = \sum_i \sum_{d \mid x, d\mid a_i} \mu(d) = \sum_{d \mid x} \mu(d) \sum_i [d \mid a_i]$，于是每次枚举 $x$ 的因子，然后后面的用桶存一下即可。

$O(n\sqrt n)$

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define pc(x) __builtin_popcount(x)
constexpr int N = 2e5 + 9, V = 5e5 + 9;
int n, q, c, a[N], pr[N], mn[V], cnt[V], ans, num;
bool ins[N];
vector<int> p[N], e[N];
void add(int x) {
  const int sz = p[x].size();
  int res = num;
  for (int i = 1; i < 1 << sz; ++i) {
    int ret = 1;
    for (int j = 0; j < sz; ++j) {
      if (i >> j & 1) ret *= p[x][j];
    }
    res += (pc(i) & 1 ? -1 : 1) * cnt[ret];
  }
  ++num, ans += res;
  for (int i : e[x]) ++cnt[i];
}
void del(int x) {
  const int sz = p[x].size();
  for (int i : e[x]) --cnt[i];
  int res = --num;
  for (int i = 1; i < 1 << sz; ++i) {
    int ret = 1;
    for (int j = 0; j < sz; ++j) {
      if (i >> j & 1) ret *= p[x][j];
    }
    res += (pc(i) & 1 ? -1 : 1) * cnt[ret];
  }
  ans -= res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  for (int i = 2; i < V; ++i) {
    if (!mn[i]) {
      pr[++c] = mn[i] = i;
      for (int j = i + i; j < V; j += i)
      if (!mn[j]) mn[j] = i;
    }
  }
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
    int u = a[i];
    while (u > 1) {
      int t = mn[u];
      p[i].push_back(t);
      while (u % t == 0) u /= t;
    }
    for (int j = 1; j * j <= a[i]; ++j) {
      if (a[i] % j == 0) {
        e[i].push_back(j);
        if (j * j != a[i]) e[i].push_back(a[i] / j);
      }
    }
  }
  while (q--) {
    int x;
    cin >> x;
    if (ins[x]) del(x);
    else add(x);
    ins[x] ^= 1;
    cout << ans << '\n';
  }
}
```

### P3008
模拟赛题，场切了。

由于保证了不会通过负权边形成环，所以将正权边连的所成一个点后，图是一个 DAG，这样我们可以拓扑排序求 DAG 最短路，每个点内部用 dijkstra 跑。

具体地，我们在拓扑排序过程中存一个点集 $S$，表示所有通过负权边可达的点，然后以这个点集为起点跑多源最短路，并且更新其所有出边的连通块的点集，细节比较多。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long

constexpr int N = 2.5e4 + 9;
int n, r, p, s, m, dst[N], bel[N], ind[N], ans[N];
vector<int> blk[N];
vector<pair<int, int>> es[N];
vector<tuple<int, int, int, int>> e[N];
void dij(int bl, const vector<pair<int, int>> &st) {
  priority_queue<pair<int, int>> q;
  // for (int i : blk[bl]) dst[i] = 0x3f3f3f3f3f3f3f3f;
  for (auto [x, y] : st) dst[x] = min(dst[x], y);
  for (auto [x, y] : st)
    if (dst[x] == y) q.emplace(-dst[x], x);
  while (!q.empty()) {
    auto [d, x] = q.top();
    q.pop(), d = -d;
    if (d != dst[x]) continue;
    for (auto [y, z] : es[x])
      if (dst[y] > dst[x] + z) {
        dst[y] = dst[x] + z;
        q.emplace(-dst[y], y);
      }
  }
}
void dfs(int x, int c) {
  bel[x] = c, blk[c].push_back(x);
  for (auto [y, z] : es[x])
    if (!bel[y]) dfs(y, c);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> r >> p >> s;
  for (int i = 1; i <= r; ++i) {
    int x, y, z;
    cin >> x >> y >> z;
    es[x].emplace_back(y, z);
    es[y].emplace_back(x, z);
  }
  for (int i = 1; i <= n; ++i) {
    if (!bel[i]) dfs(i, ++m);
    // cerr << bel[i] << ' ';
  }
  // cerr << '\n';
  for (int i = 1; i <= p; ++i) {
    int x, y, z;
    cin >> x >> y >> z;
    e[bel[x]].emplace_back(bel[y], y, x, z);
    ++ind[bel[y]];
  }
  memset(dst, 0x3f, sizeof dst);
  map<int, vector<pair<int, int>>> mp;
  mp[bel[s]].emplace_back(s, 0);
  queue<int> q;
  for (int i = 1; i <= m; ++i)
    if (!ind[i]) q.push(i);
  while (!q.empty()) {
    int x = q.front();
    q.pop();
    auto st = mp[x];
    dij(x, st);
    // cerr << x << ' ' << dst[1] << '\n';
    for (auto [y1, y2, x1, z] : e[x]) {
      mp[y1].emplace_back(y2, dst[x1] + z);
      if (!--ind[y1]) q.push(y1);
    }
  }
  for (int i = 1; i <= n; ++i) {
    if (dst[i] > 2e9) cout << "NO PATH" << '\n';
    else cout << dst[i] << '\n';
  }
}
```

### P7098
被放在了普及组模拟赛 T4，不过场切了。

考虑状压，令 $f_{i, j}$ 表示当前放第 $i$ 层，已经放了 $j$ 集合中的路线的最小花费。

需要一些比较麻烦的预处理，写的不太好有点卡常。

$O(n^22^n + n3^n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define pc(x) __builtin_popcount(x)
constexpr int N = 29, M = 1e5 + 9;
int n, m, a[N][M];
long long dp[N][1 << 14], val[1 << 14][N], Val[N][N];
bool ok[1 << 14], can[N][N];
vector<int> ru[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) cin >> a[i][j];
  }
  for (int i = 0; i < n; ++i) {
    int sz;
    cin >> sz;
    ru[i].resize(sz);
    for (int j = 0; j < sz; ++j) {
      cin >> ru[i][j], --ru[i][j];
      for (int k = 0; k < n; ++k) {
        Val[i][k] += a[k][ru[i][j]];
      }
    }
  }
  for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j) can[i][j] = 1;
  for (int i = 0; i < n; ++i) {
    map<int, int> mp;
    for (int k : ru[i]) mp[k] = 1;
    for (int j = 0; j < n; ++j) {
      if (i == j) continue;
      for (int k : ru[j]) {
        if (mp[k]) {
          can[i][j] = 0;
          break;
        }
      }
    }
  }
  for (int i = 0; i < 1 << n; ++i) {
    ok[i] = 1;
    vector<int> vec;
    for (int j = 0; j < n; ++j) {
      if (i >> j & 1) {
        vec.push_back(j);
        for (int k = 0; k < n; ++k) val[i][k + 1] += Val[j][k];
      }
    }
    // cerr << vec.size() << '\n';
    for (auto j : vec) {
      if (!ok[i]) break;
      for (auto k : vec) {
        // cerr << i << ' ' << k << ' ' << can[i][k] << '\n';
        if (!can[j][k]) ok[i] = 0;
        if (!ok[i]) break;
      }
    }
    // cerr << i << ' ' << ok[i] << '\n';
  }
  // cerr << ok[1 << 1];
  memset(dp, 0x3f, sizeof dp);
  dp[0][0] = 0;
  for (int i = 0; i < 1 << n; ++i) {
    for (int j = 1; j <= n; ++j) {
      if ()
      cmin(dp[j][i], dp[j - 1][i]);
      for (int k = i; k; k = (k - 1) & i) {
        if (!ok[k]) continue;
        cmin(dp[j][i], dp[j - 1][i ^ k] + val[k][j]);
      }
    }
  }
  long long ans = 0x3f3f3f3f3f3f3f3f;
  for (int i = 0; i <= n; ++i) cmin(ans, dp[i][(1 << n) - 1]);
  cout << ans;
}
```

### CF2150C
考虑 dp，令 $f_{i, j}$ 表示已经选了 $b_1, \dots, b_j$，现在考虑 $a_i$ 的最大价值。

首先考虑 $a_i$ 能不能选，令 $b_{p_i} = a_i$，则 $a_i$ 能选当且仅当 $p_i > j$。

于是若 $p_i > j$，$f_{i, j} = f_{i - 1, j} + v_{a_i}$。

若 $p_i = j$，$f_{i, j} = \max\limits_{k \le j} f_{i - 1, k}$，也就是考虑上一次 $B$ 选的是什么。这样可能 $b_{k + 1}, \dots, b_{j - 1}$ 并没有都被 $A$ 选了，不过这样没关系，因为我们取最大所以这种不优的情况最后会被舍掉。

若 $p_i < j$，$f_{i, j} = f_{i - 1, j}$。

于是直接线段树维护即可。

$O(n\log n)$

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 2e5 + 9;
int n, v[N], a[N], b[N], pb[N], p[N], sgt[N << 2], tg[N << 2];
void build(int u, int l, int r) {
  sgt[u] = tg[u] = 0;
  if (l == r) return ;
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
}
void apply(int u, int z) { sgt[u] += z, tg[u] += z; }
void down(int u) {
  if (tg[u]) apply(u << 1, tg[u]), apply(u << 1 | 1, tg[u]), tg[u] = 0;
}
void update1(int u, int l, int r, int x, int y, int z) {
  if (x <= l && r <= y) return apply(u, z);
  int m = (l + r) >> 1;
  down(u);
  if (m >= x) update1(u << 1, l, m, x, y, z);
  if (m < y) update1(u << 1 | 1, m + 1, r, x, y, z);
  sgt[u] = max(sgt[u << 1], sgt[u << 1 | 1]);
}
void update2(int u, int l, int r, int x, int y) {
  if (l == r) return sgt[u] = y, void();
  int m = (l + r) >> 1;
  down(u);
  if (m >= x) update2(u << 1, l, m, x, y);
  else update2(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = max(sgt[u << 1], sgt[u << 1 | 1]);
}
int query(int u, int l, int r, int x, int y) {
  if (x <= l && r <= y) return sgt[u];
  int m = (l + r) >> 1;
  down(u);
  if (m >= x && m < y) return max(query(u << 1, l, m, x, y), query(u << 1 | 1, m + 1, r, x, y));
  else if (m >= x) return query(u << 1, l, m, x, y);
  else return query(u << 1 | 1, m + 1, r, x, y);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n;
    for (int i = 1; i <= n; ++i) cin >> v[i];
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int i = 1; i <= n; ++i) cin >> b[i], pb[b[i]] = i;
    for (int i = 1; i <= n; ++i) p[i] = pb[a[i]];

    build(1, 0, n);
    for (int i = 1; i <= n; ++i) {
      update2(1, 0, n, p[i], query(1, 0, n, 0, p[i]));
      update1(1, 0, n, 0, p[i] - 1, v[a[i]]);
    }
    cout << query(1, 0, n, 0, n) << '\n';
  }
}
```

### CF1704E
首先不能直接拓扑排序，因为有的点一开始是 $0$，但是后来某个时刻可能又有值了，所以不能直接拓扑。

我们考虑这种点什么时候又有值了，显然对于两个点 $u, v$，如果 $a_v = 0$，那么从 $\text{dist}(u, v)$ 时刻开始，$a_u$ 中的值就到 $v$ 了，$\text{dist}$ 最大为 $n$，所以从 $n$ 时刻开始，这种点就不存在了。

于是我们直接模拟前 $n$ 个时刻，然后开始拓扑排序。

$O(n^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1009, md = 998244353;
int n, m, a[N], d[N], o[N], c;
vector<int> es[N];
queue<int> q;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n >> m, c = 0;
    for (int i = 1; i <= n; ++i) cin >> a[i], d[i] = 0, es[i].clear();
    for (int i = 1, x, y; i <= m; ++i) {
      cin >> x >> y, es[x].push_back(y), ++d[y];
    }
    for (int i = 1; i <= n; ++i)
      if (!d[i]) q.push(i);
    while (!q.empty()) {
      int x = q.front();
      q.pop(), o[++c] = x;
      for (int y : es[x])
        if (!--d[y]) q.push(y);
    }
    bool ok = false;
    for (int k = 0; k < n; ++k) {
      if (count(a + 1, a + n + 1, 0) == n) {
        cout << k << '\n';
        ok = true;
        break;
      }
      vector<int> p;
      for (int i = 1; i <= n; ++i)
        if (a[i] > 0) p.push_back(i);
      for (int i : p) {
        --a[i];
        for (int y : es[i]) ++a[y];
      }
    }
    for (int i = 1; i <= c; ++i) {
      for (int y : es[o[i]]) (a[y] += a[o[i]]) %= md;
    }
    if (!ok) cout << (a[o[c]] + n) % md << '\n';
  }
}
```

### CF1706D2

考虑枚举最小值，然后对于每个数，$\lfloor \dfrac {a_i}{p_i}\rfloor \ge \min \Rightarrow p_i \le \lfloor \dfrac {a_i} {\min}\rfloor\le \lfloor \dfrac {a_n}{\min}\rfloor$，而 $\sum_{i = 1} ^ n \lfloor \dfrac ni \rfloor = O(n\log  n)$。而 $p_i$ 可以分为许多连续段，每段均相同，我们可以枚举每一段，也就是此时 $p_I$ 的值域，然后用二分得到这一段的最大值。

$O(n\log^2 n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1e5 + 9;
int n, k, a[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n >> k;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    n = unique(a + 1, a + n + 1) - a - 1;
    int mx = 0, mn = 0x3f3f3f3f;
    for (int i = 1; i <= n; ++i) mx = max(mx, a[i] / k), mn = min(mn, a[i] / k);
    int ans = mx - mn;
    for (int i = 1; i <= a[1]; ++i) {
      mx = a[n] / k;
      for (int j = 1; j <= k && j <= a[n] / i; ++j) {
        mx = max(mx, a[lower_bound(a + 1, a + n + 1, (j + 1) * i) - a - 1] / j);
      }
      ans = min(ans, mx - i);
    }
    cout << ans << '\n';
  }
}
```

### ABC403G
不想打平衡树，于是直接分块，每个块长度超过 $2\sqrt n$ 就直接重构，时间复杂度 $O(n\sqrt n)$。

每次插入时，如果直接暴力 sort 的话会带 $\log$，直接炸掉，所以要写归并之类的。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 3e5 + 9, V = 1e9, S = 548;
int Q, n, a[N / S + 9][2 * S + 9], cnt[N / S + 9], bel[N], mxb, st[N / S + 9], ed[N / S + 9], b[N], su[N / S + 9][2];
void rebuild() {
  int c = 0;
  for (int i = 1; i <= mxb; ++i) {
    for (int j = 1; j <= cnt[i]; ++j) {
      b[++c] = a[i][j];
    }
    su[i][0] = su[i][1] = 0;
    cnt[i] = 0;
  }
  assert(n == c);
  for (int i = 1; i <= n; ++i) {
    bel[i] = (i - 1) / S + 1;
    a[bel[i]][++cnt[bel[i]]] = b[i];
    su[bel[i]][i & 1] += b[i];
  }
  mxb = bel[n];
}
void insert(int x, int y) {
  a[x][++cnt[x]] = y;
  inplace_merge(a[x] + 1, a[x] + cnt[x], a[x] + cnt[x] + 1);
  bel[++n] = x, su[x][0] = su[x][1] = 0;
  int sz = 0;
  for (int i = 1; i < x; ++i) sz += cnt[i];
  for (int j = 1; j <= cnt[x]; ++j) su[x][(sz + j) % 2] += a[x][j];
  for (int i = x + 1; i <= mxb; ++i) {
    swap(su[i][0], su[i][1]);
  }
  if (cnt[x] > 2 * S) rebuild();
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> Q;
  mxb = 1;
  int z = 0;
  while (Q--) {
    int y, x;
    cin >> y;
    x = (y + z) % V + 1;
    int cur = 1;
    while (cur < mxb && a[cur][cnt[cur]] < x) ++cur;
    insert(cur, x);
    int ans = 0, be = 0;
    for (int i = 1; i <= mxb; ++i) ans += su[i][1];
    cout << (z = ans) << '\n';
  }
}
```

### 24 点（midnight）
模拟赛题，很可做啊。

首先显然除了 $1$ 以外的所有数都会使答案变大，所以我们先统计所有大于 $1$ 的点权之和，如果大于 $z$ 那么必然无解。

接下来不考虑以上这种无解的情况。

然后考虑 $1$，由于 $m \le 30$ 所以此时长度超过 $m$ 的必然有解，可以通过把一些 $\times 1$ 改成 $+1$ 来实现。

于是所有长度 $\ge m$ 的都有解。

那么对于长度 $\le m$ 的，我们可以直接暴力 $O(qm^2)$。

总时间复杂度 $O(q(\log n + m^2))$，$q \le 10^6, m \le 30$ 由于给了 $4$ s，所以冲过去了。

可以继续优化，$m \le 30$，而且状态是 $0/1$，所以直接拿 int 状压，然后加很简单，乘的话，我们发现 $\times 1$ 是简单的，对于 $\ge 2$ 的情况，只有 $1 \sim \lfloor m2 \rfloor$ 是有用的，于是我们可以直接预处理出这些状态对于不同的乘数的转移，然后就可以去掉一个 $m$。

时间复杂度 $O(m^22^{\frac m2} + q(\log n + m))$

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e6 + 9;
int n, m, q, a[N], fa[N], dep[N], dfn[N], idx, mi[20][N], sz[N], c[N], c1[N];
int h[1 << 16][31];
bool vis[N];
vector<int> es[N];
void update1(int x, int y) { for (; x <= n; x += x & -x) c1[x] += y; }
int query1(int x, int r = 0) { for (; x > 0; x -= x & -x) r += c1[x]; return r; }
void update(int x, int y) { for (; x <= n; x += x & -x) c[x] += y; }
int query(int x, int r = 0) { for (; x > 0; x -= x & -x) r += c[x]; return r; }
int dfs(int x, int ff, int d = 0, int b = 0) {
  fa[x] = ff, dep[x] = dep[ff] + 1, mi[0][dfn[x] = ++idx] = ff;
  b += a[x] > 1 ? a[x] : 0, d += a[x];
  update(dfn[x], d), update(dfn[x] + 1, -d);
  update1(dfn[x], b), update1(dfn[x] + 1, -b);
  for (int y : es[x])
    if (y ^ ff) sz[x] += dfs(y, x, d, b);
  return ++sz[x];
}
int get(int x, int y) { return dfn[x] < dfn[y] ? x : y; }
int lca(int x, int y) {
  if (x == y) return x;
  if ((x = dfn[x]) > (y = dfn[y])) swap(x, y);
  int d = __lg(y - ++x + 1);
  return get(mi[d][x], mi[d][y - (1 << d) + 1]);
}
int query(int x, int y, int z) {
  int f = lca(x, y);
  int d = query(dfn[x]) + query(dfn[y]) - query(dfn[f]) - query(dfn[fa[f]]);
  int d1 = query1(dfn[x]) + query1(dfn[y]) - query1(dfn[f]) - query1(dfn[fa[f]]);
  // cerr << x << ' ' << y << ' ' << z << ' ' << f << '\n';
  // cerr << "d: " << d << ' ' << "d1: " << d1 << '\n';
  if (d1 <= z && z <= d) return 1;
  if (d1 > z) return 0;
  return -1;
}
signed main() {
#ifndef LOCAL
  freopen("midnight.in", "r", stdin);
  freopen("midnight.out", "w", stdout);
#endif
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> q;
  for (int i = 0; i < 1 << 16; ++i) {
    for (int j = 2; j <= m; ++j) {
      for (int k = 0; k * j <= m; ++k) {
        if ((i >> k & 1) && k * j <= m) h[i][j] |= 1 << (k * j);
      }
    }
  }
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i < n; ++i) {
    int x, y;
    cin >> x >> y;
    es[x].push_back(y), es[y].push_back(x);
  }
  dfs(1, 0);
  for (int i = 1; i < 20; ++i) {
    for (int j = 1; j <= n; ++j) mi[i][j] = get(mi[i - 1][j], mi[i - 1][j + (1 << (i - 1))]);
  }
  while (q--) {
    int o, x, y, z;
    cin >> o >> x >> y;
    if (o == 1) update(dfn[x], y - a[x]), update(dfn[x] + sz[x], a[x] - y), update1(dfn[x], (y > 1 ? y : 0) - (a[x] > 1 ? a[x] : 0)), update1(dfn[x] + sz[x], (a[x] > 1 ? a[x] : 0) - (y > 1 ? y : 0)), a[x] = y;
    else {
      cin >> z;
      if (int res = query(x, y, z); ~res) {
        cout << res << '\n';
        continue;
      }
      bool ch = 0;
      if (dep[x] < dep[y]) swap(x, y), ch = 1;
      vector<int> ls, rs;
      int ffa = 0, tx = x, ty = y;
      while (dep[x] > dep[y]) {
        x = fa[x];
      }
      if (x == y) ffa = x;
      while (fa[x] != fa[y]) {
        x = fa[x], y = fa[y];
      }
      if (x != y) ffa = fa[x];
      x = tx, y = ty;
      if (ch) swap(x, y);
      for (; x != ffa; x = fa[x]) ls.push_back(x);
      for (; y != ffa; y = fa[y]) rs.push_back(y);
      ls.push_back(ffa);
      vector<int> vec = ls;
      reverse(rs.begin(), rs.end());
      for (int i : rs) vec.push_back(i);
      int f = 1 << a[vec[0]];
      for (size_t i = 1; i < vec.size(); ++i) {
        int g = f; f = 0;
        if (a[vec[i]] == 1) f = g;
        f |= g << a[vec[i]];
        f |= h[g & ((1 << 16) - 1)][a[vec[i]]];
      }
      // cerr << '\n';
      cout << (f >> z & 1) << '\n';
    }
  }
}
```

-----------

2025.10.31

### P4269

对 $s_i$ 做扫描线，然后把 $> s_i$ 的位置删掉，剩下的点之间的相邻间隔超过 $d_i$ 就不可以，链表维护一下就可以了。

$O(n \log n)$，瓶颈在排序。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
int n, m, mx, a[N], o[N], ans[N], nxt[N], pre[N];
struct shoes {
  int s, d, i;
} b[N];
void del(int x) {
  cmax(mx, nxt[x] - pre[x]);
  nxt[pre[x]] = nxt[x], pre[nxt[x]] = pre[x];
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i) cin >> a[i], o[i] = i, nxt[i] = i + 1, pre[i] = i - 1;
  sort(o + 1, o + n + 1, [&](int x, int y) -> bool { return a[x] > a[y]; });
  for (int i = 1; i <= m; ++i) cin >> b[i].s >> b[i].d, b[i].i = i;
  sort(b + 1, b + m + 1, [&](auto x, auto y) -> bool { return x.s > y.s; });
  for (int i = 1, j = 0; i <= m; ++i) {
    while (j < n && a[o[j + 1]] > b[i].s) del(o[++j]);
    ans[b[i].i] = b[i].d >= mx;
  }
  for (int i = 1; i <= m; ++i) cout << ans[i] << '\n';
}
```

### CF985F
同构等价于对于每个字母 $c$ 存在一个字母 $c'$，他们出现的位置相同。

于是直接哈希记录每个字母的出现，然后把所有字母都算一遍最后判一下集合是否相等即可。

$O(n|\sum|)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
using u64 = uint64_t;
struct hash_t {
  static constexpr u64 md = (1LL << 61) - 1;
  u64 h;
  constexpr hash_t() : h(0) {}
  constexpr hash_t(u64 v) : h(v % md) {}
  hash_t operator+(const hash_t &x) const { return (h + x.h) >= md ? h + x.h - md : h + x.h; }
  hash_t operator-(const hash_t &x) const { return h >= x.h ? h - x.h : h + md - x.h; }
  hash_t operator*(const hash_t &x) const {
    __int128 tmp = h; tmp *= x.h;
    u64 r = u64(tmp & md) + u64(tmp >> 61);
    return r >= md ? r - md : r;
  }
};
constexpr int N = 2e5 + 9;
constexpr hash_t seed = 131ULL;
constexpr u64 msk = 131881937;
int n, m, p[26][N], cnt[26];
hash_t h[26][N], pw[N];
string s;
u64 shift(u64 x) {
  return x ^= msk, x ^= x << 5, x ^= x >> 11, x ^= x << 54, x ^= msk;
}
hash_t get(int q, int l, int r) { return h[q][r] - h[q][l - 1] * pw[r - l + 1]; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  cin >> s, s = ' ' + s;
  pw[0] = 1;
  for (int i = 1; i <= n; ++i) pw[i] = pw[i - 1] * seed;
  for (int i = 0; i < 26; ++i) {
    for (int j = 1; j <= n; ++j) h[i][j] = h[i][j - 1] * seed + shift(s[j] - 'a' == i);
  }
  while (m--) {
    int x, y, len;
    cin >> x >> y >> len;
    vector<u64> ls, rs;
    for (int i = 0; i < 26; ++i) ls.push_back(get(i, x, x + len - 1).h);
    for (int i = 0; i < 26; ++i) rs.push_back(get(i, y, y + len - 1).h);
    sort(ls.begin(), ls.end()), sort(rs.begin(), rs.end());
    if (ls == rs) cout << "YES\n";
    else cout << "NO\n";
  }
}
```

### P4302
区间 dp，如果当前区间可以折叠就取最小即可。

$O(n^4)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 109;
int f[N][N], n;
string s;
int dfs(int l, int r) {
  if (f[l][r]) return f[l][r];
  auto &res = f[l][r] = r - l + 1;
  for (int k = l; k < r; ++k) cmin(res, dfs(l, k) + dfs(k + 1, r));
  for (int k = 1; k < r - l + 1; ++k) {
    if ((r - l + 1) % k) continue;
    bool ok = true;
    for (int j = l; j <= r; ++j) {
      ok &= s[j] == s[(j - l) % k + l];
    }
    if (ok) cmin(res, dfs(l, l + k - 1) + 3 + (int)(log10((r - l + 1) / k)));
  }
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> s, n = s.size(), s = ' ' + s;
  cout << dfs(1, n);
}
```

### P1654
考虑 $E((x + 1)^3) = E(x^3) + E(3x^2) + E(3x) + 1$，$E((x + 1)^2) = E(x^2) + E(2x) + 1$，$E(x + 1) = E(x) + 1$，于是我们可以维护 $E(x), E(x^2), E(x^3)$，直接递推即可。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define d64 long double
constexpr int N = 1e5 + 9;
int n;
d64 p, f[N], x1[N], x2[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> p;
    x1[i] = (x1[i - 1] + 1) * p, x2[i] = (x2[i - 1] + 2 * x1[i - 1] + 1) * p;
    f[i] = f[i - 1] + (3 * x2[i - 1] + 3 * x1[i - 1] + 1) * p;
  }
  cout << fixed << setprecision(1) << f[n];
}
```

### P5839
首先用 floyd 求出每个字符变化的最小花费。

然后考虑 dp，$f_i$ 表示 $i$ 结尾的答案，转移很简单直接枚举一段 $[j + 1, i]$ 以及要把它变成的颜色 $c$，$f_i = \min f_j + w(j + 1, i, c)$，$w(j + 1, i, c)$ 表示这一段的代价，用前缀和算一下即可。

容易发现 $w(l, r, c) = s_{r, c} - s_{l - 1, c}$，于是转移即为 $f_i = \min f_j + s_{i, c} - s_{j, c}$，我们令 $g_{i, c} = \min\limits_{j \le i} f_j - s_{j, c}$，简单前缀和就做完了。

$O(nm + m^3)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
int n, m, k, a[26][26], f[N], g[N][26], su[N][26];
string s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> k >> s;
  s = ' ' + s;
  for (int i = 0; i < m; ++i)
    for (int j = 0; j < m; ++j) cin >> a[i][j];
  for (int i = 0; i < m; ++i)
    for (int j = 0; j < m; ++j)
      for (int k = 0; k < m; ++k)
        cmin(a[j][k], a[j][i] + a[i][k]);
  for (int i = 1; i <= n; ++i)
    for (int j = 0; j < m; ++j) su[i][j] = su[i - 1][j] + a[s[i] - 'a'][j];
  memset(f, 0x3f, sizeof f);
  memset(g, 0x3f, sizeof g);
  f[0] = 0;
  for (int i = 0; i <= n; ++i) {
    for (int l = 0; l < m; ++l) {
      if (i >= k) cmin(f[i], su[i][l] + g[i - k][l]);
    }
    for (int j = 0; j < m; ++j) g[i][j] = min(g[i - 1][j], f[i] - su[i][j]);
  }
  cout << f[n];
}
```

### NewMoneySystem(TopCoder)
好神秘。

首先，假设第 $i$ 张纸币是 $x$ 元，那么第 $i + 1$ 张是 $qx$（$q \in \{2, 3, 4, 5\}$）。如果我们用了 $p > q$ 张 $i$，就可以换成 $\lfloor \dfrac pq \rfloor$ 张 $i + 1$，于是我们考虑记忆化搜索。

$f_{x, y}$ 表示现在要用 $x$ 张，还有 $y$ 种面值的答案。

那么初始时，我们全部用 $1$，要 $n$ 张，也就是 $f_{n, k - 1}$。

转移考虑本次 $q$，$f_{x, y} = \min\limits_q f_{\lfloor\frac xq\rfloor, y - 1} + x \bmod q$。

时间复杂度不太懂，不过由于每次 $n$ 至少减半，可能是 $O(k\log^4 n)$ 的？

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
int n, k;
map<pair<int, int>, int> mp;
int dfs(int x, int y) {
  if (mp.count({x, y})) return mp[{x, y}];
  if (y == 0) return x;
  int res = 0x3f3f3f3f3f3f3f3f;
  for (int i = 2; i <= 5; ++i) cmin(res, dfs(x / i, y - 1) + x % i);
  return mp[{x, y}] = res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> k;
  cout << dfs(n, k - 1);
}
```

### P2051
首先注意到每一行每一列最多放两个，然后开始 dp。

$f_{i, j, k}$ 表示前 $i$ 行，$j$ 列放了 $1$ 个，$k$ 列放了 $2$ 个，$m - j - k$ 列没放。

转移考虑分类讨论这一行放几个放在那几列即可。

细节不多，$O(n^3)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 109, md = 9999973;
#define int long long
int n, m, f[N][N][N];
void update(int &x, int y) { x += y; x >= md ? x -= md : 0; }
int choose(int x) { return (x * (x - 1) / 2) % md; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  f[0][0][0] = 1;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j <= m; ++j) {
      for (int k = 0; k + j <= m; ++k) {
        update(f[i + 1][j][k], f[i][j][k]); // none
        update(f[i + 1][j + 1][k], f[i][j][k] * (m - j - k) % md); // one in empty
        if (j > 0) update(f[i + 1][j - 1][k + 1], f[i][j][k] * j % md); // one in one
        update(f[i + 1][j + 2][k], f[i][j][k] * choose(m - j - k) % md); // two in empty
        update(f[i + 1][j][k + 1], f[i][j][k] * j % md * (m - j - k) % md); // one in one, one in empty
        if (j > 1) update(f[i + 1][j - 2][k + 2], f[i][j][k] * choose(j) % md); // two in one
      }
    }
  }
  int ans = 0;
  for (int i = 0; i <= m; ++i)
    for (int j = 0; j + i <= m; ++j) update(ans, f[n][i][j]);
  cout << ans;
}
```

### P4441
直接 dp，$f_{i, j, k}$ 表示 $(i, j)$ 时，左括号个数减右括号个数为 $k$ 的最大长度。

输出方案直接用优先队列跑 bfs，这样每次最先到达一个状态的一定是最优的。

$O(r^2c)$

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 309;
int n, m, f[N][N][N];
char s[N][N];
bool vis[N][N][N];
struct state {
  string s;
  int x, y, k;
  state(string _s = "", int _x = 0, int _y = 0, int _k = 0) : s(_s), x(_x), y(_y), k(_k) {}
  bool operator<(const state &r) const {
    if (s.size() < r.s.size()) return 0;
    if (s.size() > r.s.size()) return 1;
    return s > r.s;
  }
};
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j) cin >> s[i][j];
  memset(f, -0x3f, sizeof f);
  for (int i = 1; i <= m; ++i) {
    if (s[n][i] == 'M') f[n][i][0] = 0;
  }
  for (int i = n - 1; i >= 1; --i) {
    for (int j = 1; j <= m; ++j) {
      for (int k = 0; k <= n; ++k) {
        if (s[i][j] == '(' && k > 0) cmax(f[i][j][k], 1 + max({f[i + 1][j - 1][k - 1], f[i + 1][j + 1][k - 1], f[i + 1][j][k - 1]}));
        if (s[i][j] == ')') cmax(f[i][j][k], 1 + max({f[i + 1][j - 1][k + 1], f[i + 1][j][k + 1], f[i + 1][j + 1][k + 1]}));
        if (s[i][j] == '.') cmax(f[i][j][k], max({f[i + 1][j - 1][k], f[i + 1][j][k], f[i + 1][j + 1][k]}));
      }
    }
  }
  int ans = 0;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j) cmax(ans, f[i][j][0]);
  priority_queue<state> q;
  vector<string> vec;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j)
      if (f[i][j][0] == ans) q.push({"", i, j, 0});
  while (!q.empty()) {
    auto [str, x, y, k] = q.top();
    q.pop();
    if (vis[x][y][k]) continue;
    vis[x][y][k] = 1;
    if (s[x][y] == 'M') {
      vec.push_back(str);
      continue;
    }
    if (s[x][y] == '(' && k > 0) {
      if (f[x][y][k] == 1 + f[x + 1][y - 1][k - 1]) q.push({s[x][y] + str, x + 1, y - 1, k - 1});
      if (f[x][y][k] == 1 + f[x + 1][y + 1][k - 1]) q.push({s[x][y] + str, x + 1, y + 1, k - 1});
      if (f[x][y][k] == 1 + f[x + 1][y][k - 1]) q.push({s[x][y] + str, x + 1, y, k - 1});
    }
    if (s[x][y] == ')') {
      if (f[x][y][k] == 1 + f[x + 1][y - 1][k + 1]) q.push({s[x][y] + str, x + 1, y - 1, k + 1});
      if (f[x][y][k] == 1 + f[x + 1][y + 1][k + 1]) q.push({s[x][y] + str, x + 1, y + 1, k + 1});
      if (f[x][y][k] == 1 + f[x + 1][y][k + 1]) q.push({s[x][y] + str, x + 1, y, k + 1});
    }
    if (s[x][y] == '.') {
      if (f[x][y][k] == f[x + 1][y - 1][k]) q.push({str, x + 1, y - 1, k});
      if (f[x][y][k] == f[x + 1][y + 1][k]) q.push({str, x + 1, y + 1, k});
      if (f[x][y][k] == f[x + 1][y][k]) q.push({str, x + 1, y, k});
    }
  }
  sort(vec.begin(), vec.end());
  cout << ans << "\n" << vec[0];
}
```

### P2519
将 $a, b$ 转化一下，可以得到第 $i$ 个人的排名区间 $[a + 1, n - b]$，然后我们可以类似扫描线，把所有的左端点挂到右端点上，然后 dp，$f_r = \max f_{l - 1} + \min(cnt_{[l, r]}, r - l + 1)$，$cnt$ 表示区间出现的个数。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
int n, f[N];
map<pair<int, int>, int> cnt;
vector<int> l[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    int a, b;
    cin >> a >> b;
    int L = a + 1, R = n - b;
    if (++cnt[{L, R}] == 1) l[R].push_back(L);
  }
  for (int i = 1; i <= n; ++i) {
    f[i] = f[i - 1];
    for (int j : l[i]) cmax(f[i], f[j - 1] + min(i - j + 1, cnt[{j, i}]));
  }
  cout << n - f[n];
}
```

### P2943
注意到直接分 $n$ 组，答案为 $n$，所以 $K^2 \le n \Rightarrow K \le \sqrt n$。

然后考虑维护一个 $g_{i, j}$ 表示最小的满足 $[g_{i, j}, i]$ 有 $j$ 种不同的。这个可以递推，我们令 $p_i$ 表示最大的满足 $a_{p_i} = a_i$ 的下标，那么如果 $p_i \ge g_{i - 1, j}$ 则 $g_{i, j} = g_{i - 1, j}$，否则 $g_{i, j} = g_{i - 1, j - 1}$，特别地 $g_{i, 0} = i + 1$。

于是 $f_i = \min f_{g_{i, j} - 1} + j^2$，$g$ 可以滚掉一维。

$O(n\sqrt n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 4e4 + 9;
int n, m, p[N], f[N], g[N], pre[N], lst[N];
set<int> s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i) {
    cin >> p[i], pre[i] = lst[p[i]], lst[p[i]] = i;
  }
  memset(f, 0x3f, sizeof f), f[0] = 0;
  int S = sqrt(n);
  for (int i = 1; i <= S; ++i) g[i] = n;
  for (int i = 1; i <= n; ++i) {
    g[0] = i;
    for (int j = S; j >= 1; --j) {
      if (pre[i] >= g[j]) continue;
      g[j] = g[j - 1];
    }
    for (int j = 1; j <= S; ++j) cmin(f[i], f[g[j] - 1] + j * j);
  }
  cout << f[n];
}
```

### P8476

显然有一个 dp，令 $f_{i, j}$ 表示 $b_i = j$ 的答案，$f_{i, j} = \min\limits_{j \le k} f_{i - 1, k} + f(j, a_i)$。

我们令 $g_{i, j} = \min\limits_{j \le k} f_{i, k}$，那么就成了 $f_{i, j} = g_{i - 1, j} + f(j, a_i)$。

我们考虑把 $f$ 拆开：

1. 若 $j \ge a_i$，则 $f_{i, j} = g_{i - 1, j} + j - a_i$。
2. 若 $j < a_i$，则 $f_{i, j} = g_{i - 1, j} + C$。

那么再回来考虑 $g_{i, j}$，容易发现 1、2 两种转移分别具有单调性，于是我们求后缀 min 等价于覆盖一个区间。

具体地，$j \ge a_i$ 时都是单调的，而 $j < a_i$，时，我们可以找到最小的 $p$ 满足 $f_{i, p} \ge f_{i, a_i}$，于是取 min 相当于将 $[p, a_i)$ 赋值为 $f_{i, a_i}$。

综上，每次先分类转移，再求后缀 min，最终答案即为 $g_{n, 1}$。

用线段树维护，$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e6 + 9;
int n, C, a[N], b[N], sgt[N << 2];
struct tag {
  int as, ad, add;
  tag(int x = -1, int y = 0, int z = 0) : as(x), ad(y), add(z) {}
  tag operator+(const tag &x) const {
    if (x.as != -1) return x;
    tag z = *this;
    z.ad += x.ad, z.add += x.add;
    return z;
  }
} tg[N << 2];
void apply(int u, int r, tag z) {
  if (z.as != -1) sgt[u] = z.as;
  sgt[u] += z.ad + b[r] * z.add;
  tg[u] = tg[u] + z;
}
void down(int u, int l, int r) {
  int m = (l + r) >> 1;
  apply(u << 1, m, tg[u]), apply(u << 1 | 1, r, tg[u]);
  tg[u] = tag();
}
void update(int u, int l, int r, int x, int y, tag z) {
  if (x > y) return ;
  if (x <= l && r <= y) return apply(u, r, z);
  int m = (l + r) >> 1;
  down(u, l, r);
  if (m >= x) update(u << 1, l, m, x, y, z);
  if (m < y) update(u << 1 | 1, m + 1, r, x, y, z);
  sgt[u] = max(sgt[u << 1], sgt[u << 1 | 1]);
}
int query(int u, int l, int r, int x) {
  if (l == r) return sgt[u];
  int m = (l + r) >> 1;
  down(u, l, r);
  if (m >= x) return query(u << 1, l, m, x);
  else return query(u << 1 | 1, m + 1, r, x);
}
int find(int u, int l, int r, int p, int k) {
  if (r <= p && sgt[u] < k) return -1;
  if (l == r) return l;
  int m = (l + r) >> 1;
  down(u, l, r);
  int res = find(u << 1, l, m, p, k);
  if (~res) return res;
  if (m < p) res = find(u << 1 | 1, m + 1, r, p, k);
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> C;
  for (int i = 1; i <= n; ++i) cin >> a[i], b[i] = a[i];
  sort(b + 1, b + n + 1);
  for (int i = 1; i <= n; ++i) {
    int p = lower_bound(b + 1, b + n + 1, a[i]) - b;
    update(1, 1, n, p + 1, n, {-1, -a[i], 1});
    if (p == 1) continue;
    update(1, 1, n, 1, p - 1, {-1, C, 0});
    int k = query(1, 1, n, p);
    int ps = find(1, 1, n, p - 1, k);
    if (ps != -1) update(1, 1, n, ps, p - 1, {k, 0, 0});
  }
  cout << query(1, 1, n, 1);
}
```
