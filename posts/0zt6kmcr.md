---
title: "记录 续 续"
date: 2025-10-22T19:12:17+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/0zt6kmcr"
luogu_id: "0zt6kmcr"
---

[记录 续](https://www.luogu.com.cn/article/cn2jwcqz) 又要炸了。

-------

2025.10.22

### P5785
首先有 $O(n^2)$ dp，$f_i = \min_{j < i} f_j + s\sum_{k = j + 1}^n c_k + \sum_{k = j + 1}^i c_k \sum_{k = 1}^i t_k$。

对 $c, t$ 都做前缀和后，$f_i = \min f_j + s(c_n - c_j) + t_i(c_i - c_j)$。

变形之后可得 $t_ic_j + f_j - t_ic_i - c_ns = f_j - c_j s$，斜率优化。

由于 $t$ 可能为负，所以斜率没有单调性，用单调栈维护凸包然后二分出第一个斜率大于 $t_i$ 的点，这个点也就是直线与凸包的切点，也就是决策点。

由于 $c \ge 0$ ，所以还会出现 $x$ 坐标相同的点，此时要根据 $y$ 坐标相对大小判断其斜率是无穷大还是无穷小。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
#define d64 long double
constexpr d64 eps = 1e-10, inf = 1e18;
constexpr int N = 3e5 + 9;
int n, s, c[N], t[N], f[N], q[N], hd, tl;
int getx(int i) {
  return c[i];
}
int gety(int i) {
  return f[i] - c[i] * s;
}
d64 slope(int i, int j) {
  if (getx(i) == getx(j)) return getx(j) < getx(i) ? -inf : inf;
  return 1. * (gety(j) - gety(i)) / (getx(j) - getx(i));
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> s;
  for (int i = 1; i <= n; ++i) cin >> t[i] >> c[i], t[i] += t[i - 1], c[i] += c[i - 1];
  hd = tl = 1;
  for (int i = 1; i <= n; ++i) {
    int l = hd, r = tl;
    while (l < r) {
      int mid = (l + r) >> 1;
      if (slope(q[mid], q[mid + 1]) - eps <= t[i]) l = mid + 1;
      else r = mid;
    }
    int j = q[l];
    f[i] = f[j] + s * c[n] + t[i] * c[i] - t[i] * c[j] - c[j] * s;
    while (hd < tl && slope(q[tl - 1], q[tl]) - eps >= slope(q[tl], i)) --tl;
    q[++tl] = i;
  }
  cout << f[n];
}
```

### P3195
$(c_i - L)\times 2(c_j + 1) + f_i - (c_i - L)^2 = f_j + (c_j + 1) ^2$，转成函数形式，然后斜率优化。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
#define d64 long double
constexpr d64 eps = 1e-10;
constexpr int N = 5e4 + 9;
int n, L, c[N], hd, tl, q[N], f[N];
d64 getx(int i) { return 2 * (c[i] + 1); }
d64 gety(int i) { return 1. * (c[i] + 1) * (c[i] + 1) + f[i]; }
d64 slope(int i, int j) {
  return 1. * (gety(j) - gety(i)) / (getx(j) - getx(i));
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> L;
  for (int i = 1; i <= n; ++i) cin >> c[i], c[i] += c[i - 1] + 1;
  hd = tl = 0;
  for (int i = 1; i <= n; ++i) {
    while (hd < tl && slope(q[hd], q[hd + 1]) - eps < c[i] - L) ++hd;
    int j = q[hd];
    f[i] = f[j] + (c[i] - c[j] - 1 - L) * (c[i] - c[j] - 1 - L);
    while (hd < tl && slope(q[tl - 1], q[tl]) + eps > slope(q[tl], i)) --tl;
    q[++tl] = i;
  }
  cout << f[n];
}
```

### P3800
$f_{i, j}$ 表示到 $(i, j)$ 的最大答案，$f_{i, j} = \max\limits_{k = j - t}^{j + t} f_{i - 1, k} + v_{i, j}$，转移是分层的区间最大值，直接用 st 表处理 $f_{i - 1}$，$O(n^2 \log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 4009;
int n, m, k, t, f[N][N], st[15][N];
int query(int l, int r) {
  int d = __lg(r - l + 1);
  return max(st[d][l], st[d][r - (1 << d) + 1]);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> k >> t;
  for (int i = 1; i <= k; ++i) {
    int x, y;
    cin >> x >> y >> f[x][y];
  }
  for (int i = 2; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) st[0][j] = f[i - 1][j];
    for (int j = 1; j < 15; ++j) {
      for (int k = 1; k + (1 << j) - 1 <= m; ++k) {
        st[j][k] = max(st[j - 1][k], st[j - 1][k + (1 << (j - 1))]);
      }
    }
    for (int j = 1; j <= m; ++j) {
      f[i][j] += query(max(1, j - t), min(m, j + t));
    }
  }
  cout << *max_element(f[n] + 1, f[n] + m + 1);
}
```

### P4910
$f_{i, 0/1}$ 表示 $i$ 涂什么色，$f_{i, 0} = f_{i - 1, 1}, f_{i, 1} = f_{i - 1, 0} + f_{i - 1, 1}$。

由于是环，所以分成两次，每次钦定 $1$ 选什么。

显然可以用矩阵优化，$\begin{bmatrix}f_{i, 0} & f_{i, 1}\end{bmatrix} \begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix} = \begin{bmatrix} f_{i + 1, 0} & f_{i + 1, 1}\end{bmatrix}$。

$O(t \log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int md = 1e9 + 7;
struct matrix {
  vector<int> vec;
  int n, m;
  auto operator[](const int i) { return vec.begin() + i * m; }
  auto operator[](const int i) const { return vec.begin() + i * m; }
  matrix() = default;
  matrix(int x, int y) : n(x), m(y), vec(x * y, 0) {}
};
matrix operator*(const matrix &lhs, const matrix &rhs) {
  assert(lhs.m == rhs.n);
  matrix res(lhs.n, rhs.m);
  for (int i = 0; i < lhs.n; ++i)
    for (int j = 0; j < lhs.m; ++j)
      for (int k = 0; k < rhs.m; ++k)
        (res[i][j] += lhs[i][k] * rhs[k][j]) %= md;
  return res;
}
matrix I(int n) {
  matrix res(n, n);
  for (int i = 0; i < n; ++i) res[i][i] = 1;
  return res;
}
matrix qpow(matrix a, int b) {
  matrix r = I(a.n);
  for (; b > 0; b >>= 1, a = a * a)
    if (b & 1) r = r * a;
  return r;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  matrix b(2, 2);
  b[0][1] = b[1][0] = b[1][1] = 1;
  while (tt--) {
    int n;
    cin >> n;
    matrix a(1, 2);
    a[0][0] = 1;
    a = a * qpow(b, n - 1);
    int ans = a[0][1];
    a[0][0] = 0, a[0][1] = 1;
    a = a * qpow(b, n - 1);
    (ans += a[0][0] + a[0][1]) %= md;
    cout << ans << '\n';
  }
}
```

-------
2025.10.26

### P3519
简单。

考虑枚举最多和最少的字符，然后直接算最大子段和就可以，记录一下有没有选最少的字符。

但是直接做是 $O(|\sum|^2n)$，$n \leq 10^6$ 显然不太能过。

容易发现除了枚举的两个字符外都不会产生影响，所以每次归并求出只包含两个字符的就可以，这样是 $O(|\sum|n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T& x, const T& y) { if (x < y) { x = y; return true; } return false; }
template<class T> inline bool cmin(T& x, const T& y) { if (x > y) { x = y; return true; } return false; }
constexpr int N = 1e6 + 9;
int n, p[26][N], len[26], ps[N];
string s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> s;
  s = ' ' + s;
  for (int i = 1; i <= n; ++i) {
    p[s[i] - 'a'][++len[s[i] - 'a']] = i;
  }
  int ans = 0;
  for (int i = 0; i < 26; ++i) {
    if (len[i] == 0) continue;
    for (int j = 0; j < 26; ++j) {
      if (i == j) continue;
      if (len[j] == 0) continue;
      merge(p[i] + 1, p[i] + len[i] + 1, p[j] + 1, p[j] + len[j] + 1, ps + 1);
      for (int k = 1, su = -1, had = false; k <= len[i] + len[j]; ++k) {
        if (s[ps[k]] - 'a' == i) ++su;
        if (s[ps[k]] - 'a' == j) su -= had, had = true;
        if (su < 0) su = -1, had = false;
        cmax(ans, su);
      }
    }
  }
  cout << ans;
}
```

### P6820
首先考虑 dp，$f_{i, j}$ 表示第一个写完了 $1\sim i$，第二个写完了 $1\sim j$ 的最短时间。

显然，如果 $a_i = b_j$，只能写一个 $f_{i, j} = \min(f_{i, j - 1}, f_{i - 1, j}) + 1$；否则，$f_{i, j} = f_{i - 1, j - 1} + 1$。

容易发现，我们的转移可以看成全部左移一位再全局加 $1$ 再修改一位。

左移显然，全局加 $1$ 可以直接在初始时减掉 $n$，最后加上，修改的话，$f_{i, j - 1}$ 这里要加 $1$，因为这是全局加过一次再转移，$f_{i - 1, j}$ 直接从左移前的位置转移就可以。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T& x, const T& y) { if (x < y) { x = y; return true; } return false; }
template<class T> inline bool cmin(T& x, const T& y) { if (x > y) { x = y; return true; } return false; }
constexpr int N = 1e6 + 9;
int n, a[N], p[N], f[N * 2];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i <= n; ++i) {
    int x;
    cin >> x;
    p[x] = i;
  }
  for (int i = n; i <= 2 * n; ++i) f[i] = i - n;
  for (int i = 1; i <= n; ++i) {
    f[p[a[i]] + n - i] = min(f[p[a[i]] + n - i + 1], f[p[a[i]] + n - i - 1] + 1);
  }
  cout << f[n] + n;
}
```

