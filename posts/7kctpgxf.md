---
title: "记录 续 续 续 续"
date: 2025-11-17T19:21:58+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/7kctpgxf"
luogu_id: "7kctpgxf"
---

2025.11.17
### AT_agc043_d

首先序列长度为 $3$，假设取了一个 $x_1$，接下来取得数满足什么条件？

显然如果取其它开头，那么必然大于 $x_1$，否则就只能取当前序列。由于长度为 $3$，所以所有递减子区间长度 $\le 3$，而这些子区间就是同时取了一个序列。显然对于不同序列取得开头必然递增的，所以排列被划分为多个段，每个段长度 $\le 3$，开头为前缀最大值。

容易发现长度为 $1$ 的段和长度为 $2$ 的段拼起来即可得到一个序列，那么如果 $2$ 的段数多于 $1$ 的，必然无法拼出。

由此可以得到排列的构造方法。

然后直接 dp 即可，$f_{i, j}$ 表示 $i$ 个数，$1$ 的段数 $-$ $2$ 的段数为 $j$。

转移时，段首是固定的，而其余几个位置可以随意选择。

$O(n^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2009, M = 3 * N;
int n, md, f[3 * N][2 * M];
signed main() {
  cin >> n >> md;
  f[0][M] = 1;
  for (int i = 0; i < 3 * n; ++i) {
    for (int j = -i; j <= i; ++j) {
      (f[i + 1][j + 1 + M] += f[i][j + M]) %= md;
      (f[i + 2][j - 1 + M] += f[i][j + M] * (i + 1)) %= md;
      (f[i + 3][j + M] += f[i][j + M] * (i + 1) * (i + 2) % md) %= md;
    }
  }
  int ans = 0;
  for (int i = 0; i <= 3 * n; ++i) (ans += f[3 * n][M + i]) %= md;
  cout << ans;
}
```

### P14520
梦熊模拟赛。

观察大样例有单调性，直接二分。

稍微观察一下，发现如果一方缩起来，另一方必然追不上，只能也缩起来，所以直接判断两人的总和大小即可。

但是小 L 先手，所以可以提前吃掉一个，也判一下即可。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
int n, a[N];
bool chk(int x) {
  int pr = 0, sf = 0;
  for (int i = 1; i <= x; ++i) pr += a[i];
  for (int i = x + 1; i <= n; ++i) sf += a[i];
  if (pr > sf) return true;
  if (a[x] > a[x + 1] && a[x] + a[x + 1] > a[x + 2]) return pr + a[x + 1] * 2 > sf;
  return false;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n;
    a[n + 1] = 0;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    int l = 0, r = n + 1;
    while (l < r) {
      int m = (l + r) >> 1;
      if (chk(m)) r = m;
      else l = m + 1;
    }
    for (int i = 1; i < n; ++i) cout << (i >= l);
    cout << '\n';
  }
}
```

### P14521
直接 dfs，反求出到达每个点的 $x$ 的限制区间，然后直接离散化差分前缀和一下即可。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
char buf[1 << 26], *p1, *p2, obuf[1 << 25], *O = obuf;
#define gc (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 1 << 26, stdin)) == p1 ? EOF : *p1++)
#define pc(x) (*O++ = (x))
#define flush() (fwrite(obuf, 1, O - obuf, stdout))
template<class T> inline void read(T &x) {
  x = 0;
  bool f = false;
  char c = gc;
  for (; c < '0' || '9' < c; c = gc) f |= c == '-';
  for (; '0' <= c && c <= '9'; c = gc) x = (x << 1) + (x << 3) + (c & 15);
  if (f) x = -x;
}
template<class T> inline void write(T x) {
  if (x > 9) write(x / 10);
  pc(x % 10 + '0');
}
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 5e5 + 9;
int n, q, cn, fa[N], a[N], b[N * 4], c[N * 4], Q[2 * N];
vector<tuple<int, int, int>> es[N];
pair<int, int> seg[N];
void dfs(int x, int s, int L, int R) {
  for (auto [y, l, r] : es[x]) {
    seg[y] = {max(L, l - s), min(R, r - s)};
    if (seg[y].first > seg[y].second) continue;
    dfs(y, s + a[y], seg[y].first, seg[y].second);
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  read(n), read(q);
  for (int i = 2; i <= n; ++i) {
    int l, r;
    read(fa[i]), read(l), read(r);
    es[fa[i]].emplace_back(i, l, r);
  }
  for (int i = 1; i <= n; ++i) {
    char c = gc;
    for (; c != '-' && c != '+'; c = gc);
    read(a[i]);
    if (c == '-') a[i] = -a[i];
    seg[i] = {1, -1};
  }
  seg[1] = {-1e18, 1e18};
  dfs(1, a[1], -1e18, 1e18);
  for (int i = 1; i <= q; ++i) read(Q[i]), b[++cn] = Q[i];
  for (int i = 1; i <= n; ++i)
    if (seg[i].first <= seg[i].second) b[++cn] = seg[i].first, b[++cn] = seg[i].second;
  sort(b + 1, b + cn + 1);
  cn = unique(b + 1, b + cn + 1) - b - 1;
  for (int i = 1; i <= n; ++i) {
    if (seg[i].first > seg[i].second) continue;
    int l = lower_bound(b + 1, b + cn + 1, seg[i].first) - b;
    int r = lower_bound(b + 1, b + cn + 1, seg[i].second) - b;
    ++c[l], --c[r + 1];
  }
  for (int i = 1; i <= cn; ++i) c[i] += c[i - 1];
  for (int i = 1; i <= q; ++i) write(c[lower_bound(b + 1, b + cn + 1, Q[i]) - b]), pc('\n');
  return flush(), 0;
}
```

### P14522
操作等价于 $x - (x \And y)$。

显然 $x \ominus y \le x$，所以我们考虑能否把一堆数凑出 $0$。

首先把最大值去掉。

观察到有 $x \And y$，那么只要某一位出现了多个 $1$，必然可以同操作使得这一位变为 $0$。

具体的，我们按顺序操作，$1$ 和 $1$ 变为 $0$，然后 $0$ 和 $1$ 会变为 $0$，所以每次合并必然会把出现大于 $1$ 次的位置变为 $0$。

而只出现一次的位最多有 $\log V$ 个，因此最多 $\log V + 1 = 26$ 个数，就必然可以凑出 $0$。

再加上最大值即为 $27$。

也就是说长度大于等于 $27$ 的区间必然是区间最大值。

而其余的区间直接暴力即可。

暴力的话，考虑 $a_k \ominus (a_l\ominus \dots)$，我们枚举 $k, l$，考虑计算后面部分。观察每一位可以发现，出现次数大于 $2$ 的位必然为 $0$，而其余位设为 $S$，那么 $a_k \ominus (a_l \And S)$ 必然正确，具体可以考虑分讨 $1$ 在那些部分。

大于部分，直接最大值分治即可，$O(n\log n)$。

$O(n\log^3 n)$，可过。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
char buf[1 << 26], *p1, *p2;
#define gc (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 1 << 26, stdin)) == p1 ? EOF : *p1++)
template<class T> inline void read(T &x) {
  x = 0;
  bool f = false;
  char c = gc;
  for (; c < '0' || '9' < c; c = gc) f |= c == '-';
  for (; '0' <= c && c <= '9'; c = gc) x = (x << 1) + (x << 3) + (c & 15);
  if (f) x = -x;
}
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e5 + 9, K = 26, md = 998244353;
int n, a[N], vst[N], ans, s[N][K], lft[N], rht[N], st[20][N];
int get(int x, int y) { return a[x] > a[y] ? x : y; }
int query(int l, int r) {
  int d = __lg(r - l + 1);
  return get(st[d][l], st[d][r - (1 << d) + 1]);
}
void dfs(int l, int r) {
  if (l > r) return ;
  int m = query(l, r);
  dfs(l, m - 1), dfs(m + 1, r);
  if (m - l < r - m) {
    for (int i = l; i <= m; ++i) {
      int R = max(m, i + K);
      if (R > r) continue;
      (ans += (r - R + 1) * a[m]) %= md;
    }
  }
  else {
    for (int i = m; i <= r; ++i) {
      int L = min(i - K, m);
      if (L < l) continue;
      (ans += (L - l + 1) * a[m]) %= md;
    }
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  read(n);
  for (int i = 1; i <= n; ++i) {
    read(a[i]), st[0][i] = i;
    (ans += a[i]) %= md, lft[i] = i - 1, rht[i] = i + 1;
    for (int j = 0; j < K; ++j) s[i][j] = s[i - 1][j] + (a[i] >> j & 1);
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = i + 1; j <= i + K - 1 && j <= n; ++j) {
      int x = 0, res = 0;
      for (int k = 0; k < K; ++k)
        if (s[j][k] - s[i - 1][k] <= 2) x |= 1 << k;
      for (int k = i; k <= j; ++k) {
        int y = x & a[k];
        int mn = y;
        for (int l = i; l <= j; ++l)
          if (l != k) cmin(mn, y & a[l]);
        cmax(res, a[k] - mn);
      }
      (ans += res) %= md;
    }
  }
  for (int i = 1; i < 20; ++i)
    for (int j = 1; j + (1 << i) - 1 <= n; ++j) st[i][j] = get(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
  dfs(1, n);
  cout << ans;
}
```

--------
2025.11.18
### P5537 【XR-3】系统设计
考虑 $x \to y$ 记录每条边的编号，可以构成一个字符串，那么问题即为找到 $x\to y$ 的字符串与 $a_l, \dots, a_r$ 的最长匹配。

直接用 unordered_map 存 $1\to x$ 的哈希值，然后用树状数组维护 $a$ 的哈希值。

询问直接二分即可，卡了单模哈希差评。

不想写线段树上二分。

$O(n\log^2 n)$。

卡常。

```cpp
#include <bits/stdc++.h>
using namespace std;
char buf[1 << 26], *p1, *p2;
#define gc (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 1 << 26, stdin)) == p1 ? EOF : *p1++)
template<class T> inline void read(T &x) {
  x = 0;
  bool f = false;
  char c = gc;
  for (; c < '0' || '9' < c; c = gc) f |= c == '-';
  for (; '0' <= c && c <= '9'; c = gc) x = (x << 1) + (x << 3) + (c & 15);
  if (f) x = -x;
}
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 5e5 + 9;
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
hash_t h[N], ha[N], pw[N], c[N], ipw[N];
int n, m, q, fa[N], rt, a[N], dep[N], L;
vector<int> es[N];
unordered_map<u64, int> mp;
hash_t inv(hash_t a, int b = hash_t::hmod - 2) {
  hash_t r = 1;
  for (; b > 0; b >>= 1, a = a * a)
    if (b & 1) r = r * a;
  return r;
}
void update(int x, hash_t y) {
  for (; x <= L; x += x & -x) c[x] += y;
}
hash_t query(int x, hash_t r = 0) {
  for (; x > 0; x -= x & -x) r += c[x];
  return r;
}
int query(int l, int r) {
  int u = 0;
  for (int i = 19; i >= 0; --i) {
    if ((u + (1 << i)) > r) continue;
  }
  return u;
}
void dfs(int x, int ff) {
  int s = 0; dep[x] = dep[ff] + 1;
  mp[h[x].h] = x;
  for (int y : es[x]) {
    h[y] = h[x] + hash_t::shift(++s) * pw[L - dep[x]];
    dfs(y, x);
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> q;
  L = max(n, m);
  for (int i = 1; i <= n; ++i) {
    cin >> fa[i];
    if (fa[i] == 0) rt = i;
    else es[fa[i]].push_back(i);
  }
  pw[0] = 1;
  for (int i = 1; i <= L; ++i) pw[i] = pw[i - 1] * seed;
  ipw[L] = inv(pw[L]);
  for (int i = L - 1; i >= 0; --i) ipw[i] = ipw[i + 1] * seed;
  for (int i = 1; i <= m; ++i) cin >> a[i], update(i, hash_t::shift(a[i]) * pw[L - i]);
  dfs(rt, 0);
  // cerr << (h[6] - h[1] + md) % md * pw[dep[1] - 1] << '\n';
  while (q--) {
    int o, x, l, r;
    cin >> o >> x >> l;
    if (o == 1) {
      cin >> r;
      // cerr << (query(r) - query(l - 1)) * pw[l - 1] % md << '\n';
      int L = l - 1, R = r;
      while (L < R) {
        int mid = (L + R + 1) >> 1;
        hash_t hsh = (query(mid) - query(l - 1)) * pw[l - 1] * ipw[dep[x] - 1] + h[x];
        if (mp.count(hsh.h)) L = mid;
        else R = mid - 1;
      }
      cout << mp[((query(L) - query(l - 1)) * pw[l - 1] * ipw[dep[x] - 1] + h[x]).h] << '\n';
    }
    else {
      update(x, hash_t::hmod - hash_t::shift(a[x]) * pw[L - x]);
      a[x] = l;
      update(x, hash_t::shift(a[x]) * pw[L - x]);
    }
  }
}
```

-----------
2025.11.20
### AT_agc046_e
构造。

唯一难点：如何判断无解。

首先考虑出现次数最少的数字 $x$，和最多的 $y$。

那么对于每个 $y$，一定有一个 $x$ 与其距离不超过 $k$。

所以序列是成这样的 $\dots y\dots x\dots y\dots y\dots x\dots y\dots$。

容易发现如果 $a_y > 2a_x$ 那么必然是无法满足的，所以有解的必要条件是 $a_y \le 2a_x$。

考虑充分性，我们只要构造出这个序列即可。

首先，我们每次先把所有的 $z_i$ 满足 $a_{z_i} = a_x$ 找出来，也就是出现次数最少的几个数，然后对于其余所有数字，必然出现次数 $\ge 2$，我们左右各放一个即可，这样最小值 $-1$ 其余的 $-2$，可以归纳证明。

然后我们考虑如何构造字典序最小。

显然按位贪心，由于每个位置都存在包含其的排列，我们可以每次往序列中加入一段数，使得最后 $k$ 个是排列。

枚举加入的数的个数 $l$，由于已知是排列，所以这 $l$ 个数字是固定的。我们考虑如果加入当前这段，剩余数字也要满足前文判断无解的条件，所以如果 $\max \le 2\min$ 就可以。

但是 $\max > 2\min$ 并不一定不可以，因为在加入时前面已经放了数字。

但是 $\max > 2 \min + 1$ 显然不行，而 $\max = 2 \min + 1$ 的情况，需要满足最大值在最小值前面而其余直接按字典序即可。

$O(k^2\sum a_i)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9, inf = 10000;
int n, k, a[N], mx, mn = inf, ans[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> k;
  a[0] = inf, a[k + 1] = -inf;
  for (int i = 1; i <= k; ++i) cin >> a[i], cmin(mn, a[i]), cmax(mx, a[i]), n += a[i];
  if (2 * mn < mx) return cout << -1, 0;
  int fx = 0;
  while (fx < n) {
    vector<int> vec = {inf};
    cerr << fx << '\n';
    for (int l = 1; l <= n - fx && l <= k; ++l) {
      vector<int> b;
      map<int, int> mp;
      if (fx + l < k) continue;
      for (int i = fx + l - k + 1; i <= fx; ++i) mp[ans[i]] = 1;
      for (int i = 1; i <= k; ++i)
        if (!mp.count(i)) b.push_back(i), --a[i];
      int pmn = inf, pmx = -inf;
      for (int i = 1; i <= k; ++i) {
        cmax(pmx, a[i]), cmin(pmn, a[i]);
      }
      cerr << pmn << ' ' << pmx << '\n';
      if (pmn * 2 >= pmx) cmin(vec, b);
      else if (pmn * 2 + 1 == pmx) {
        vector<int> ls, rs, md;
        b.clear();
        for (int i = 1; i <= k; ++i)
          if (!mp.count(i)) {
            if (a[i] == pmn) rs.push_back(i);
            else if (a[i] == pmx) ls.push_back(i);
            else md.push_back(i);
          }
        int p = 0;
        for (int i : ls) {
          while (p < md.size() && md[p] < i) b.push_back(md[p++]);
          b.push_back(i);
        }
        for (int i : rs) {
          while (p < md.size() && md[p] < i) b.push_back(md[p++]);
          b.push_back(i);
        }
        while (p < md.size()) b.push_back(md[p++]);
        cmin(vec, b);
      }
      for (int i = 1; i <= k; ++i)
        if (!mp.count(i)) ++a[i];
    }
    for (int i : vec) ans[++fx] = i, --a[i];
  }
  for (int i = 1; i <= n; ++i) cout << ans[i] << ' ';
}
```

-----------
2025.11.21
### P10743
很神秘。

----------
2025.11.22
### P14413
考虑 dp，$f_{i, j, k, 0/1, 0/1}$ 表示前三张牌以及下一个能否选 $i$ 和 $k$。

滚动掉 $i$，$O(n^3)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 509;
int n, c[N], a[N], v[N], f[2][N][N][2][2], ans;
int can(int x, int y) {
  return c[x] == c[y] || a[x] == a[y];
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> c[i] >> a[i] >> v[i];
  int ans = 0;
  memset(f, -0x3f, sizeof f);
  f[1][1][2][1][1] = 0;
  for (int k = 3; k <= n + 3; ++k) {
    for (int i = 1; i <= n + 1; ++i)
      for (int j = i + 1; j <= k && j <= n + 2; ++j) 
        for (int p = 0; p < 2; ++p) for (int q = 0; q < 2; ++q) f[k & 1 ^ 1][i][j][p][q] = -0x3f3f3f3f;
    for (int i = 1; i <= n + 1; ++i) {
      for (int j = i + 1; j < k && j <= n + 2; ++j) {
        cmax(f[k & 1 ^ 1][i][j][can(k, i)][can(k, k + 1)], f[k & 1][i][j][0][1] + v[k]);
        cmax(f[k & 1 ^ 1][i][j][can(k, i)][can(k, k + 1)], f[k & 1][i][j][1][1] + v[k]);
        cmax(f[k & 1 ^ 1][j][k][can(i, j)][can(i, k + 1)], f[k & 1][i][j][1][0] + v[i]);
        cmax(f[k & 1 ^ 1][j][k][can(i, j)][can(i, k + 1)], f[k & 1][i][j][1][1] + v[i]);
        cmax(ans, f[k & 1][i][j][0][0]);
        cmax(ans, f[k & 1][i][j][1][0]);
        cmax(ans, f[k & 1][i][j][0][1]);
        cmax(ans, f[k & 1][i][j][1][1]);
      }
    }
  }
  cout << ans;
}
```
### P11792
比 T3 简单。

考虑二分，然后分割是形如阶梯状的，check 考虑枚举每一行最远扩展到的位置。

我们假设扩展的区域包含最大值，那么当前二分答案为 $x$，则要求所有数 $\in [\max - x, \max]$，于是可以 $O(n^2)$ 枚举。

我们枚举的区域有 $8$ 种可能，直接写容易被卡常，加点剪枝即可。

$O(n^2\log V)$。

check 内部也可以二分做到 $O(n\log V \log n)$，懒得写。

```
#include <bits/stdc++.h>
using namespace std;
template <class T> bool cmax(T& x, const T& y) { if (x < y) return x = y, true; return false; }
template <class T> bool cmin(T& x, const T& y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2009, inf = 0x3f3f3f3f;
int n, m, a[N][N], mx, mn = inf;
bool chk(int x) {
  int rmx = 0, rmn = inf;
  for (int i = 1, le = m; i <= n; ++i) {
    int nw = 0;
    while (nw < le && mx - a[i][nw + 1] <= x) ++nw;
    for (int j = nw + 1; j <= m; ++j) cmax(rmx, a[i][j]), cmin(rmn, a[i][j]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  rmx = 0, rmn = inf;
  for (int i = n, le = m; i >= 1; --i) {
    int nw = 0;
    while (nw < le && mx - a[i][nw + 1] <= x) ++nw;
    for (int j = nw + 1; j <= m; ++j) cmax(rmx, a[i][j]), cmin(rmn, a[i][j]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  rmx = 0, rmn = inf;
  for (int i = 1, le = n; i <= m; ++i) {
    int nw = 0;
    while (nw < le && mx - a[nw + 1][i] <= x) ++nw;
    for (int j = nw + 1; j <= n; ++j) cmax(rmx, a[j][i]), cmin(rmn, a[j][i]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  rmx = 0, rmn = inf;
  for (int i = m, le = n; i >= 1; --i) {
    int nw = 0;
    while (nw < le && mx - a[nw + 1][i] <= x) ++nw;
    for (int j = nw + 1; j <= n; ++j) cmax(rmx, a[j][i]), cmin(rmn, a[j][i]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  rmx = 0, rmn = inf;
  for (int i = 1, le = m; i <= n; ++i) {
    int nw = 0;
    while (nw < le && mx - a[i][m - (nw + 1) + 1] <= x) ++nw;
    for (int j = nw + 1; j <= m; ++j) cmax(rmx, a[i][m - j + 1]), cmin(rmn, a[i][m - j + 1]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  rmx = 0, rmn = inf;
  for (int i = n, le = m; i >= 1; --i) {
    int nw = 0;
    while (nw < le && mx - a[i][m - (nw + 1) + 1] <= x) ++nw;
    for (int j = nw + 1; j <= m; ++j) cmax(rmx, a[i][m - j + 1]), cmin(rmn, a[i][m - j + 1]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  rmx = 0, rmn = inf;
  for (int i = 1, le = n; i <= m; ++i) {
    int nw = 0;
    while (nw < le && mx - a[n - (nw + 1) + 1][i] <= x) ++nw;
    for (int j = nw + 1; j <= n; ++j) cmax(rmx, a[n - j + 1][i]), cmin(rmn, a[n - j + 1][i]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  rmx = 0, rmn = inf;
  for (int i = m, le = n; i >= 1; --i) {
    int nw = 0;
    while (nw < le && mx - a[n - (nw + 1) + 1][i] <= x) ++nw;
    for (int j = nw + 1; j <= n; ++j) cmax(rmx, a[n - j + 1][i]), cmin(rmn, a[n - j + 1][i]);
    if (rmx - rmn > x) break;
    le = nw;
  }
  if (rmx - rmn <= x) return true;
  return false;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) cin >> a[i][j], cmax(mx, a[i][j]), cmin(mn, a[i][j]);
  }
  int l = 0, r = mx - mn;
  while (l < r) {
    int mid = (l + r) >> 1;
    if (chk(mid)) r = mid;
    else l = mid + 1;
  }
  cout << l;
}
```
-----------
2025.11.26
### P6533
首先容易得到一个 $O(qnc)$ 的暴力 dp。

注意到这个东西可以矩阵优化，直接做完了，但是卡空间。

观察可以发现只有 $O(c)$ 个值是有用的，其余都是 $0$，所以我们可以直接记录。

或者说，直接记录一个区间的 dp 数组，$f_i$ 表示选了 $i$ 个人买彩色。

然后 $f, g$ 容易合并，是一个卷积的形式，$O(c^2)$。

总时间复杂度 $O(qc^2\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9, md = 1e4 + 7;
int inv(int a, int b = md - 2) {
  int r = 1;
  for (; b > 0; b >>= 1, a = a * a % md)
    if (b & 1) r = r * a % md;
  return r;
}
int n, c, q, a[N], b[N];
using info = array<int, 20>;
info sgt[N << 2];
info operator+(const info &lhs, const info &rhs) {
  info res = {};
  for (int i = 0; i < c; ++i)
    for (int j = 0; i + j < c; ++j) {
      (res[i + j] += lhs[i] * rhs[j]) %= md;
    }
  return res;
}
void build(int u, int l, int r) {
  if (l == r) {
    sgt[u][0] = b[l], sgt[u][1] = a[l];
    return ;
  }
  int m = (l + r) >> 1;
  build(u << 1, l, m), build(u << 1 | 1, m + 1, r);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
void update(int u, int l, int r, int x) {
  if (l == r) {
    sgt[u][0] = b[l], sgt[u][1] = a[l];
    return ;
  }
  int m = (l + r) >> 1;
  if (m >= x) update(u << 1, l, m, x);
  else update(u << 1 | 1, m + 1, r, x);
  sgt[u] = sgt[u << 1] + sgt[u << 1 | 1];
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> c;
  int all = 1;
  for (int i = 1; i <= n; ++i) cin >> a[i], a[i] %= md;
  for (int i = 1; i <= n; ++i) cin >> b[i], b[i] %= md, (all *= a[i] + b[i]) %= md;
  build(1, 1, n);
  cin >> q;
  while (q--) {
    int p, x, y;
    cin >> p >> x >> y;
    x %= md, y %= md;
    (all *= inv(a[p] + b[p])) %= md;
    a[p] = x, b[p] = y;
    (all *= a[p] + b[p]) %= md;
    update(1, 1, n, p);
    int ans = 0;
    for (int i = 0; i < c; ++i) (ans += sgt[1][i]) %= md;
    cout << (all - ans + md) % md << '\n';
  }
}

/*


f[i][j] = f[i - 1][j] * b[i]
f[i][j] = f[i - 1][j - 1] * a[i]


f[n][c]


[f[i - 1][0] f[i - 1][1] .... f[i - 1][c - 1]]    [b[i] a[i] 0     ...   0   ]  =  [f[i][0] f[i][1] ...... f[i][c - 1]]
                                                  [0    b[i] a[i]  ...   0   ]
                                                  [0    0    b[i]  ...   0   ]
                                                  [0    0    0     ...   0   ]
                                                  .
                                                  .
                                                  .
                                                  [0    0    0     ...   b[i]]

*/
```

-----------
2025.11.30
### P14638
学会了。

首先有一个分治的 $O(nq\log n)$ 做法。令 $[x, y]$ 表示当前分治的区间，$[l, r]$ 表示我们找到的满足条件的区间。那么每次钦定 $x \le l \le mid \le r \le y$，用 st 表维护前缀和的最值，对于左右子区间分别枚举 $l, r$ 计算，容易做到单次 $O(n)$。

然后考虑一点小剪枝：每次枚举端点时，都有一段前缀是不合法的，我们直接跳过这一段，这样单次复杂度就是 $O(\min(R, y - x + 1))$。

还有另一个小剪枝，就是如果当前区间长度 $ < L$ 直接 return。

这样的时间复杂度是 $O((\log \frac nL - \log \frac nR) n + R \log \frac nR)$。

大致观察一下可以发现，后面的 $O(R\log \frac nR)$ 不是瓶颈，所以考虑如何优化 $O(n\log \frac RL)$。

考虑对限制 $[L, R]$ 分块，形如 $[2^k, 2^{k + 1})$。这样我们可以预处理出这 $\log n$ 块的答案，询问相当于对于两个散块和一堆整块查询。

整块可以用 st 表维护每个位置的最值，对于散块，可以发现一定满足 $\frac RL < 2$，所以直接暴力分治就是 $O(n)$。

然后就做完了，时间复杂度是 $O(n\log n + n\log^2 n + q(\log n + n))$。

本地大样例要跑 1.8 s，不过本来就卡常。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T& x, const T& y) { if (x < y) { x = y; return true; } return false; }
template<class T> inline bool cmin(T& x, const T& y) { if (x > y) { x = y; return true; } return false; }
constexpr int N = 5e4 + 9, M = __lg(N) + 2, inf = 1e18;
using u64 = uint64_t;
int n, a[N], q, s[N], f[N];
int st[2][M][N], g[M][N], st1[N][M][M];
int get(int x, int y, int t) { return t ? min(x, y) : max(x, y); }
int query(int l, int r, int t) {
  if (l > r) return t ? inf : -inf;
  int d = __lg(r - l + 1);
  return get(st[t][d][l], st[t][d][r - (1 << d) + 1], t);
}
int query1(int l, int r, int p) {
  int d = __lg(r - l + 1);
  return max(st1[p][d][l], st1[p][d][r - (1 << d) + 1]);
}
void dfs(int l, int r, int L, int R) {
  if (r - l + 1 < L) return ;
  if (l == r) return cmax(f[l], a[l]), void();
  int m = (l + r) >> 1;
  dfs(l, m, L, R), dfs(m + 1, r, L, R);
  for (int i = max(l, m - R + 2), pre = -inf; i <= m; ++i) {
    int x = max(m + 1, i + L - 1), y = min(r, i + R - 1);
    cmax(pre, query(x, y, 0) - s[i - 1]);
    cmax(f[i], pre);
  }
  for (int i = min(r, m + R - 1), suf = -inf; i > m; --i) {
    int x = max(l, i - R + 1), y = min(m, i - L + 1);
    cmax(suf, s[i] - query(x - 1, y - 1, 1));
    cmax(f[i], suf);
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i], s[i] = s[i - 1] + a[i];
  for (int i = 0; i <= n; ++i) st[0][0][i] = st[1][0][i] = s[i];
  for (int o = 0; o < 2; ++o)
    for (int i = 1; i < M; ++i)
      for (int j = 0; j + (1 << i) - 1 <= n; ++j) st[o][i][j] = get(st[o][i - 1][j], st[o][i - 1][j + (1 << (i - 1))], o);
  for (int i = 0; i < M; ++i) {
    int l = 1 << i, r = min((1LL << (i + 1)) - 1, n);
    if (l > n) break;
    for (int j = 1; j <= n; ++j) f[j] = -inf;
    dfs(1, n, l, r);
    for (int j = 1; j <= n; ++j) g[i][j] = f[j], st1[j][0][i] = f[j];
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j < M; ++j)
      for (int k = 0; k + (1 << j) - 1 < M; ++k) st1[i][j][k] = max(st1[i][j - 1][k], st1[i][j - 1][k + (1 << (j - 1))]);
  }
  cin >> q;
  while (q--) {
    int l, r;
    cin >> l >> r;
    for (int i = 1; i <= n; ++i) f[i] = -inf;
    int up = -1, low = M;
    for (int o = 0; o < M; ++o) {
      int L = 1 << o, R = min((1LL << (o + 1)) - 1, n);
      if (L > n) break;
      if (L <= l && l <= R) dfs(1, n, l, min(R, r));
      if (l <= L && R <= r) cmin(low, o), cmax(up, o);
      if (L <= r && r <= R) dfs(1, n, max(l, L), r);
    }
    if (low <= up)
      for (int i = 1; i <= n; ++i) cmax(f[i], query1(low, up, i));
    u64 res = 0;
    for (int i = 1; i <= n; ++i) res ^= (u64) i * f[i];
    cout << res << '\n';
  }
}
```