------
2025.10.27
### P8112
直接 kmp 求出以每个 $1\le i \le m$ 结尾的 $t$ 的子串，最长的满足是 $s$ 前缀，然后 dp 即可。

因为 dp 数组 $f$ 是递增的，所以从最长的转移即可。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e7 + 9;
string s, t;
int n, m, nxt[N], f[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> s >> t;
  memset(f, 0x3f, sizeof f);
  f[0] = 0, s = ' ' + s, t = ' ' + t;
  for (int i = 2, j = 0; i <= n; ++i) {
    while (j && s[j + 1] != s[i]) j = nxt[j];
    nxt[i] = j += s[j + 1] == s[i];
  }
  for (int i = 1, j = 0; i <= m; ++i) {
    while (j && s[j + 1] != t[i]) j = nxt[j];
    j += s[j + 1] == t[i];
    // int k = j;
    // while (k) cmin(f[i], f[i - k] + 1), k = nxt[k];
    cmin(f[i], f[i - j] + 1);
  }
  if (f[m] == 0x3f3f3f3f) cout << "Fake";
  else cout << f[m];
}
```

### P8227
妙妙题。

首先操作是可逆的，所以我们可以将 $A$ 和 $B$ 都展开使得它们相等。

但这样不是最优的，我们可以把一部分相同的子串去掉，只对剩下的展开。

展开一个子串的话可以递归处理，计算答案也可以递归。

总的时间复杂度是 $O(n)$ 的，可以建括号树，然后会发现两个递归的点是不同的，所以相当于把树遍历了一遍。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e6 + 9;
int n, stk[N], tp, nxt[2][N];
bool vis[2][N];
string s[2];
int calc(int _, int l, int r, int thi) {
  if (r - l == 1) return 0;
  if (nxt[_][l] == r) {
    return calc(_, l + 1, r - 1, true) + !thi;
  }
  else {
    int res = 0;
    for (int i = l; i <= r; i = nxt[_][i] + 1)
      res += calc(_, i, nxt[_][i], false);
    return res + thi;
  }
}
int dfs(int l, int r) {
  if (r - l == 1) return 0;
  int res = 0;
  for (int _ = 0; _ < 2; ++_)
    for (int i = l; i <= r; vis[_][i] = true, i = nxt[_][i] + 1);
  for (int i = l; i <= r; i = nxt[0][i] + 1) {
    if (vis[1][i] && nxt[0][i] == nxt[1][i]) res += dfs(i + 1, nxt[0][i] - 1);
  }
  for (int _ = 0; _ < 2; ++_)
    for (int i = l; i <= r; i = nxt[_][i] + 1) {
      if (!vis[_ ^ 1][i] || nxt[_][i] != nxt[_ ^ 1][i]) res += calc(_, i, nxt[_][i], false);
    }
  for (int _ = 0; _ < 2; ++_)
    for (int i = l; i <= r; vis[_][i] = false, i = nxt[_][i] + 1);
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int _ = 0; _ < 2; ++_) {
    cin >> s[_];
    s[_] = ' ' + s[_];
    for (int i = 1; i <= n; ++i) {
      if (tp && s[_][stk[tp]] == '(' && s[_][i] == ')') nxt[_][stk[tp--]] = i;
      else stk[++tp] = i;
    }
  }
  // cerr << calc(0, 1, 6, false);
  cout << dfs(1, n);
}
```

------
2025.10.28

### CF472G
暴力草过去的，$64$ 个数分一段，$O(\dfrac {nq}w)$。

```cpp
#pragma GCC target("popcnt")
#include <bits/stdc++.h>
using namespace std;
#define int unsigned long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e5 + 9, K = 64;
int n, m, q, pa[N], pb[N];
string a, b;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> a >> b;
  n = a.size(), m = b.size();
  for (int i = 0; i + K - 1 < n; ++i) {
    for (int j = 0; j < K; ++j) pa[i] |= (int) (a[i + j] - '0') << j;
  }
  for (int i = 0; i + K - 1 < m; ++i) {
    for (int j = 0; j < K; ++j) pb[i] |= (int) (b[i + j] - '0') << j;
  }
  cin >> q;
  while (q--) {
    int p1, p2, len;
    cin >> p1 >> p2 >> len;
    int ans = 0, i = 0;
    for (; i + K <= len; i += K) {
      ans += __builtin_popcountll(pa[p1 + i] ^ pb[p2 + i]);
    }
    for (; i < len; ++i) ans += a[p1 + i] != b[p2 + i];
    cout << ans << '\n';
  }
}
```

### P8010
通过观察可得，答案即为 $\min_{i = l}^r\min_{j = i}^r |A(1, j) - i|$。

考虑交换 $i, j$，得到 $\min_{j = l}^r\min_{i = l}^j |A(1, j) - i|$，由于 $A(1, i) \le i$，所以如果 $A(1, j) \ge l$ 答案即为 $0$，否则为 $l - \max_{j = l}^r A(1, j)$，而 $A(1, i)$ 是单调的，所以就是 $\max(0, l - A(1, r))$。

记 $c_i = A(1, i)$。

显然可以线段树做到 $O(n\log n)$，但是过不了。

容易发现对于修改操作，每次只会给一个前缀加上非负数，那么相当于对 $c$ 做覆盖。

考虑对于所有 $c_i = i$ 的点建立链表，其余点向 $c_i$ 连边，用并查集维护，注意不能按秩合并。

那么对于每次查询，直接并查集既可。对于修改 $1\sim x$，显然 $1\le i\le x$ 的 $c_i$ 是不会变的，而对于 $x < i$ 会被合并。

因为是链表，所以合并操作直接删去即可，记录一下链表上相邻点之间的差值，这样修改时可以快速判断是否应该合并。

合并掉一个点，只需将这个点再向当前位置连边即可。

$O(n\log n)$，瓶颈在并查集。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 6e6 + 9;
int n, q, a[N], fa[N], nxt[N], w[N], h[N];
int get(int x) { return x == fa[x] ? x : fa[x] = get(fa[x]); }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1, mx = 0, lst = 0; i <= n; ++i) {
    fa[i] = fa[i - 1];
    if (a[i] >= mx) {
      mx = a[i], fa[i] = nxt[lst] = i;
      w[lst] = a[i] - a[lst], lst = i;
    }
    // cerr << get(i) << ' ';
  }
  // cerr << '\n';
  // for (int i = 1; i; i = nxt[i]) cerr << i << ' ' << w[i] << '\n';
  while (q--) {
    int o, x, y;
    cin >> o >> x >> y;
    if (o == 1) {
      x = get(x);
      y = -y;
      while (nxt[x]) {
        w[x] += y;
        if (w[x] < 0) {
          y = w[x];
          w[x] = w[nxt[x]];
          fa[nxt[x]] = x;
          nxt[x] = nxt[nxt[x]];
        }
        else break;
      }
    }
    else {
      // cerr << get(y) << '\n';
      cout << max(0ll, x - get(y)) << '\n';
    }
  }
}
```

以及过不了的线段树。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 6e6 + 9;
int n, q, a[N], tg[N << 2];
pair<int, int> sgt[N << 2];
void build(int u, int l, int r) {
  if (l == r) return sgt[u] = {a[l], l}, void();
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
  sgt[u] = max(sgt[u << 1], sgt[u << 1 | 1]);
}
void apply(int u, int z) {
  sgt[u].first += z, tg[u] += z;
}
void down(int u) {
  if (tg[u]) apply(u << 1, tg[u]), apply(u << 1 | 1, tg[u]), tg[u] = 0;
}
void update(int u, int l, int r, int x, int y) {
  if (r <= x) return apply(u, y);
  int m = (l + r) >> 1;
  down(u);
  update(u << 1, l, m, x, y);
  if (m < x) update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = max(sgt[u << 1], sgt[u << 1 | 1]);
}
pair<int, int> query(int u, int l, int r, int x) {
  if (r <= x) return sgt[u];
  int m = (l + r) >> 1;
  down(u);
  pair<int, int> res = query(u << 1, l, m, x);
  if (m < x) cmax(res, query(u << 1 | 1, m + 1, r, x));
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  build(1, 1, n);
  while (q--) {
    int o, x, y;
    cin >> o >> x >> y;
    if (o == 1) {
      update(1, 1, n, x, y);
    }
    else {
      // cerr << get(y) << '\n';
      cout << max(0ll, x - query(1, 1, n, y).second) << '\n';
    }
  }
}
```

### P5590
考虑先找出所有在路径上的边，那么对于这些边 $(u, v)$，我们令 $d_i$ 表示 $1\to i$ 的距离，有 $1 \le d_v - d_u = w(u, v) \le 9$。

于是建图跑差分约束即可。

$O(n^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2009;
int n, m, vis[N][2], dst[N];
vector<int> es[N][2];
vector<pair<int, int>> se[N];
pair<int, int> e[N];
void dfs(int x, int k) {
  vis[x][k] = 1;
  for (int y : es[x][k])
    if (!vis[y][k]) dfs(y, k);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    cin >> e[i].first >> e[i].second;
    es[e[i].first][0].push_back(e[i].second);
    es[e[i].second][1].push_back(e[i].first);
  }
  dfs(1, 0), dfs(n, 1);
  if (!vis[n][0]) return cout << -1, 0;
  memset(dst, 0x3f, sizeof dst);
  dst[1] = 0;
  for (int i = 1; i <= m; ++i) {
    if (!vis[e[i].first][0] || !vis[e[i].second][0]) continue;
    if (!vis[e[i].first][1] || !vis[e[i].second][1]) continue;
    se[e[i].first].emplace_back(e[i].second, 9);
    se[e[i].second].emplace_back(e[i].first, -1);
  }
  for (int i = 1; i <= n; ++i) {
    bool ok = false;
    for (int j = 1; j <= n; ++j) {
      if (dst[j] == 0x3f3f3f3f) continue;
      for (auto [y, z] : se[j]) {
        if (dst[y] > dst[j] + z) dst[y] = dst[j] + z, ok = true;
      }
    }
    if (i == n && ok) return cout << "-1", 0;
  }
  cout << n << ' ' << m << '\n';
  for (int i = 1; i <= m; ++i) {
    cout << e[i].first << ' ' << e[i].second << ' ' << max(1, min(9, dst[e[i].second] - dst[e[i].first])) << '\n';
  }
}
```

### P11085
首先注意到班内先排序，然后相邻必然是同桌；再注意到把桌子排序，去掉左端点相同的之后，每个班排序后的第 $2 \times i - 1, 2 \times i$ 两个人必然是同一张桌子。

然后再发现，每个位置 $2 \times i - 1, 2 \times i$ 选的桌子 $p_i$ 是单调的，可以用分治优化。

$O(nm\log k \log m)$，$\log m$ 是算代价的。

```cpp
 #include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e5 + 9;
int n, m, k, ans;
map<int, int> mp;
vector<pair<int, int>> a;
vector<int> h[N], pr[N], sf[N], f[N];
int calc(int i, int j) {
  auto [l, r] = a[j];
  int tr = upper_bound(f[i].begin() + 1, f[i].begin() + 2 * m + 1, r) - f[i].begin();
  int tl = lower_bound(f[i].begin() + 1, f[i].begin() + 2 * m + 1, l) - f[i].begin() - 1;
  return tl * l - pr[i][tl] + sf[i][tr] - (2 * m - tr + 1) * r;
}
void dfs(int l, int r, int pl, int pr) {
  if (l > r) return ;
  int m = (l + r) >> 1;
  int cur = pl - 1, mn = 0x3f3f3f3f3f3f3f3f;
  for (int i = pl; i <= pr; ++i) {
    if (calc(m, i) < mn) mn = calc(m, i), cur = i;
  }
  ans += mn;
  dfs(l, m - 1, pl, cur), dfs(m + 1, r, cur, pr);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> m >> n >> k;
  for (int i = 1; i <= k; ++i) {
    int l, r;
    cin >> l >> r;
    cmax(mp[l], r);
  }
  for (auto [x, y] : mp) a.emplace_back(x, y);
  k = a.size();
  for (int i = 1; i <= m; ++i) {
    h[i].resize(n * 2 + 4);
    for (int j = 1; j <= n; ++j) {
      cin >> h[i][2 * j] >> h[i][2 * j - 1];
    }
    sort(h[i].begin() + 1, h[i].begin() + 2 * n + 1);
  }
  for (int i = 1; i <= n; ++i) f[i].resize(2 * m + 5);
  for (int i = 1; i <= m; ++i) {
    for (int j = 1; j <= n; ++j) f[j][i * 2 - 1] = h[i][j * 2 - 1], f[j][2 * i] = h[i][j * 2];
  }
  for (int i = 1; i <= n; ++i) {
    sort(f[i].begin() + 1, f[i].begin() + 2 * m + 1);
    pr[i].resize(m * 2 + 4), sf[i].resize(m * 2 + 4);
    for (int j = 1; j <= 2 * m; ++j) pr[i][j] = pr[i][j - 1] + f[i][j];
    for (int j = 2 * m; j >= 1; --j) sf[i][j] = sf[i][j + 1] + f[i][j];
  }
  dfs(1, n, 0, k - 1);
  cout << ans;
}
```

### CF1238E
$m\le 20$ 考虑状压，令 $f_S$ 表示已经放了 $S$ 中的所有字母后的贡献。

由于贡献与位置的大小相关，考虑拆开。

$c_{i, j}$ 表示 $i, j$ 这个字母对的出现次数，那么显然贡献为 $|p_i - p_j| c_{i , j}$。

如果已知 $p_i, p_j$ 大小关系，那么就好做了，于是我们考虑转移时不计算 $i, j \in S$ 的，只计算有一个在 $S$ 中的贡献。

显然这样做是对的，于是我们预处理一个 $g_{S, i} = \sum_{j \in S}c_{i, j}$，然后转移即为 $f_S = \min_j f_{S - \{j\}} + |S|(g_{S - \{j\}, j} - g_{U - S, j})$。

$O(n2^m)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
int n, m, cnt[20][20], f[1 << 20], g[1 << 20][20];
string s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> s;
  s = ' ' + s;
  for (int i = 1; i < n; ++i) {
    ++cnt[s[i] - 'a'][s[i + 1] - 'a'];
    ++cnt[s[i + 1] - 'a'][s[i] - 'a'];
  }
  for (int i = 0; i < 1 << m; ++i) {
    for (int j = 0; j < m; ++j) {
      g[i][j] = g[i ^ (i & -i)][j] + cnt[__lg(i & -i)][j];
    }
  }
  memset(f, 0x3f, sizeof f);
  f[0] = 0;
  for (int i = 0; i < 1 << m; ++i) {
    for (int j = 0; j < m; ++j) {
      if (i >> j & 1 ^ 1) continue;
      cmin(f[i], f[i ^ 1 << j] + __builtin_popcount(i) * (g[i ^ 1 << j][j] - g[i ^ ((1 << m) - 1)][j]));
    }
  }
  cout << f[(1 << m) - 1];
}
```
-----
2025.10.29

### P13274
代码很长，但是不用动脑的做法。

手玩可以发现只有 110 和 101 会变，观察样例就可以发现，如果有 110 那么答案即为最左侧的 110 到右端的距离，如果没有但是有 101 答案是 $1$ 否则是 $0$。

写个暴力简单验证一下，然后考虑如何维护。

由于每个位置 $i$ 的值与 $i - 2, i - 1, i$ 有关，直接反转 $[l, r]$ 是不行的。

考虑反转 $[l + 2, r]$，这样区间内所有位置和与其相关联的都会一起反转，所以我们记录一下 110,001,101,010 的出现次数，直接交换即可。

而 $l, l + 1, r + 1, r + 2$ 四个位置也会变，手动更新一下，代码比较长。

查询直接线段树上二分即可。

$O(q\log n)$，不知道为什么被卡常了。

注意到操作的时候不用 pushdown 可以减掉很多常数。

```cpp
#include <bits/stdc++.h>
using namespace std;
namespace {
char buf[1 << 26], *p1, *p2;
#define gc (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 1 << 26, stdin)) == p1 ? EOF : *p1++)
template<class T> inline void read(T &x) {
  x = 0;
  char c = gc;
  for (; c < '0' || '9' < c; c = gc);
  for (; '0' <= c && c <= '9'; c = gc) x = (x << 1) + (x << 3) + (c & 15);
}
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 4e5 + 9;
int n, q, a[N];
struct info {
  int ooz, zzo, ozo, zoz, o, z;
  info operator+(const info &x) const {
    return {ooz + x.ooz, zzo + x.zzo, ozo + x.ozo, zoz + x.zoz, o + x.o, z + x.z};
  }
} sgt[N << 2];
bool tg[N << 2];
void build(int u, int l, int r) {
  tg[u] = false;
  if (l == r) {
    sgt[u].ooz = a[l - 2] == 1 && a[l - 1] == 1 && a[l] == 0;
    sgt[u].zzo = a[l - 2] == 0 && a[l - 1] == 0 && a[l] == 1;
    sgt[u].ozo = a[l - 2] == 1 && a[l - 1] == 0 && a[l] == 1;
    sgt[u].zoz = a[l - 2] == 0 && a[l - 1] == 1 && a[l] == 0;
    sgt[u].o = a[l] == 1, sgt[u].z = a[l] == 0;
    return ;
  }
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
void apply(int u) {
  swap(sgt[u].ooz, sgt[u].zzo), swap(sgt[u].zoz, sgt[u].ozo);
  swap(sgt[u].o, sgt[u].z), tg[u] ^= 1;
}
void down(int u) {
  if (tg[u]) apply(u << 1), apply(u << 1 | 1), tg[u] = false;
}
void update(int u, int l, int r, int x, int y) {
  if (x <= l && r <= y) return apply(u);
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x, y);
  if (m < y) update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
void update1(int u, int l, int r, int x, info &y) {
  if (l == r) return sgt[u] = y, void();
  int m = (l + r) >> 1;
  if (m >= x) update1(u << 1, l, m, x, y);
  else update1(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
int query(int u, int l, int r, int x) {
  if (l == r) return sgt[u].o;
  int m = (l + r) >> 1;
  down(u);
  if (m >= x) return query(u << 1, l, m, x);
  else return query(u << 1 | 1, m + 1, r, x);
}
int get(int u, int l, int r) {
  if (sgt[u].ooz == 0) return n + 1;
  if (l == r) return l;
  int m = (l + r) >> 1;
  down(u);
  if (sgt[u << 1].ooz > 0) return get(u << 1, l, m);
  else return get(u << 1 | 1, m + 1, r);
}
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int c, tt;
  read(c), read(tt);
  while (tt--) {
    read(n), read(q);
    for (int i = 1; i <= n; ++i) {
      char c = gc;
      for (; c < '0' || '1' < c; c = gc);
      a[i] = c - '0';
    }
    build(1, 3, n);
    int64_t ans = n - get(1, 3, n) + 1;
    if (ans == 0 && sgt[1].ozo > 0) ans = 1;
    for (int i = 1; i <= q; ++i) {
      int l, r;
      read(l), read(r);
      if (l + 2 <= r) update(1, 3, n, l + 2, r);
      int lf2 = 0, lf1 = 0, l0 = 0, l1 = 0;
      if (l - 2 >= 1) {
        if (l - 2 < 3) lf2 = a[l - 2];
        else lf2 = query(1, 3, n, l - 2);
      }
      else lf2 = -1;
      if (l - 1 >= 1) {
        if (l - 1 < 3) lf1 = a[l - 1];
        else lf1 = query(1, 3, n, l - 1);
      }
      else lf1 = -1;
      if (l < 3) a[l] ^= 1, l0 = a[l];
      else l0 = query(1, 3, n, l) ^ 1;
      if (l + 1 < 3) {
        if (l + 1 <= r) a[l + 1] ^= 1;
        l1 = a[l + 1];
      }
      else {
        l1 = query(1, 3, n, l + 1);
        if (l + 1 <= r) l1 ^= 1;
      }
      // cerr << lf2 << ' ' << lf1 << ' ' << l0 << ' ' << l1 << '\n';
      { // l + 1
        info nw = {0, 0, 0, 0, l1 == 1, l1 == 0};
        nw.ooz = lf1 == 1 && l0 == 1 && l1 == 0;
        nw.zzo = lf1 == 0 && l0 == 0 && l1 == 1;
        nw.ozo = lf1 == 1 && l0 == 0 && l1 == 1;
        nw.zoz = lf1 == 0 && l0 == 1 && l1 == 0;
        if (l + 1 >= 3 && l + 1 <= r) update1(1, 3, n, l + 1, nw);
      }
      { // l
        info nw = {0, 0, 0, 0, l0 == 1, l0 == 0};
        nw.ooz = lf2 == 1 && lf1 == 1 && l0 == 0;
        nw.zzo = lf2 == 0 && lf1 == 0 && l0 == 1;
        nw.ozo = lf2 == 1 && lf1 == 0 && l0 == 1;
        nw.zoz = lf2 == 0 && lf1 == 1 && l0 == 0;
        if (l >= 3) update1(1, 3, n, l, nw);
      }
      int rf1 = 0, r0 = 0, r1 = 0, r2 = 0;
      if (r - 1 >= 1) {
        if (r - 1 < 3) rf1 = a[r - 1];
        else rf1 = query(1, 3, n, r - 1);
      }
      else rf1 = -1;
      if (r < 3) r0 = a[r];
      else r0 = query(1, 3, n, r);
      if (r + 1 < 3) r1 = a[r + 1];
      else if (r + 1 <= n) r1 = query(1, 3, n, r + 1);
      else r1 = -1;
      if (r + 2 < 3) r2 = a[r + 2];
      else if (r + 2 <= n) r2 = query(1, 3, n, r + 2);
      else r2 = -1;
      { // r + 1
        info nw = {0, 0, 0, 0, r1 == 1, r1 == 0};
        nw.ooz = rf1 == 1 && r0 == 1 && r1 == 0;
        nw.zzo = rf1 == 0 && r0 == 0 && r1 == 1;
        nw.ozo = rf1 == 1 && r0 == 0 && r1 == 1;
        nw.zoz = rf1 == 0 && r0 == 1 && r1 == 0;
        if (r + 1 >= 3 && r + 1 <= n) update1(1, 3, n, r + 1, nw);
      }
      { // r + 2
        info nw = {0, 0, 0, 0, r2 == 1, r2 == 0};
        nw.ooz = r0 == 1 && r1 == 1 && r2 == 0;
        nw.zzo = r0 == 0 && r1 == 0 && r2 == 1;
        nw.ozo = r0 == 1 && r1 == 0 && r2 == 1;
        nw.zoz = r0 == 0 && r1 == 1 && r2 == 0;
        if (r + 2 >= 3 && r + 2 <= n) update1(1, 3, n, r + 2, nw);
      }
      int res = n - get(1, 3, n) + 1;
      if (res == 0 && sgt[1].ozo > 0) res = 1;
      // cerr << res << '\n';
      ans ^= 1ll * (i + 1) * res;
    }
    cout << ans << '\n';
  }
}
```

### P13271
记录每个点的状态为 $(x, p)$，表示到达 $x$ 时，$p$ 的值。

然后直接跑 dijkstra，每次 $(x, p)$ 可以到 $(y, p), (x, p + 1), (x, p - 1)$。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 3e5 + 9;
int n, m, k, v[N], w[N];
vector<pair<int, int>> es[N];
map<int, int> dst[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int c;
  cin >> c;
  cin >> n >> m >> k;
  for (int i = 1; i < k; ++i) cin >> v[i], v[i] += v[i - 1];
  for (int i = 2; i <= k; ++i) cin >> w[i], w[i] += w[i - 1];
  for (int i = 1; i <= n; ++i) {
    int d;
    cin >> d;
    es[i].resize(d);
    for (int j = 0; j < d; ++j) cin >> es[i][j].first >> es[i][j].second;
  }
  priority_queue<tuple<int, int, int>> q;
  dst[1][1] = 0;
  q.emplace(0, 1, 1);
  for (; !q.empty(); ) {
    auto [d, x, p] = q.top();
    d = -d, q.pop();
    if (dst[x][p] != d) continue;
    if (p > 1 && !es[x].empty()) {
      int np = min(p - 1, (int) es[x].size());
      int t = w[p] - w[np];
      if (!dst[x].count(np)) dst[x][np] = 0x3f3f3f3f3f3f3f3f;
      if (dst[x][np] > dst[x][p] + t) {
        dst[x][np] = dst[x][p] + t;
        q.emplace(-dst[x][np], x, np);
      }
    }
    if (p < k && p < es[x].size()) {
      int t = v[p] - v[p - 1];
      if (!dst[x].count(p + 1)) dst[x][p + 1] = 0x3f3f3f3f3f3f3f3f;
      if (dst[x][p + 1] > dst[x][p] + t) {
        dst[x][p + 1] = dst[x][p] + t;
        q.emplace(-dst[x][p + 1], x, p + 1);
      }
    }
    // cerr << p << ' ';
    if (p > es[x].size()) continue;
    auto [y, z] = es[x][p - 1];
    if (!dst[y].count(p)) dst[y][p] = 0x3f3f3f3f3f3f3f3f;
    if (dst[y][p] > dst[x][p] + z) {
      dst[y][p] = dst[x][p] + z;
      q.emplace(-dst[y][p], y, p);
    }
  }
  for (int i = 1; i <= n; ++i) {
    if (dst[i].empty()) cout << -1 << ' ';
    else {
      int mn = 0x3f3f3f3f3f3f3f3f;
      for (auto [x, y] : dst[i]) cmin(mn, y);
      cout << mn << ' ';
    }
  }
}
```

### P7706
被诈骗了。

直接用线段树维护这个东西，考虑如何设计信息。

每次我们维护一个区间中的 $\max a, \min b, \max \limits_{i < j} a_i - b_j, \max\limits_{i < j} a_j - b_i, \max\limits_{i < j < k} a_i + a_k - b_j$ 五个东西。

那么每次合并信息，$\max a, \min b$ 是容易的，其余只需考虑在左右区间选一个最小或最大的点即可。

单点修改是容易的。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 5e5 + 9, inf = 1e9;
int n, m, a[N], b[N];
struct info {
  int mnb, mxa, s, sl, sr;
  info operator+(const info &x) const {
    return {min(mnb, x.mnb), max(mxa, x.mxa), max({s, x.s, sl + x.mxa, x.sr + mxa}),
            max({sl, x.sl, mxa - x.mnb}), max({sr, x.sr, x.mxa - mnb})};
  }
} sgt[N << 2];
void build(int u, int l, int r) {
  if (l == r) return sgt[u] = {b[l], a[l], -inf, -inf, -inf}, void();
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
void update(int u, int l, int r, int x, info y) {
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
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i <= n; ++i) cin >> b[i];
  build(1, 1, n);
  while (m--) {
    int o, x, y;
    cin >> o >> x >> y;
    if (o == 1) a[x] = y, update(1, 1, n, x, {b[x], a[x], -inf, -inf, -inf});
    else if (o == 2) b[x] = y, update(1, 1, n, x, {b[x], a[x], -inf, -inf, -inf});
    else cout << query(1, 1, n, x, y).s << '\n';
  }
}
```

### CF2000H
值域线段树，然后查询直接线段树上二分。

维护连续的没有出现的段长，二分时会出现一个段跨过中点，这种情况直接返回就可以了。

$O(q\log V)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e5 + 9, V = 4e6 + 9, inf = 1e12;
int n, m, a[N], b[N << 1];
pair<char, int> q[N];
struct info {
  int ml, mr, mx, all;
  info operator+(const info &x) const {
    return {max(ml, all + x.ml), max(x.mr, mr + x.all), max({mx, x.mx, mr + x.ml}), all + x.all};
  }
} sgt[V << 2];
void build(int u, int l, int r) {
  sgt[u] = {r - l + 1, r - l + 1, r - l + 1, r - l + 1};
  if (l == r) return ;
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
}
void update(int u, int l, int r, int x, int y) {
  // cerr << u << ' ' << l << ' ' << r << ' ' << x << ' ' << y << '\n';
  if (l == r) return sgt[u] = {y == 0 ? 1 : -inf, y == 0 ? 1 : -inf, y == 0 ? 1 : -inf, y == 0 ? 1 : -inf}, void();
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x, y);
  else update(u << 1 | 1, m + 1, r, x, y);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
int query(int u, int l, int r, int x) {
  // cerr << u << ' ' << l << ' ' << r << ' ' << x << '\n';
  if (l == r) return l;
  int m = (l + r) >> 1;
  if (sgt[u << 1].mx >= x) return query(u << 1, l, m, x);
  else {
    if (sgt[u << 1].mr + sgt[u << 1 | 1].ml >= x) return m - sgt[u << 1].mr + 1;
    return query(u << 1 | 1, m + 1, r, x);
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt, c = 0;
  cin >> tt;
  build(1, 1, V);
  while (tt--) {
    for (int i = 1; i <= c; ++i) update(1, 1, V, b[i], 0);
    c = 0;
    cin >> n;
    for (int i = 1; i <= n; ++i) cin >> a[i], b[++c] = a[i], update(1, 1, V, a[i], 1);
    cin >> m;
    while (m--) {
      char o;
      int x;
      cin >> o >> x;
      if (o == '+') update(1, 1, V, x, 1), b[++c] = x;
      else if (o == '-') update(1, 1, V, x, 0), b[++c] = x;
      else {
        cout << query(1, 1, V, x) << ' ';
      }
    }
    cout << '\n';
    // return 0;
  }
}
```
--------
2025.10.30
### CF949B
手玩一下发现前 $\lceil \dfrac n2\rceil$ 个是不动的，而剩下的可以递归。

于是分 $x, n$ 的奇偶讨论一下即可。

大样例太水了，导致我多写了一个判断然后绑包就爆炸了。

$O(q\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
int n, q;
int f(int n, int k) {
  if (k & 1) return (k + 1) / 2;
  else if (n & 1) return f(n - (n + 1) / 2, (k / 2 + (n - (n + 1) / 2) - 2) % (n - (n + 1) / 2) + 1) + (n + 1) / 2;
  else return f(n - (n + 1) / 2, k / 2) + (n + 1) / 2;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  while (q--) {
    int x;
    cin >> x;
    cout << f(n, x) << '\n';
  }
}
```

-------
2025.11.3
### P3193
加训串串！

$A$ 中没有出现 $X$，显然 kmp 是跑不出来的。

考虑 kmp 自动机，相当于在上面跑不到 $m$ 这个状态。

于是记 $g_{i, j}$ 表示加一个字母转移 $i \to j$ 的个数。

考虑 dp，$f_{i, j}$ 表示加了 $i$ 个字母，走到了状态 $j$，$f_{i, j} = \sum_{k = 0}^{m - 1} f_{i - 1, k}g_{k, j}$，显然是矩阵乘法的形式。

$O(m^3 \log n)$

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 29;
template<size_t N, size_t M>
using matrix = array<array<int, M>, N>;
int n, m, md, nxt[N], to[N][10];
matrix<N, N> g;
string s;
template<size_t N, size_t M, size_t R>
matrix<N, R> operator*(const matrix<N, M> &lhs, const matrix<M, R> &rhs) {
  matrix<N, R> res = {};
  for (size_t i = 0; i < N; ++i)
    for (size_t j = 0; j < M; ++j)
      for (size_t k = 0; k < R; ++k)
        (res[i][j] += lhs[i][k] * rhs[k][j]) %= md;
  return res;
}
template<size_t N, size_t M>
matrix<N, M> qpow(matrix<N, M> a, int b) {
  matrix<N, M> r = {};
  if (b == 0) return r;
  for (--b, r = a; b > 0; b >>= 1, a = a * a)
    if (b & 1) r = r * a;
  return r;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> md;
  cin >> s;
  s = ' ' + s;
  for (int i = 2, j = 0; i <= m; ++i) {
    while (j && s[j + 1] != s[i]) j = nxt[j];
    nxt[i] = j += s[j + 1] == s[i];
  }
  for (int i = 0; i < m; ++i) {
    for (int j = 0; j < 10; ++j) {
      if (i < m && s[i + 1] == j + '0') to[i][j] = i + 1;
      else to[i][j] = to[nxt[i]][j];
      if (to[i][j] < m) ++g[i][to[i][j]];
    }
  }
  matrix<1, N> f = {};
  f[0][0] = 1;
  f = f * qpow(g, n);
  int ans = 0;
  for (int i = 0; i < m; ++i) (ans += f[0][i]) %= md;
  cout << ans;
}
```

### CF808G
建 kmp 自动机，然后容易得到一个 $O(nm)$ 的 dp，$f_{i, j}$ 表示填完 $s_{1 \dots i}$ 后，匹配到了 $t_{1\dots j}$ 出现次数最多为多少。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
int n, m, nxt[N], to[N][26];
string s, t;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> s >> t;
  n = s.size(), m = t.size();
  s = ' ' + s, t = ' ' + t;
  for (int i = 2, j = 0; i <= m; ++i) {
    while (j && t[j + 1] != t[i]) j = nxt[j];
    nxt[i] = j += t[j + 1] == t[i];
  }
  for (int i = 0; i <= m; ++i) {
    for (int j = 0; j < 26; ++j) {
      if (i < m && t[i + 1] == j + 'a') to[i][j] = i + 1;
      else to[i][j] = to[nxt[i]][j];
    }
  }
  vector<vector<int>> f(n + 5, vector<int>(m + 5, -0x3f3f3f3f));
  f[0][0] = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j <= m; ++j) {
      if (s[i + 1] != '?') cmax(f[i + 1][to[j][s[i + 1] - 'a']], f[i][j] + (to[j][s[i + 1] - 'a'] == m));
      else {
        for (int k = 0; k < 26; ++k) cmax(f[i + 1][to[j][k]], f[i][j] + (to[j][k] == m));
      }
    }
  }
  cout << *max_element(f[n].begin(), f[n].end());
}
```

### P14363
$|t_1| \neq |t_2|$。


容易发现可以先把 $s_i, t$ 最短的不同子串取出来，那么满足条件，等价于不同部分**想等**，而 $s_i$ 前缀为 $t$ 前缀的后缀，$s_i$ 后缀为 $t$ 后缀的前缀。

考虑反转前缀，问题变成求有多少 $(pre \ s_i, suf\ s_i)$ 分别是 $(pre \ t, suf \ t)$ 的前缀。

考虑对于前后缀建出字典树，将 $s, t$ 插入字典树中。

记 $p_a$ 表示 $a$ 在字典树上的结束节点。

那么一个串 $a$ 是 $b$ 的前缀，当且仅当 $p_b \in \text{subtree}(p_a)$。

转化为 dfs 序，即为 $dfn_{p_a} \le dfn_{p_b} < dfn_{p_a} + sz_{p_a}$。

那么对于一个 $i$，前后缀分别对应一个限制，这就相当于二维偏序。

于是离线下来，扫描线加树状数组即可。

$O(L_1 + L_2 + (q + n) \log (L_1 + L_2))$。

代码里对每个不同串都单独建了字典树/bangbangt

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
using u64 = unsigned long long;
mt19937_64 rng(random_device{}());
constexpr int N = 2e5 + 9, L = 5e6 + 9;
constexpr u64 md = (1LL << 61) - 1;
const u64 seed = uniform_int_distribution<u64>(md >> 2, md >> 1)(rng);
int n, q, len[N], tot[2], ch[2][L][26], dfn[2][L], sz[2][L], idx[2], c[L], ans[N];
pair<int, int> ed[N], edq[N];
string s[N][2];
map<pair<u64, u64>, int> rt[2];
set<int> rot[2];
vector<pair<int, int>> vec[L];
vector<tuple<int, int, int>> qry[L];
void update(int x, int y) { for (; x <= tot[0]; x += x & -x) c[x] += y; }
int query(int x, int r = 0) { for (; x > 0; x -= x & -x) r += c[x]; return r; }
u64 add(u64 x, u64 y) {
  x += y;
  if (x >= md) x -= md;
  return x;
}
u64 sub(u64 x, u64 y) {
  x += md - y;
  if (x >= md) x -= md;
  return x;
}
u64 mul(u64 x, u64 y) {
  __int128 r = (__int128) x * y;
  u64 t = u64(r >> 61) + u64(r & md);
  if (t >= md) t -= md;
  return t;
}
u64 shift(u64 x) {
  x ^= x << 15;
  x ^= x >> 7;
  x ^= x << 13;
  return x;
}
int ins(int &u, const string &str, int p, bool s) {
  // cerr << u << ' ' << str << ' ' << p << ' ' << s << '\n';
  if (!u) u = ++tot[s];
  if (str.size() == p) return u;
  int c = str[p] - 'a';
  return ins(ch[s][u][c], str, p + 1, s);
}
int dfs(int u, bool s) {
  // cerr << u << ' ' << s << ' ' << tot[s] << ' ' << idx[s] << '\n';
  dfn[s][u] = ++idx[s];
  for (int i = 0; i < 26; ++i)
    if (ch[s][u][i]) sz[s][u] += dfs(ch[s][u][i], s);
  return ++sz[s][u];
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  for (int i = 1; i <= n; ++i) {
    cin >> s[i][0] >> s[i][1];
    len[i] = s[i][0].size();
    s[i][0] = ' ' + s[i][0], s[i][1] = ' ' + s[i][1];
    int l = 1, r = len[i];
    string pre, suf;
    while (l < len[i] && s[i][0][l] == s[i][1][l]) pre += s[i][0][l], ++l;
    while (r > 1 && s[i][0][r] == s[i][1][r]) suf += s[i][0][r], --r;
    reverse(pre.begin(), pre.end());
    reverse(suf.begin(), suf.end());
    if (l <= r) {
      u64 h1 = 0, h2 = 0;
      for (int j = l; j <= r; ++j) {
        h1 = add(mul(h1, seed), shift(s[i][0][j]));
        h2 = add(mul(h2, seed), shift(s[i][1][j]));
      }
      ed[i].first = ins(rt[0][make_pair(h1, h2)], pre, 0, 0);
      ed[i].second = ins(rt[1][make_pair(h1, h2)], suf, 0, 1);
      rot[0].insert(rt[0][make_pair(h1, h2)]);
      rot[1].insert(rt[1][make_pair(h1, h2)]);
    }
  }
  // return 0;
  for (int i = 1; i <= q; ++i) {
    string t[2];
    cin >> t[0] >> t[1];
    if (t[0].size() != t[1].size()) continue;
    const int m = t[0].size();
    t[0] = ' ' + t[0], t[1] = ' ' + t[1];
    int l = 1, r = m;
    string pre, suf;
    while (l < m && t[0][l] == t[1][l]) pre += t[0][l], ++l;
    while (r > 1 && t[0][r] == t[1][r]) suf += t[0][r], --r;
    reverse(pre.begin(), pre.end());
    reverse(suf.begin(), suf.end());
    assert(l <= r);
    u64 h1 = 0, h2 = 0;
    for (int j = l; j <= r; ++j) {
      h1 = add(mul(h1, seed), shift(t[0][j]));
      h2 = add(mul(h2, seed), shift(t[1][j]));
    }
    edq[i].first = ins(rt[0][make_pair(h1, h2)], pre, 0, 0);
    edq[i].second = ins(rt[1][make_pair(h1, h2)], suf, 0, 1);
    rot[0].insert(rt[0][make_pair(h1, h2)]);
    rot[1].insert(rt[1][make_pair(h1, h2)]);
  }
  for (int r : rot[0]) dfs(r, 0);
  for (int r : rot[1]) dfs(r, 1);
  for (int i = 1; i <= n; ++i) {
    // cerr << ed[i].first << ' ' << ed[i].second << ' ' << dfn[0][ed[i].first] << ' ' << dfn[1][ed[i].second] << '\n';
    if (ed[i].first == 0) continue;
    qry[dfn[0][ed[i].first]].emplace_back(1, dfn[1][ed[i].second], dfn[1][ed[i].second] + sz[1][ed[i].second] - 1);
    qry[dfn[0][ed[i].first] + sz[0][ed[i].first]].emplace_back(-1, dfn[1][ed[i].second], dfn[1][ed[i].second] + sz[1][ed[i].second] - 1);
  }
  for (int i = 1; i <= q; ++i) vec[dfn[0][edq[i].first]].emplace_back(dfn[1][edq[i].second], i);
  for (int i = 1; i <= idx[0]; ++i) {
    for (auto [d, x, y] : qry[i]) update(x, d), update(y + 1, -d);
    for (auto [x, y] : vec[i]) ans[y] = query(x);
  }
  for (int i = 1; i <= q; ++i) cout << ans[i] << '\n';
}
```
----------
2025.11.04
### CF1154F
这个题，*800 吧。

直接对 $a$ 排序，选前 $k$ 个，然后 dp，令 %f_i$ 表示选前 $i$ 个的最小花费。

每次枚举选的优惠券，$O(km + n \log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e5 + 9;
int n, m, k, a[N], s[N], f[N];
pair<int, int> b[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> k;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i <= m; ++i) cin >> b[i].first >> b[i].second, b[i].second = b[i].first - b[i].second;
  sort(a + 1, a + n + 1);
  for (int i = 1; i <= k; ++i) s[i] = s[i - 1] + a[i];
  memset(f, 0x3f, sizeof f);
  f[0] = 0;
  for (int i = 1; i <= k; ++i) {
    cmin(f[i], f[i - 1] + a[i]);
    for (int j = 1; j <= m; ++j) {
      if (i >= b[j].first) cmin(f[i], f[i - b[j].first] + s[i] - s[max(0ll, i - b[j].second)]);
    }
  }
  cout << f[k];
}
```

### CF1149B
容易想到一个 $O(l^3)$ 的 dp，$f_{i, j, k}$ 表示三种分别匹配到 $i, j, k$ 时，最小需要前多少个字母。

每次 dp 一遍，$O(ql^3)$ 过不了。我们可以发现，每次新加一个字母只会影响 $O(l^2)$ 个状态。

$O(ql^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9, L = 259;
int n, q, nxt[N][26], len[4], f[L][L][L], str[4][N];
string s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q >> s;
  s = ' ' + s;
  for (int i = 0; i < 26; ++i) nxt[n + 2][i] = nxt[n + 1][i] = n + 1;
  for (int i = n; i >= 1; --i) {
    for (int j = 0; j < 26; ++j) nxt[i][j] = nxt[i + 1][j];
    nxt[i][s[i] - 'a'] = i;
  }
  memset(f, 0x3f, sizeof f);
  f[0][0][0] = 0;
  while (q--) {
    char op, c;
    int x;
    cin >> op >> x;
    if (op == '+') {
      cin >> c;
      str[x][++len[x]] = c - 'a';
      for (int i = (x != 1 ? 0 : len[1]); i <= len[1]; ++i) {
        for (int j = (x != 2 ? 0 : len[2]); j <= len[2]; ++j) {
          for (int k = (x != 3 ? 0 : len[3]); k <= len[3]; ++k) {
            f[i][j][k] = 0x3f3f3f3f;
            if (i >= 1) cmin(f[i][j][k], nxt[f[i - 1][j][k] + 1][str[1][i]]);
            if (j >= 1) cmin(f[i][j][k], nxt[f[i][j - 1][k] + 1][str[2][j]]);
            if (k >= 1) cmin(f[i][j][k], nxt[f[i][j][k - 1] + 1][str[3][k]]);
          }
        }
      }
    }
    else --len[x];
    // cerr << f[len[1]][len[2]][len[3]] << '\n';
    if (f[len[1]][len[2]][len[3]] <= n) cout << "YES\n";
    else cout << "NO\n";
  }
}
```

----------
2025.11.05
#### HDU4677
分块。

考虑按左端点所在的块为第一关键字，右端点为第二关键字排序。

我们把左端点同一个块的询问一起处理。

令块长为 $S$。

由于左端点所在的块相同，所以右端点时单调的，我们可以每次暴力合并右侧部分，最多会合并 $O(\dfrac {n^2}S)$ 次。

而左侧块内部分，可以直接暴力，每次利用时间戳优化，避免清空，$O(qS)$。

总复杂度是 $O(qS + \dfrac {n^2}S)$，$S = \dfrac {n}{\sqrt{q}}$ 时最优。

$O(n\sqrt q)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 30009;
vector<int> es[N];
int n, m, q, blk, ans[N], far[N], fal[N], cntl, cntr, u[N], tg, mid, lst, st[N], ed[N];
struct qry {
  int l, r, i;
  bool operator<(const qry &x) const {
    if (l / blk == x.l / blk) return r < x.r;
    return l / blk < x.l / blk;
  }
} Q[N];
int getrf(int x) { return x == far[x] ? x : far[x] = getrf(far[x]); }
void mer(int x, int y) {
  if ((x = getrf(x)) == (y = getrf(y))) return ;
  far[x] = y, --cntr;
}
int getlf(int x) { return u[x] != tg && (u[x] = tg, fal[x] = far[x]), x == fal[x] ? x : fal[x] = getlf(fal[x]); }
void mel(int x, int y) {
  if ((x = getlf(x)) == (y = getlf(y))) return ;
  fal[x] = y, --cntl;
}
int query(int l, int r) {
  for (int i = max(lst, mid) + 1; i <= r; ++i) {
    ++cntr;
    for (int y : es[i]) if (mid < y && y <= r) mer(i, y);
  }
  lst = r, cntl = 0;
  for (int i = l; i <= min(r, mid); ++i) {
    ++cntl;
    for (int y : es[i]) if (l <= y && y <= r) mel(i, y);
  }
  return cntl + cntr;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  for (int _ = 1; _ <= tt; ++_) {
    cin >> n >> m;
    for (int i = 1; i <= n; ++i) es[i].clear(), u[i] = st[i] = 0;
    for (int i = 1; i <= m; ++i) {
      int x, y;
      cin >> x >> y;
      es[x].push_back(y), es[y].push_back(x);
    }
    cin >> q;
    blk = sqrt(1. * n * n / q) + 1;
    for (int i = 1; i <= n; ++i) {
      if (!st[i / blk]) st[i / blk] = i;
      ed[i / blk] = i;
    }
    for (int i = 1; i <= q; ++i) cin >> Q[i].l >> Q[i].r, Q[i].i = i;
    sort(Q + 1, Q + q + 1);
    for (int i = 1; i <= q; ++i) {
      int j = i;
      while (j < q && Q[j + 1].l / blk == Q[i].l / blk) ++j;
      mid = lst = ed[Q[i].l / blk], cntr = 0;
      for (int k = st[Q[i].l / blk]; k <= n; ++k) far[k] = k;
      for (int k = i; k <= j; ++k) {
        tg = k;
        ans[Q[k].i] = query(Q[k].l, Q[k].r);
        // cerr << Q[k].l << ' ' << Q[k].r << ' ' << Q[k].i << '\n';
      }
      i = j;
    }
    cout << "Case #" << _ << ":\n";
    for (int i = 1; i <= q; ++i) cout << ans[i] << '\n';
  }
}
```

### P14378
vp 一下。

容易发现我们把所有颜色的值转化成一个 $c$，那么我们对 $a, c$ 升降序排列，大的加小的。

于是可以单次 $O(n)$。

注意到询问可以使一个位置移动，于是可以分成三段，左右侧不变，中间段会错位。

于是用 st 表记录 $a_i + c_i, a_{i - 1} + c_i, a_{i + 1} + c_i$ 三个的最值即可，$O((n + q) \log n)$。

有点细节，写了 $40$ min，菜菜菜菜。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 5e5 + 9, inf[2] = {0x3f3f3f3f, -0x3f3f3f3f};
int n, k, q, a[N], o[N], rk[N], add[N];
int st[2][3][20][N]; // 0/1: min/max; 0/1/2 i - 1/i/i + 1;
pair<int, int> b[N];
int get(int x, int y, int t) { return t ? max(x, y) : min(x, y); }
int query(int x, int y, int t, int s) {
  if (x > y) return inf[t];
  int d = __lg(y - x + 1);
  return get(st[t][s][d][x], st[t][s][d][y - (1 << d) + 1], t);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> k >> q;
  for (int i = 1; i <= n; ++i) cin >> a[i], o[i] = i;
  for (int i = 1; i <= k; ++i) cin >> b[i].second;
  for (int i = 1; i <= k; ++i) cin >> b[i].first;
  sort(b + 1, b + k + 1);
  for (int i = 1, p = 1; i <= k; ++i)
    for (int j = 1; j <= b[i].second; ++j) add[p++] = b[i].first;
  sort(o + 1, o + n + 1, [&](int x, int y) -> bool { return a[x] > a[y]; });
  for (int i = 1; i <= n; ++i) rk[o[i]] = i;
  sort(a + 1, a + n + 1, greater<int>());
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j < 3; ++j) {
      st[0][j][0][i] = st[1][j][0][i] = a[i + j - 1] + add[i];
      if (i + j - 1 < 1 || i + j - 1 > n) st[0][j][0][i] = inf[0], st[1][j][0][i] = inf[1];
    }
  }
  for (int p = 0; p < 2; ++p) {
    for (int q = 0; q < 3; ++q) {
      for (int i = 1; i < 20; ++i) {
        for (int j = 1; j + (1 << i) - 1 <= n; ++j) st[p][q][i][j] = get(st[p][q][i - 1][j], st[p][q][i - 1][j + (1 << (i - 1))], p);
      }
    }
  }
  // for (int i = 1; i <= n; ++i) cerr << a[i] << ' ';
  // cerr << '\n';
  // for (int i = 1; i <= n; ++i) cerr << rk[i] << ' ';
  // cerr << '\n';
  // for (int i = 1; i <= n; ++i) cerr << add[i] << ' ';
  // cerr << '\n';
  // cerr << query(3, 5, 0, 1) << '\n';
  // cerr << query(3, 5, 1, 1) << '\n';
  // return 0;
  while (q--) {
    int x, y;
    cin >> x >> y;
    int p1 = lower_bound(a + 1, a + n + 1, y, greater<int>()) - a, p2 = rk[x];
    if (p1 > p2) --p1;
    // cerr << p1 << ' ' << p2 << '\n';
    int mn = y + add[p1], mx = y + add[p1];
    cmin(mn, query(1, min(p1, p2) - 1, 0, 1));
    cmax(mx, query(1, min(p1, p2) - 1, 1, 1));
    cmin(mn, query(max(p1, p2) + 1, n, 0, 1));
    cmax(mx, query(max(p1, p2) + 1, n, 1, 1));
    if (p1 < p2) {
      cmin(mn, query(p1 + 1, p2, 0, 0));
      cmax(mx, query(p1 + 1, p2, 1, 0));
    }
    if (p2 < p1) {
      cmin(mn, query(p2, p1 - 1, 0, 2));
      cmax(mx, query(p2, p1 - 1, 1, 2));
    }
    cout << mx - mn << '\n';
  }
}


/*



1 5 2 3 4
1 2 3 4 5

1 3 4 5 2
1 2 3 4 5

8  4 4 4
4 4 5 6 6



*/
```

### P14379
显然从 $f$ 入手。

我们观察一下可以发现是 $\text{mex}$，于是尝试分类讨论。

分讨 $1, 2$ 是否存在及其位置，可以得到 $f(l, r) = 1$ 的充要条件为：
- $[l, r]$ 中有 $1$。
- $[l, r]$ 有 $2$ 或 $a_l \neq 1$ 或 $a_r \neq 1$。

两个都需满足。

直接计算似乎不太好做（？）考虑正难则反，我们计算 $f(l, r) = 0$ 的，即：
- $[l, r]$ 中无 $1$。
- $[l, r]$ 中无 $2$ 且 $a_l = a_r = 1$。

满足其一即可。

这个是容易的，开两个 set 记录 $1, 2$ 的位置，然后每次修改考虑维护偏移量即可。

$O(q\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e6 + 9;
int n, q, a[N], s[N];
set<int> ps1, ps2;
void update(int x, int y) { for (; x <= n; x += x & -x) s[x] += y; }
int query(int x, int r = 0) { for (; x > 0; x -= x & -x) r += s[x]; return r; }
int get(int l, int r) { return query(r) - query(l - 1); }
int calc1(int l, int r) { return (r - l - 2) * (r - l - 1) / 2; }
int calc2(int l, int r, int t = 0) { return t = get(l, r - 1), t * (t - 1) / 2; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  ps1.insert(0), ps2.insert(0), ps1.insert(n + 1), ps2.insert(n + 1);
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
    if (a[i] == 1) ps1.insert(i);
    if (a[i] == 2) ps2.insert(i);
    update(i, a[i] == 1);
  }
  int res = 0;
  for (auto it = next(ps1.begin()); it != ps1.end(); ++it) {
    res += calc1(*prev(it), *it);
  }
  for (auto it = next(ps2.begin()); it != ps2.end(); ++it) {
    res += calc2(*prev(it), *it);
  }
  while (q--) {
    int x, y;
    cin >> x >> y;
    if (a[x] == 1) {
      auto it = ps1.lower_bound(x);
      res -= calc1(*prev(it), *it);
      res -= calc1(*it, *next(it));
      res += calc1(*prev(it), *next(it));
      ps1.erase(it);
    }
    if (a[x] == 2) {
      auto it = ps2.lower_bound(x);
      res -= calc2(*prev(it), *it);
      res -= calc2(*it, *next(it));
      res += calc2(*prev(it), *next(it));
      ps2.erase(it);
    }
    auto it = ps2.lower_bound(x);
    // int t = 0;
    // for (auto it = next(ps1.begin()); it != ps1.end(); ++it) {
    //   t += calc1(*prev(it), *it);
    // }
    // for (auto it = next(ps2.begin()); it != ps2.end(); ++it) {
    //   t += calc2(*prev(it), *it);
    // }
    // cerr << res << ' ' << t << '\n';
    res -= calc2(*prev(it), *it);
    update(x, -(a[x] == 1));
    a[x] = y;
    update(x, a[x] == 1);
    res += calc2(*prev(it), *it);
    if (a[x] == 1) {
      auto it = ps1.insert(x).first;
      res -= calc1(*prev(it), *next(it));
      res += calc1(*prev(it), *it);
      res += calc1(*it, *next(it));
    }
    if (a[x] == 2) {
      auto it = ps2.insert(x).first;
      res -= calc2(*prev(it), *next(it));
      res += calc2(*prev(it), *it);
      res += calc2(*it, *next(it));
    }
    // t = 0;
    // for (auto it = next(ps1.begin()); it != ps1.end(); ++it) {
    //   t += calc1(*prev(it), *it);
    // }
    // for (auto it = next(ps2.begin()); it != ps2.end(); ++it) {
    //   t += calc2(*prev(it), *it);
    // }
    // cerr << res << ' ' << t << '\n';
    cout << n * (n - 1) / 2 - res << '\n';
  }
}
```
