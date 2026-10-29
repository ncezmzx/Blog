---
title: "记录"
date: 2025-10-10T08:46:39+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/nxgwm1e4"
luogu_id: "nxgwm1e4"
---

2025.10.10
### CF1257E
先把三段都排序，然后顺次拼接，记为 $b$。容易发现题目要求即为 $b$ 是升序排列。

每次操作等价于移动 $b$ 中一个元素。

考虑计算移动次数，显然一个元素最多移动一次。

令 $c$ 为 $b$ 的子序列，$c$ 中所有元素不操作，那么我们要最大化 $|c|$。

由于 $c$ 不操作，故 $c$ 必然是升序排列，所以最大化 $|c|$ 即为 $b$ 的最长上升子序列 $\text{LIS}$。

综上，操作次数最小为 $n - \text{LIS}$。

### CF632E
*2400

多重背包，但是限制了要买恰好 $k$ 个物品，求可以凑出的价值有哪些。

考虑把所有物品的价格减去 $\min$，这样只要在最后加上 $k\times \min$ 即可。

此时，必然存在价格为 $0$ 的物品，可以用这些物品来凑到 $k$ 个。

所以背包算出每个价格最少要多少物品，只要 $\leq k$，就可以用 $0$ 凑成 $k$。

最后记得加上 $k\times \min$。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1009;
int n, k, a[N], dp[N * N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> k;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  int mn = *min_element(a + 1, a + n + 1), mx = *max_element(a + 1, a + n + 1);
  for (int i = 1; i <= n; ++i) a[i] -= mn;
  sort(a + 1, a + n + 1);
  memset(dp, 0x3f, sizeof dp);
  dp[0] = 0;
  for (int i = 2; i <= n; ++i) {
    for (int j = a[i]; j <= mx * k; ++j) dp[j] = min(dp[j], dp[j - a[i]] + 1);
  }
  for (int i = 0; i <= mx * k; ++i) {
    if (dp[i] <= k) cout << i + mn * k << ' ';
  }
}
```

### CF1175F
*2500？

集训好像讲了。

首先，我们考虑如何 $O(1)$ 判断一个区间是否是排列。

我们可以为每个数 $1 \leq i \leq n$ 随机赋上一个权值 $v_i$。

考虑异或哈希，一个区间 $[l, r]$ 是否为排列可以通过 $\oplus_{l \leq i \leq r} v_{a_i} = \oplus_{i \leq r - l + 1} v_i$ 来判断。

接下来考虑如何统计。

一个区间 $[l, r]$ 是排列的必要条件是 $r - l + 1$ 为区间最大值。

所以我们可以按最大值分治，统计当前区间 $[l, r]$ 中跨过最大值 $m$ 的子区间个数，由于长度固定，直接枚举较小的一边 $O(1)$ 判断即可。

根据这个做法，容易发现我们总共判断的子区间是 $O(n \log n)$ 级别的，所以答案不会很大。

用别的做法可以证得答案是 $O(n)$ 的，但是我不会。

```cpp
#include <bits/stdc++.h>
using namespace std;
mt19937_64 rng(random_device{}());
constexpr int N = 3e5 + 9;
int n, a[N], st[20][N];
uint64_t h[N], b[N], ans;
bool is(int l, int r) { return (b[r] ^ b[l - 1]) == h[r - l + 1]; }
int get(int x, int y) { return a[x] > a[y] ? x : y; }
int query(int l, int r) {
  int d = __lg(r - l + 1);
  return get(st[d][l], st[d][r - (1 << d) + 1]);
}
void dfs(int l, int r) {
  if (l > r) return ;
  int m = query(l, r), len = a[m];
  dfs(l, m - 1), dfs(m + 1, r);
  if (m - l < r - m) {
    for (int i = max(l, m - len + 1); i <= m && i + len - 1 <= r; ++i) {
      ans += is(i, i + len - 1);
    }
  }
  else {
    for (int i = min(r, m + len - 1); i >= m && i - len + 1 >= l; --i) {
      ans += is(i - len + 1, i);
    }
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) h[i] = rng();
  for (int i = 1; i <= n; ++i) cin >> a[i], b[i] = h[a[i]] ^ b[i - 1], st[0][i] = i;
  for (int i = 1; i <= n; ++i) h[i] ^= h[i - 1];
  for (int i = 1; i < 20; ++i) {
    for (int j = 1; j + (1 << i) - 1 <= n; ++j) st[i][j] = get(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
  }
  dfs(1, n);
  cout << ans;
}
```

### CF339E
神秘构造。

显然反转操作是可逆的，所以考虑反过来，求将 $a$ 变成 ${1, 2, 3, \dots, n}$。

每次操作反转 $[l, r]$，$[1, l - 2]$、$[l + 2, r - 2]$、$[r +21, n]$ 中相邻的差不会改变，只有 $l - 1, l, l + 1, r - 1, r, r + 1$ 改变。

由于最多操作 $3$ 次，所以只有 $O(1)$ 个位置。

我们直接找出这些位置，然后枚举，dfs 即可。

复杂度 $O(n)$，常数巨大。

记得最后要反转求出来的操作序列。

### CF468C
又是神秘构造。

考虑 $\sum_{i = 0}^{10^{18} - 1} f(i) \equiv p \pmod a$。

那么 $\sum_{i = 1}^{10^{18}} f(i) \equiv p - f(0) + f(10^{18}) \equiv p + 1 \pmod a$。

归纳可得，$\sum_{i = x}^{10^{18} + x - 1} f(i) \equiv p + x \pmod a$。

先算出 $p = 18 \times 45 \times 10^{17}$，然后求出 $x$ 即可。

注意算 $p$ 的时候可能会炸 long long，可以把 $45$ 拆成 $9 \times 5$。

### CF839D
令 $f_i$ 表示 $\gcd = i$ 的所有子序列的长度之和，这个不好算。

令 $g_i$ 表示 $i \mid \gcd$ 的所有子序列的长度之和，这个很好算，直接调和级数算出每个 $i$ 的倍数个数 $s$，每个数可以为 $2^{s - 1}$ 个子序列的长度做出 $1$ 的贡献，所以 $g_i = s 2^{s - 1}$。

显然，$g_i = \sum_{i \mid j} f_j$。

考虑如何通过 $g$ 算出 $f$。

我们从大到小计算 $f, g$。对于 $i$，算出 $g_i$ 之后，所有的 $f_j$（$i < j$）都是已知的，我们直接枚举 $j > i, i \mid j$，从 $g_i$ 中减去 $f_j$ 即可得到 $f_i$。

$O(n \log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 2e5 + 9, V = 1e6 + 9, md = 1e9 + 7;
int n, a[N], cnt[V], pw[V], f[V], ans;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = pw[0] = 1; i < V; ++i) pw[i] = pw[i - 1] * 2 % md;
  for (int i = 1; i <= n; ++i) cin >> a[i], ++cnt[a[i]];
  for (int i = V - 9; i > 1; --i) {
    int s = 0;
    for (int j = i; j < V; j += i) s += cnt[j];
    f[i] = s * pw[s - 1] % md;
    for (int j = i << 1; j < V; j += i) (f[i] += md - f[j]) %= md;
    (ans += f[i] * i % md) %= md;
  }
  cout << ans;
}
```
### CF383E
*2700

不会。

考虑正难则反，求不正确的单词数。

令 $S$ 表示元音集合，$T$ 表示非元音集合。

容易发现，不正确的单词每个字母必然 $\in T$。

于是问题变成了求出每个集合 $T$，有多少单词不正确。

直接枚举 $O(2^{24} n)$。考虑把单词也转化为集合，则可以通过求子集和来算，$O(3^{24})$。

然后这个东西高维前缀和做一下就是 $O(2^{24}\times 24)$。

代码很好写。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 1e4 + 9;
int n, f[1 << 24];
string a[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
    int s = 0;
    for (auto j : a[i]) s |= 1 << (j - 'a');
    ++f[s];
  }
  for (int i = 0; i < 24; ++i) {
    for (int j = 0; j < 1 << 24; ++j)
      if (j >> i & 1) f[j] += f[j ^ (1 << i)];
  }
  int ans = 0;
  for (int i = 0; i < 1 << 24; ++i) ans ^= (n - f[i]) * (n - f[i]);
  cout << ans;
}
```

### CF323C
经典在线二位数点。

对于每个数 $i$，记其在 $p$ 中的位置 $x_i$，$q$ 中位置 $y_i$，则 $(x_i, y_i)$ 为二维平面上的点。

询问直接查一个矩形中的点的个数，强制在线，直接主席树就做完了。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1e6 + 9;
int n, m, p[N], q[N], ps[N];
int rt[N], ls[N << 5], rs[N << 5], sgt[N << 5], tot;
int build(int l, int r) {
  int u = ++tot;
  if (l == r) return u;
  int m = (l + r) >> 1;
  ls[u] = build(l, m), rs[u] = build(m + 1, r);
  return u;
}
int update(int u, int l, int r, int x) {
  int dir = ++tot;
  ls[dir] = ls[u], rs[dir] = rs[u], sgt[dir] = sgt[u] + 1;
  if (l == r) return dir;
  int m = (l + r) >> 1;
  if (m >= x) ls[dir] = update(ls[u], l, m, x);
  else rs[dir] = update(rs[u], m + 1, r, x);
  return dir;
}
int query(int u, int v, int l, int r, int x, int y) {
  if (sgt[u] == sgt[v]) return 0;
  if (x <= l && r <= y) return sgt[v] - sgt[u];
  int m = (l + r) >> 1, res = 0;
  if (m >= x) res += query(ls[u], ls[v], l, m, x, y);
  if (m < y) res += query(rs[u], rs[v], m + 1, r, x, y);
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> p[i];
  for (int i = 1; i <= n; ++i) cin >> q[i], ps[q[i]] = i;
  rt[0] = build(1, n);
  for (int i = 1; i <= n; ++i) rt[i] = update(rt[i - 1], 1, n, ps[p[i]]);
  cin >> m;
  int lst = 0;
  while (m--) {
    int a, b, c, d;
    cin >> a >> b >> c >> d;
    auto f = [&](int x) -> int { return (x - 1 + lst) % n + 1; };
    a = f(a), b = f(b), c = f(c), d = f(d);
    auto [l1, r1] = minmax(a, b);
    auto [l2, r2] = minmax(c, d);
    cout << (lst = query(rt[l1 - 1], rt[r1], 1, n, l2, r2)) << '\n';
    ++lst;
  }
}
```
### CF494C
*2600

好题！

首先 $E(\max a_i) \neq \max \{ E(a_i) \}$。

题目保证区间只有包含与不交两种情况，我们把包含关系看作边，可以得到一个森林。

人为加入一个 $l = 1, r = n, p = 0$，显然不会对答案有影响，这样就是一颗树了。

然后考虑树形 dp，由于操作最多使最大值增加 $q$ 次，所以令 $f_{x, i}$ 表示以 $x$ 为根的子树，最大值 $\leq i + \max_x$ 的概率，其中 $\max_x$ 表示 $[l_x, r_x]$ 中的最大值。

转移有 $f_{x, i} = p_x\prod_{y} f_{x, i + \max_x - \max_y - 1} + (1 - p_x)\prod_{y} f_{x, i + \max_x - \max_y}$。

当 $i = 0$ 时，也即 $x$ 没有操作，故前半部分为 $0$，特判一下。

最后统计答案，$f_{rt, i} - f_{rt, i - 1}$ 即为 $\max = \max_{rt} + i$ 的概率，乘上 $i + \max_{rt}$ 求和就是答案。

建树可以按 $l$ 排序然后直接 $O(q^2)$ 枚举，最大值 ST 表。

```cpp
#include <bits/stdc++.h>
using namespace std;
using d64 = long double;
constexpr int N = 1e5 + 9, M = 5009;
int n, q, a[N], st[20][N], o[M];
int l[M], r[M];
d64 p[M], f[M][M];
vector<int> es[M];
int query(int l, int r) {
  int d = __lg(r - l + 1);
  return max(st[d][l], st[d][r - (1 << d) + 1]);
}
void dfs(int x) {
  f[x][0] = 1 - p[x];
  for (int y : es[x])
    dfs(y), f[x][0] *= f[y][min(q, query(l[x], r[x]) - query(l[y], r[y]))];
  for (int i = 1; i <= q; ++i) {
    d64 p1 = 1, p2 = 1;
    for (int y : es[x]) {
      p1 *= f[y][min(q, i - 1 + query(l[x], r[x]) - query(l[y], r[y]))];
      p2 *= f[y][min(q, i + query(l[x], r[x]) - query(l[y], r[y]))];
    }
    f[x][i] = p[x] * p1 + (1 - p[x]) * p2;
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q;
  for (int i = 1; i <= n; ++i) cin >> a[i], st[0][i] = a[i];
  for (int i = 1; i < 20; ++i)
    for (int j = 1; j + (1 << i) - 1 <= n; ++j) st[i][j] = max(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
  ++q, l[1] = 1, r[1] = n, p[1] = 0;
  for (int i = 2; i <= q; ++i) cin >> l[i] >> r[i] >> p[i];
  iota(o + 1, o + q + 1, 1);
  sort(o + 1, o + q + 1, [&](int x, int y) -> bool { return l[x] == l[y] ? r[x] > r[y] : l[x] < l[y]; });
  for (int i = 1; i <= q; ++i) {
    for (int j = i - 1; j >= 1; --j) {
      if (l[o[j]] <= l[o[i]] && r[o[i]] <= r[o[j]]) {
        es[o[j]].push_back(o[i]);
        break;
      }
    }
  }
  dfs(o[1]);
  d64 ans = f[o[1]][0] * query(1, n);
  for (int i = 1; i <= q; ++i) ans += (f[o[1]][i] - f[o[1]][i - 1]) * (i + query(1, n));
  cout << fixed << setprecision(9) << ans;
}
```

### CF900D
和 CF839D 类似。

考虑枚举 $y$ 的因子 $k$，则 $\sum_{i = 1}^n \dfrac {a_i}k = \dfrac yk, \dfrac {a_i}k \geq 1$。

方案数即为 $\sum_{n = 1}^{\frac yk - 1} \dbinom{\frac yk - 1}{n - 1} = 2^{\frac yk - 1}$。

由于没有保证 $\dfrac {a_i}k$ 互质，所以这其实是 $k \mid \gcd$ 的答案。

于是和 CF839D 一样，倒序枚举，然后把倍数的答案减掉即可。

```
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int md = 1e9 + 7, N = 1e5 + 9;
int qpow(int a, int b) {
  int r = 1;
  for (; b > 0; b >>= 1, a = a * a % md)
    if (b & 1) r = r * a % md;
  return r;
}
int x, y, f[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> x >> y;
  if (y % x != 0) return cout << 0, 0;
  vector<int> fc;
  for (int i = 1; i * i <= y; ++i)
    if (y % i == 0) {
      fc.push_back(i);
      if (i * i != y) fc.push_back(y / i);
    }
  sort(fc.begin(), fc.end(), greater<int>());
  const int sz = fc.size();
  for (int i = 0; i < sz; ++i) {
    f[i] = qpow(2, y / fc[i] - 1);
    for (int j = i - 1; j >= 0; --j) {
      if (fc[j] % fc[i] == 0) (f[i] += md - f[j]) %= md;
    }
    if (fc[i] == x) return cout << f[i], 0;
  }
}
```

----------------

2025.10.11

### CF1633E

*2400

好题！

注意到有绝对值，很麻烦，所以考虑去掉它。

首先，回忆一下 kruskal 求最小生成树的过程，我们只是按边权排序而已，也就是说我们只关心其相对大小而不关心具体数值。

接着考虑去绝对值。

对于 $x$，我们来观察 $|w_i - x|$ 的大小关系。

画图容易发现，$x$ 随着改变，$|w_i - x|$ 是 V 字型，而当任意两个 $i\neq j, |w_i - x| = |w_j - x|$ 时，边权的大小关系会改变，进而 MST 也可能改变。

显然这样的交点只有 $O(m^2)$ 个，故 MST 也只有 $O(m^2)$ 个。

我们可以直接枚举这些点，也就是 $x = \dfrac {w_i - w_j} 2, w_i > w_j$，然后对于每个计算一遍 MST。

注意要把 $|w_i - x|$ 的拐点和 $0$ 也加进去，这样才能完整包含所有可能的 MST。

求出了这 $O(m^2)$ 个关键点之后，对询问排序，每次枚举点 $x_i$，我们算出此时的 MST，然后双指针 $O(1)$ 计算 $q_j \in [x_i, x_{i + 1})$ 的询问。

由于拐点也被视为关键点，故 $[x_i, x_{i + 1})$ 范围内，不会有边的 $w_i - x$ 正负性改变，可以直接拆掉绝对值计算。

总时间复杂度 $O(m^3 \log m + q \log q)$。

可以通过基数排序和双指针去掉 $\log$，但没必要。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 59, M = 309, Q = 1e7 + 9;
int n, m, a, b, c, p, k, q[Q], fa[N], tmp[M * M], len = 1;
struct edge { int u, v, w; } e[M];
int getf(int x) { return x == fa[x] ? x : fa[x] = getf(fa[x]); }
bool mer(int x, int y) {
  if ((x = getf(x)) == (y = getf(y))) return false;
  return fa[x] = y, true;
}
pair<int, int> calc(int x) {
  iota(fa + 1, fa + n + 1, 1);
  sort(e + 1, e + m + 1, [&](auto ls, auto rs) -> bool { return abs(ls.w - x) < abs(rs.w - x); });
  int w = 0, d = 0;
  for (int i = 1; i <= m; ++i)
    if (mer(e[i].u, e[i].v))
      w += abs(e[i].w - x), d += e[i].w <= x ? 1 : -1;
  return {w, d};
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= m; ++i) cin >> e[i].u >> e[i].v >> e[i].w;
  cin >> p >> k >> a >> b >> c;
  for (int i = 1; i <= p; ++i) cin >> q[i];
  for (int i = p + 1; i <= k; ++i) q[i] = (q[i - 1] * a + b) % c; 
  sort(e + 1, e + m + 1, [&](auto x, auto y) -> bool { return x.w < y.w; });
  for (int i = 1; i <= m; ++i) {
    for (int j = i; j <= m; ++j)
      tmp[++len] = (e[i].w + e[j].w) >> 1,
      tmp[++len] = ((e[i].w + e[j].w) >> 1) + 1;
  }
  tmp[++len] = 0x3f3f3f3f;
  sort(tmp + 1, tmp + len + 1);
  len = unique(tmp + 1, tmp + len + 1) - tmp - 1;
  sort(q + 1, q + k + 1);
  int ans = 0;
  for (int j = 0, i = 1; j < k && i < len; ++i) {
    int cur = tmp[i], nxt = tmp[i + 1];
    auto [w, d] = calc(cur);
    while (j < k && q[j + 1] < nxt)
      ans ^= w + (q[++j] - cur) * d;
  }
  cout << ans;
}
```
### CF665E
水题，能有 *2100 ？

求前缀异或和，然后上 01 trie 即可，$O(n \log a)$。
### CF817F
线段树，1、2 操作直接区间覆盖，3 操作区间取反，查询直接线段树二分。

动态开点会 MLE，不懂，似乎只能写离散化。

但是没有卡 ODT，所以写了 ODT。

要卡的话很简单，造 $\dfrac n2$ 次 1、2 交替的，这样会有 $\dfrac n2$ 段，再 $\dfrac n2$ 次 3 就卡掉了。

### CF1375F
神仙构造。

首先要观察到，当 $a, b, c$ 构成等差数列，且最大值不可以修改时，后手必败。

此时，令 $a < b < c$，可以构造 $y = c - b = b - a$。

然后考虑如何构造出等差数列。

首先加一个 $x = \inf$，这样可以得到操作后最大的数。

这个数必然是中位数，因为第三次操作可以操作第一次的位置。

所以第一次的位置必然是 $b$。

那么考虑构造出 $c$，我们再加一个 $3b - a - b - c$，这样的话无论它加给 $a$ 还是 $c$，这个位置都成了最大值 $c$ 。

第三次，直接构造 $y = c - b$，由于上一回操作的是最大值，所以后手必败。
### CF432D
前缀等于后缀直接用 kmp 算。

考虑出现次数。

令 $f_i$ 表示前缀 $s_{1,\dots, i}$ 出现的次数。

转移直接 $f_i \to f_{nxt_i}$，倒序枚举 $i$。

因为假设前缀 $s_i$ 在 $s_{j, \dots, j + i - 1}$ 再次出现，那么 $nxt_{j + i - 1} = i$ 所以会被统计到。

然后就做完了。

笑点解析：用 AC 自动机统计次数，会推出次数即为 fail 树上的子树大小，也就是上面的东西。
### CF797E
小唐题。

容易发现答案有一个很松的上界 $\dfrac nk$。

于是可以根号分治，$k \leq S$ 时直接预处理每个 $k, p$ 的答案，$k > S$ 时，直接暴力。

时间复杂度 $O(n\sqrt n)$，跑得飞快。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1e5 + 9, S = 316;
int n, a[N], q, ans[N / S + 9][N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int k = 1; k <= n / S; ++k) {
    for (int i = n; i >= 1; --i) {
      if (i + a[i] + k > n) ans[k][i] = 1;
      else ans[k][i] = ans[k][i + a[i] + k] + 1;
    }
  }
  cin >> q;
  while (q--) {
    int p, k;
    cin >> p >> k;
    if (k > n / S) {
      int res = 0;
      while (p <= n) ++res, p = p + a[p] + k;
      cout << res << '\n';
    }
    else cout << ans[k][p] << '\n';
  }
}
```

---------

2025.10.12

### CF566D
写点水题

1, 3 并查集，2 用链表维护相同的段，做完了。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 2e5 + 9;
int n, m, fa[N], nxt[N];
int getf(int x) { return x == fa[x] ? x : fa[x] = getf(fa[x]); }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m;
  for (int i = 1; i <= n; ++i) fa[i] = i, nxt[i] = i + 1;
  nxt[n + 1] = n + 1;
  while (m--) {
    int o, x, y;
    cin >> o >> x >> y;
    if (o == 1) {
      fa[getf(x)] = getf(y);
    }
    else if (o == 2) {
      for (int i = x; i <= y; i = exchange(nxt[i], nxt[y])) {
        fa[getf(i)] = getf(x);
      }
    }
    else cout << (getf(x) == getf(y) ? "YES\n" : "NO\n");
  }
}
```

-------

2025.10.13
### CF1634F
*2700？

感觉很厉害。

首先区间加斐波那契数列显然是不能直接做的。

观察到 $f_i = f_{i - 1} + f_{i - 2}$，所以我们考虑这样差分：$d_i = a_i - a_{i - 1} - a_{i - 2}$。

容易发现 $f$ 差分后全为 $0$。

现在考虑操作对差分数组的影响，手玩一下会发现 $d_l + 1, d_{r + 1} - f_{r - l + 2}, d_{r + 2} - f_{r - l + 1}$，于是每次直接维护这几个位置即可。

让后考虑相等，对 $a, b$ 一起差分，然后原数组相等等价于差分数组相等，存一下不等的位置数量，每次操作更新以下即可。

也可以令 $a_i \leftarrow a_i - b_i$，然后变成令 $a_i = 0$，这等价于差分数组 $d_i = 0$，直接维护即可。

$O(n)$，居然只开了 $3\times 10^5$。

写的时候没想到做差，所以操作写了两遍。
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 3e5 + 9;
int n, q, md, a[N], b[N], fib[N], diff;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> q >> md;
  fib[1] = fib[2] = 1;
  for (int i = 3; i <= n + 2; ++i) fib[i] = (fib[i - 1] + fib[i - 2]) % md;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i <= n; ++i) cin >> b[i];
  for (int i = n; i; --i)
    a[i] = (a[i] - a[i - 1] - (i > 2 ? a[i - 2] : 0) + 2 * md) % md,
    b[i] = (b[i] - b[i - 1] - (i > 2 ? b[i - 2] : 0) + 2 * md) % md;
  for (int i = 1; i <= n; ++i)
    if (a[i] != b[i]) ++diff;
  while (q--) {
    int l, r;
    char c;
    cin >> c >> l >> r;
    if (c == 'A') {
      int al = (a[l] + 1) % md;
      if (a[l] == b[l] && al != b[l]) ++diff;
      else if (a[l] != b[l] && al == b[l]) --diff;
      a[l] = al;
      if (r < n) {
        int ar = (a[r + 1] - fib[r - l + 2] + md) % md;
        if (a[r + 1] == b[r + 1] && ar != b[r + 1]) ++diff;
        else if (a[r + 1] != b[r + 1] && ar == b[r + 1]) --diff;
        a[r + 1] = ar;
      }
      if (r + 1 < n) {
        int ar = (a[r + 2] - fib[r - l + 1] + md) % md;
        if (a[r + 2] == b[r + 2] && ar != b[r + 2]) ++diff;
        else if (a[r + 2] != b[r + 2] && ar == b[r + 2]) --diff;
        a[r + 2] = ar;
      }
    }
    else {
      int bl = (b[l] + 1) % md;
      if (b[l] == a[l] && bl != a[l]) ++diff;
      else if (b[l] != a[l] && bl == a[l]) --diff;
      b[l] = bl;
      if (r < n) {
        int br = (b[r + 1] - fib[r - l + 2] + md) % md;
        if (b[r + 1] == a[r + 1] && br != a[r + 1]) ++diff;
        else if (b[r + 1] != a[r + 1] && br == a[r + 1]) --diff;
        b[r + 1] = br;
      }
      if (r + 1 < n) {
        int br = (b[r + 2] - fib[r - l + 1] + md) % md;
        if (b[r + 2] == a[r + 2] && br != a[r + 2]) ++diff;
        else if (b[r + 2] != a[r + 2] && br == a[r + 2]) --diff;
        b[r + 2] = br;
      }
    }
    cout << (diff ? "NO\n" : "YES\n");
  }
}
```

### CF1213F
小唐题。

有 $p, q$ 两个限制，不好同时处理，考虑去掉一个。

令 $t_i = s_{p_i}$，$p$ 的限制等价于 $t_i \leq t_{i + 1}$，这是容易做的。

然后，我们可以把 $q$ 的限制同样转化到 $t$ 上面。

假设限制为 $t_{q^{'}_i} \leq t_{q^{'}_{i + 1}}$，那么若 $q^{'}_i < q^{'}_{i + 1}$，显然满足。否则，可以得到 $t_{q^{'}_{i + 1} = \dots = t_{q^{'}_i}}$。

那么问题就变成了区间合并，直接用并查集维护每个位置所在的集合，一个集合的父亲用最右侧的点表示。

这样每次合并 $l, r$，可以通过不断地跳 $l$ 来完成。

只有合并，所以是 $O(n \log n)$，$\log $ 是并查集的。

合并完之后，先判断连续段数量是否 $ > k$，然后每个段依次染色即可，由于限制是 $\le$，所以段数太多可以染一个色。

代码很短很好写。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 2e5 + 9;
int n, k, p[N], q[N], ip[N], fa[N], col[N];
int getf(int x) { return x == fa[x] ? x : fa[x] = getf(fa[x]); }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> k;
  for (int i = 1; i <= n; ++i) cin >> p[i], ip[p[i]] = i;
  for (int i = 1; i <= n; ++i) cin >> q[i], q[i] = ip[q[i]];
  for (int i = 1; i <= n; ++i) fa[i] = i;
  for (int i = 1; i < n; ++i) {
    int l = q[i], r = q[i + 1];
    if (l < r) continue;
    swap(l, r);
    while (getf(l) < r) {
      int f = getf(l);
      l = f;
      fa[f] = f + 1;
    }
  }
  // for (int i = 1; i <= n; ++i) cerr << getf(i) << ' ';
  int cnt = 0;
  for (int i = 1; i <= n; ++i)
    if (getf(i) == i) ++cnt;
  if (cnt < k) cout << "NO";
  else {
    cout << "YES\n";
    int tt = 0;
    for (int i = 2; i <= n; ++i) {
      if (getf(i) == getf(i - 1)) col[i] = col[i - 1];
      else col[i] = min(k - 1, ++tt);
    }
    string s(n, 's');
    for (int i = 1; i <= n; ++i) s[p[i] - 1] = char('a' + col[i]);
    cout << s;
  }
}
```
### CF1204D2
神秘结论题。

不会证明，大概是令 ```1``` 为 ```(```，```0``` 为 ```)```，然后把括号串删去，剩下的直接全部赋为 ```0```。

证明还是看题解吧，[link1](https://www.luogu.com.cn/article/6zfuvr1p) [link2](https://www.luogu.com.cn/article/oszgcmlo)。
### CF1176F
样例用脚都能过。

考虑 dp，$f_{i, j}$ 表示第 $i$ 轮，已经打了 $j$ 张牌。

由于只关心 $j \bmod 10$，所以状态是 $O(n)$ 的。

转移考虑分类讨论，按照本轮打出的牌数分类。

0. 打了 $0$ 张，$f_{i, j} = f_{i - 1, j}$。
1. 打了 $1$ 张，此时若 $j = 0$，则本次打出的牌中有一张伤害翻倍，显然是让伤害最高的。
2. 打了 $2$ 张，此时若 $j = 0, 1$ 可以翻倍。由于每轮出牌的 $\sum c_i \le 3$，所以可以直接分讨转移。
3. 打了 $3$ 张，此时若 $j = 0, 1, 2$ 可以，只能打 $3$ 张 $c_i = 1$ 的。

转移有些细节，但是思路很简单。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 2e5 + 9;
template<class T> void cmax(T &x, T y) { if (x < y) x = y; }
int n, f[N][10];
vector<int> g[4];
int cost(int x, int y, int z, int c) {
  return x + y + z + max({x, y, z}) * c;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  memset(f, -0x3f, sizeof f);
  f[0][0] = 0;
  for (int i = 1, k; i <= n; ++i) {
    cin >> k;
    for (int j = 0; j < 4; ++j) g[j].clear();
    for (int j = 1; j <= k; ++j) {
      int c, d;
      cin >> c >> d;
      g[c].push_back(d);
    }
    for (int j = 0; j < 4; ++j) sort(g[j].begin(), g[j].end(), greater<int>());
    for (int j = 0; j < 10; ++j) {
      { // 0
        cmax(f[i][j], f[i - 1][j]);
      }
      { // 1
        int coef = j <= 0 ? 1 : 0;
        if (!g[1].empty()) cmax(f[i][j], f[i - 1][(j + 9) % 10] + cost(g[1][0], 0, 0, coef));
        if (!g[2].empty()) cmax(f[i][j], f[i - 1][(j + 9) % 10] + cost(g[2][0], 0, 0, coef));
        if (!g[3].empty()) cmax(f[i][j], f[i - 1][(j + 9) % 10] + cost(g[3][0], 0, 0, coef));
      }
      { // 2
        int coef = j <= 1 ? 1 : 0;
        if (g[1].size() > 1) cmax(f[i][j], f[i - 1][(j + 8) % 10] + cost(g[1][0], g[1][1], 0, coef));
        if (!g[1].empty() && !g[2].empty()) cmax(f[i][j], f[i - 1][(j + 8) % 10] + cost(g[1][0], g[2][0], 0, coef));
      }
      { // 3
        int coef = j <= 2 ? 1 : 0;
        if (g[1].size() > 2) cmax(f[i][j], f[i - 1][(j + 7) % 10] + cost(g[1][0], g[1][1], g[1][2], coef));
      }
    }
  }
  cout << *max_element(f[n], f[n] + 10);
}
```
### CF1151E
小唐题，不懂出题人为什么要说这是一颗树，链你就说链啊！！！！

首先考虑把连通块转化一下，连通块个数等于点数减边数。

考虑算点数，一个点 $i$ 被算进答案中，当且仅当 $l\le a_i \le r$，贡献为 $a_i(n - a_i + 1)$。

考虑算边数，一条边 $i \to i + 1$ 被算进答案中，当且仅当 $i, i + 1$ 均存在，贡献即为 $\min(a_i, a_{i + 1})(n - \max(a_i, a_{i + 1}) + 1)$。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 1e5 + 9;
int n, a[N], ans;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i];
  for (int i = 1; i <= n; ++i)
    ans += a[i] * (n - a[i] + 1) - min(a[i], a[i - 1]) * (n - max(a[i], a[i - 1]) + 1);
  cout << ans;
}
```

### CF2065H
拆贡献，每对 $i, j, s_i \neq s_j$ 会有一的贡献，总答案是 $2^n - 1 + \sum_{i = 1}^n\sum_{j = i + 1}^n [s_i \neq s_j] \cdot 2^{i - 1 + n - j}$。

考虑修改一个位置 $p$，会产生的贡献 $g(p) = 2^{p - 1}\sum_{i = p + 1}^n [s_i \neq s_{p}]\cdot 2^{n - i} + 2^{n - p} \sum_{i = 1}^{p - 1} [s_i \neq s_p]\cdot 2^{i - 1}$。

用树状数组维护即可。

写的不太好。有空再改改。

$O(n \log n)$。
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 2e5 + 9, md = 998244353;
int n, q, a[N], pw[N];
string s;
struct fenwick {
  int c1[N], c2[N], tg, u1[N], u2[N];
  void clear() { ++tg; }
  void update1(int x, int y) {
    for (; x <= n; x += x & -x) u1[x] != tg && (u1[x] = tg, c1[x] = 0), (c1[x] += y) %= md;
  }
  int query1(int x, int r = 0) {
    for (; x > 0; x -= x & -x) u1[x] != tg && (u1[x] = tg, c1[x] = 0), (r += c1[x]) %= md;
    return r;
  }
  void update2(int x, int y) {
    for (; x > 0; x -= x & -x) u2[x] != tg && (u2[x] = tg, c2[x] = 0), (c2[x] += y) %= md;
  }
  int query2(int x, int r = 0) {
    for (x = max(x, 1ll); x <= n; x += x & -x) u2[x] != tg && (u2[x] = tg, c2[x] = 0), (r += c2[x]) %= md;
    return r;
  }
} p0, p1;
int g(int x) {
  int res = 0;
  if (a[x] == 0) (res += pw[x - 1] * p1.query2(x + 1)) %= md;
  else (res += pw[x - 1] * p0.query2(x + 1)) %= md;
  if (a[x] == 0) (res += pw[n - x] * p1.query1(x - 1)) %= md;
  else (res += pw[n - x] * p0.query1(x - 1)) %= md;
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  for (int i = pw[0] = 1; i < N; ++i) pw[i] = pw[i - 1] * 2 % md;
  while (tt--) {
    cin >> s >> q;
    n = s.size(), s = ' ' + s;
    for (int i = 1; i <= n; ++i) a[i] = s[i] - '0';
    p0.clear(), p1.clear();
    for (int i = 1; i <= n; ++i) {
      if (a[i] == 0) p0.update1(i, pw[i - 1]), p0.update2(i, pw[n - i]);
      else p1.update1(i, pw[i - 1]), p1.update2(i, pw[n - i]);
    }
    int ans = (pw[n] - 1 + md) % md;
    for (int i = 1; i <= n; ++i) {
      if (a[i] == 0) (ans += pw[i - 1] * p1.query2(i)) %= md;
      else (ans += pw[i - 1] * p0.query2(i)) %= md;
    }
    // cerr << ans << '\n';
    for (int i = 1, x; i <= q; ++i) {
      cin >> x;
      // cerr << g(x) << '\n';
      (ans += md - g(x)) %= md;
      if (a[x] == 0) p0.update1(x, md - pw[x - 1]), p0.update2(x, md - pw[n - x]);
      else p1.update1(x, md - pw[x - 1]), p1.update2(x, md - pw[n - x]);
      a[x] ^= 1;
      if (a[x] == 0) p0.update1(x, pw[x - 1]), p0.update2(x, pw[n - x]);
      else p1.update1(x, pw[x - 1]), p1.update2(x, pw[n - x]);
      (ans += g(x)) %= md;
      cout << ans << ' ';
    }
    cout << '\n';
  }
}
```
---------
2025.10.14
### CF1203F1
贪心，显然优先把 $b_i \ge 0$ 的做了，直接按 $a_i$ 升序排就可以了。

然后是 $b_i < 0$ 的，设当前 rating 是 $x$，那么 $i$ 比 $j$ 先做等价于 $x + b_i \ge a_j, x + b_j < a_i$，也就是 $a_i + b_i > a_j + b_j$。

然后直接排序就做完了。
```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 109;
int n, r, a[N], b[N], o[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> r;
  for (int i = 1; i <= n; ++i) cin >> a[i] >> b[i], o[i] = i;
  sort(o + 1, o + n + 1, [&](int x, int y) -> bool {
    if (b[x] >= 0 && b[y] >= 0) return a[x] < a[y];
    if (b[x] < 0 && b[y] < 0) return a[x] + b[x] > a[y] + b[y];
    return b[x] > b[y];
  });
  for (int i = 1; i <= n; ++i) {
    if (r < a[o[i]]) return cout << "NO", 0;
    r += b[o[i]];
  }
  if (r < 0) cout << "NO";
  else cout << "YES";
}
```
### CF1359E
写点组合。

考虑第三个条件，令 $a < b$，思考 $(x \bmod b) \equiv x \pmod a$ 的充要条件。

令 $x = pb + q$（$0 \le q < b$），那么原式 $q \equiv pb + q \pmod a$，由于 $x$ 任意，故 $p$ 任意，所以充要条件为 $a \mid b$。

推广到序列上同理，$\forall 1 \le i \le k, a_1 \mid a_i$。

我们枚举 $1 \le a_i \le n$，由于其余数必然是它的倍数，直接从里面选出 $k - 1$ 个即可。

$O(n)$。
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 5e5 + 9, md = 998244353;
int n, k, fc[N], ifc[N], ans;
int qpow(int a, int b) {
  int r = 1;
  for (; b > 0; b >>= 1, a = a * a % md)
    if (b & 1) r = r * a % md;
  return r;
}
int C(int n, int m) {
  if (n < m) return 0;
  return fc[n] * ifc[n - m] % md * ifc[m] % md;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> k;
  for (int i = fc[0] = 1; i < N; ++i) fc[i] = i * fc[i - 1] % md;
  ifc[N - 1] = qpow(fc[N - 1], md - 2);
  for (int i = N - 2; i >= 0; --i) ifc[i] = (i + 1) * ifc[i + 1] % md;
  for (int i = 1; i <= n; ++i) {
    (ans += C(n / i - 1, k - 1)) %= md;
  }
  cout << ans;
}
```
### CF2119D
考虑转化，把删点变成加点，于是问题变成求将 $n$ 点中的若干的加入 $[l_i, i]$ 中。

$f_{i, j}$ 表示后 $i$ 个点，有 $j$ 个没有选的方案数，转移考虑 $i$ 选不选。

不选的话，$f_{i, j} = f_{i + 1, j - 1}$，多了一个不选的点。

选的话，$f_{i, j} = f_{i + 1, j} \times i \times (j + 1)$，显然这个点被一个区间 $[l, r]$ 包含，$l \le i$ 有 $i$ 种，$r$ 两两不同，所以只能从后 $i$ 个没有选的点中拿，有 $j + 1$ 种（$i$ 这里也有一种）。

倒序的原因是因为所有区间的右端点是固定的，所以枚举到 $i$ 时，可能的区间全在右侧。

$O(n^2)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 5009;
int n, md, f[N][N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n >> md;
    f[n + 1][0] = 1;
    for (int i = 1; i <= n; ++i) f[n + 1][i] = 0;
    for (int i = n; i >= 1; --i) {
      for (int j = 0; j <= n; ++j) {
        f[i][j] = 0;
        if (j > 0) f[i][j] = f[i + 1][j - 1];
        (f[i][j] += f[i + 1][j] * i * (j + 1)) %= md;
      }
    }
    int ans = 0;
    for (int i = 0; i <= n; ++i) (ans += f[1][i]) %= md;
    cout << ans << '\n';
  }
}
```

### CF2061E
由于 $m \le 10$ 显然可以求出每个位置 $i$ 操作 $j$ 次后的最小值。

然后可以直接分组背包，但是显然会炸。

想到这里就不会了。

令 $s_{i, j}$ 表示 $i$ 操作 $j$ 次的最小值，通过观察发现这个东西关于 $j$ 的下降在变缓，也即差分数组 $d_j = s_{i, j} - s_{i, j - 1}$ 单调不减。

证明：考虑 $s_{i, j}$ 与 $s_{i, j - 1}$ 之间不同的最高位 $p$，则 $d_j \le -2^p$。假设 $d_j \ge d_{j + 1}$，则 $d_{j + 1} \le -2^p$，由于 $d_{j + 1} = s_{i, j + 1} - s_{i, j}$，而 $s_{i, j}$ 的 $p$ 位为 $0$，所以 $s_{i, j + 1}$ 和 $s_{i, j}$ 必然有一位 $q > p$ 不同，那么 $s_{i, j}$ 可以选择操作减掉 $q$ 位，此时更优，与 $s_{i, j}$ 最优矛盾，故 $d_j \le d_{j + 1}$。

然后由于单调不升，所以我们对所有 $d_j$ 排序，若选择 $j$，则因为 $d_{j - 1} \le d_{j}$，所以 $1 \sim j - 1$ 都会被选，也就自然的满足了限制。

$O(nm \log {nm} + (n + m)2^m)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
constexpr int N = 1e5 + 9;
int n, m, k, a[N], b[N], da[1 << 10], s[N][12], c[N * 10];
template<class T> void cmin(T& x, T y) { if (x > y) x = y; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n >> m >> k;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int i = 0; i < m; ++i) cin >> b[i];
    for (int i = 0; i < 1 << m; ++i) {
      da[i] = (1 << 30) - 1;
      for (int j = 0; j < m; ++j)
        if (i >> j & 1) da[i] &= b[j];
    }
    for (int i = 1; i <= n; ++i) {
      memset(s[i], 0x3f, sizeof s[i]);
      for (int j = 0; j < 1 << m; ++j) {
        cmin(s[i][__builtin_popcount(j)], a[i] & da[j]);
      }
      for (int j = m; j >= 1; --j)
        c[(i - 1) * m + j] = s[i][j] - s[i][j - 1];
    }
    sort(c + 1, c + n * m + 1);
    int64_t ans = accumulate(a + 1, a + n + 1, 0ll);
    for (int i = 1; i <= k; ++i) ans += c[i];
    cout << ans << '\n';
  }
}
```

### CF2044G2
一开始没看清题，以为是把所有的全部给了，然后倍增发现过不了样例，才知道一次只能给一个。

建图，然后这个东西显然到环就可以了，直接拓扑排序求出每个点把子树清空所花的时间，也就是子树大小即可。

G1 同理。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 2e5 + 9;
int n, dst[N], d[N], nxt[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n;
    for (int i = 1; i <= n; ++i) d[i] = dst[i] = 0;
    for (int i = 1; i <= n; ++i) {
      cin >> nxt[i];
      ++d[nxt[i]];
    }
    queue<int> q;
    for (int i = 1; i <= n; ++i) {
      if (!d[i]) q.push(i);
    }
    int ans = 0;
    while (!q.empty()) {
      int x = q.front();
      q.pop();
      ans = max(ans, ++dst[x]);
      dst[nxt[x]] += dst[x];
      if (!--d[nxt[x]]) q.push(nxt[x]);
    }
    cout << ans + 2 << '\n';
  }
}
```

### CF2062D
显然先把操作转化为子树加和全局加子树减。

考虑对于一棵子树 $i$，如果 $a_i$ 不是最大值，那么一定要子树减，最终 $a_i$ 成为最大值，但是会导致其他部分变大；而 $a_i$ 是最大值，我们可以直接做子树加。

因此，$a_i$ 取其所有儿子的最大值。

我们考虑类似树形 dp，对于 $i$，我们要使其满足条件。

首先 $a_i = \max_{i \to j} a_j$，但是由于 $l_i \le a_i \le r_i$，所以我们限制一下 $a_i$。

此时 $a_i$ 可能不是最大，所以我们要将大于 $a_i$ 的儿子，全部通过子树减变成相同。

我们令 $f_i$ 表示 $i$ 子树全局加子树减的次数，$f_i = \sum_{i \to j} f_j$。

然后，对于 $i\to j, a_i < a_j$，$f_i \leftarrow f_i + a_j - a_i$，也就是加上这次的操作。

最后答案即为 $a_1 + f_1$，这里假定 $1$ 为根。

$O(n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e5 + 9;
int n, a[N], l[N], r[N], f[N];
vector<int> es[N];
void dfs(int x, int ff) {
  f[x] = a[x] = 0;
  for (int y : es[x])
    if (y ^ ff) dfs(y, x), cmax(a[x], a[y]), f[x] += f[y];
  cmax(a[x], l[x]), cmin(a[x], r[x]);
  for (int y : es[x])
    if ((y ^ ff) && a[x] < a[y]) f[x] += a[y] - a[x];
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n;
    for (int i = 1; i <= n; ++i) es[i].clear();
    for (int i = 1; i <= n; ++i) cin >> l[i] >> r[i];
    for (int i = 1; i < n; ++i) {
      int x, y;
      cin >> x >> y;
      es[x].push_back(y), es[y].push_back(x);
    }
    dfs(1, 0);
    cout << a[1] + f[1] << '\n';
  }
}
```

### CF2037G
$f_i$ 表示 $1$ 到 $i$ 的方案数，显然 $f_i = \sum_{j = 1}^{i - 1}[\gcd(a_i, a_j) \neq 1] f_j$。

转化一下。

$$
f_i = \sum_{j = 1}^{i - 1}[\gcd(a_i, a_j) \neq 1] f_j
\\
f_i = \sum_{j = 1}^{i - 1}f_j - \sum_{j = 1}^{i - 1}[\gcd(a_i, a_j) = 1] f_j
\\
f_i = \sum_{j = 1}^{i - 1}f_j - \sum_{j = 1}^{i - 1}f_j\sum_{d \mid a_i, d \mid a_j} \mu(d)
\\
f_i = \sum_{j = 1}^{i - 1}f_j - \sum_{d \mid a_i}\mu(d) \sum_{j = 1}^{i - 1}[d\mid a_j]f_j
$$

令 $g_d = \sum_{j = 1}^{i - 1}[d \mid a_j] f_j$，每次可以 $O(\sqrt V)$ 修改查询。

$O(n\sqrt V)$。

实现的时候可以不记 $\sum_{j = 1}^{i - 1} f_j$，因为所有数都有 $1$ 这个因子，所以就是 $g_1$，由于 $\mu(1) = 1$，所以会被减掉，把这一部分去掉就行了。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 2e5 + 9, V = 1e6 + 9, md = 998244353;
int n, a[N], mu[V], pri[N], ct, f[N], g[V];
bool vis[V];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  mu[1] = 1;
  for (int i = 2; i < V; ++i) {
    if (!vis[i]) pri[++ct] = i, mu[i] = -1;
    for (int j = 1; j <= ct && i * pri[j] < V; ++j) {
      vis[i * pri[j]] = 1;
      if (i % pri[j] == 0) break;
      mu[i * pri[j]] = -mu[i];
    }
  }
  for (int i = f[1] = 1; i <= n; ++i) {
    cin >> a[i];
    vector<int> fct;
    for (int d = 1; d * d <= a[i]; ++d) {
      if (a[i] % d == 0) {
        fct.push_back(d);
        if (d * d != a[i]) fct.push_back(a[i] / d);
      }
    }
    for (int d : fct)
      if (d > 1) (f[i] += md - mu[d] * g[d]) %= md;  // 保留 g[1]
    for (int d : fct) (g[d] += f[i]) %= md;
  }
  cout << f[n];
}
```
### CF2027D2

感觉很牛。

dp 很简单，设 $f_{i, j}$ 表示 $k = i$ 时，删掉前 $j$ 个的最小代价。

转移直接枚举 $l, \sum_{j = l + 1}^i a_l \le b_k$，$f_{i, j} = \min f_{i, l} + m - i$。

显然 $f_i$ 单调不降，所以可以双指针找最小的 $l$，复杂度 $O(nm)$。

考虑计算方案，此时 $f_{i, j}$ 可以从 $p, f_{i, p} = f_{i, l}$ 转移过来，由于 $f_i$ 有单调性，所以同样可以双指针求出 $p$，前缀和一下即可。

$O(nm)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 3e5 + 9, md = 1e9 + 7;
int a[N], b[N], n, m, f[N], g[N], pr[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n >> m;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int i = 1; i <= m; ++i) cin >> b[i];
    for (int i = 1; i <= n; ++i) a[i] += a[i - 1], pr[i] = g[i] = 0, f[i] = 0x3f3f3f3f3f3f3f3f;
    f[0] = 0, g[0] = pr[0] = 1;
    for (int k = 1; k <= m; ++k)
      for (int i = 1, j = 1, p = 0; j <= n; ++j) {
        while (i <= j && a[j] - a[i - 1] > b[k]) ++i;
        if (i <= j) {
          cmax(p, i - 1);
          while (p + 1 < j && f[p + 1] == f[i - 1]) ++p;
          if (f[j] > f[i - 1] + m - k) {
            f[j] = f[i - 1] + m - k;
            g[j] = (pr[p] - (i - 1 > 0 ? pr[i - 2] : 0) + md) % md;
          }
          else if (f[j] == f[i - 1] + m - k) (g[j] += pr[p] - (i - 1 > 0 ? pr[i - 2] : 0) + md) %= md;
        }
        pr[j] = (pr[j - 1] + g[j]) % md;
      }
    if (f[n] == 0x3f3f3f3f3f3f3f3f) cout << -1 << '\n';
    else cout << f[n] << ' ' << g[n] << '\n';
  }
}
```

### CF2020E
注意到 $a_i < 2^{10}$，所以 $f(S) < 2^{10}$。

我们可以算出每种 $f(S)$ 的出现概率，由于分母都是 $10000$，所以我们最后再除掉。

考虑 dp，$f_{i, j}$ 表示前 $i$ 个数，异或和为 $j$，$f_{i, j} = (10000 - p_i) f_{i - 1, j} + p_i f_{i - 1, j \oplus a_i}$。

$i$ 可以滚动掉。

$O(na)$

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 2e5 + 9, md = 1e9 + 7;
int n, a[N], p[N], f[1 << 10], g[1 << 10];
int qpow(int a, int b) {
  int r = 1;
  for (; b > 0; b >>= 1, a = a * a % md)
    if (b & 1) r = r * a % md;
  return r;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int i = 1; i <= n; ++i) cin >> p[i];
    memset(g, 0, sizeof g);
    g[0] = 1;
    for (int i = 1; i <= n; ++i) {
      memset(f, 0, sizeof f);
      for (int j = 0; j < 1 << 10; ++j) {
        f[j] = ((10000 - p[i]) * g[j] + g[j ^ a[i]] * p[i]) % md;
      }
      memcpy(g, f, sizeof f);
    }
    int ans = 0;
    for (int i = 0; i < 1 << 10; ++i) {
      (ans += f[i] * i * i) %= md;
    }
    (ans *= qpow(qpow(10000, n), md - 2)) %= md;
    cout << ans << '\n';
  }
}
```

### CF1942D
考虑每个位置 $i$ 存 $1 \sim i$ 的子序列前 $k$ 大的值，然后每次把 $1\sim i - 1$ 的最大值取掉，用堆维护每个位置的答案，然后直接弹掉最大的，最后还原一下即可。

$O(nk\log k)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1009;
int n, k, a[N][N];
priority_queue<int> f[N];
queue<pair<int, int>> Q;
int get(int x) {
  int t = f[x].top();
  return Q.push({x, t}), f[x].pop(), t;
}
void remake() {
  while (!Q.empty()) {
    auto [x, y] = Q.front();
    f[x].push(y);
    Q.pop();
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n >> k;
    for (int i = 1; i <= n; ++i)
      for (int j = i; j <= n; ++j) cin >> a[i][j];
    for (int i = 0; i <= n; ++i) {
      while (!f[i].empty()) f[i].pop();
    }
    f[0].push(0);
    for (int i = 1; i <= n; ++i) {
      priority_queue<pair<int, int>> q;
      q.emplace(a[1][i], -1);
      for (int j = 0; j < i; ++j) {
        q.emplace(a[j + 2][i] + get(j), j);
      }
      while (!q.empty() && f[i].size() < k) {
        auto [x, y] = q.top();
        q.pop();
        f[i].emplace(x);
        if (y == -1) continue;
        if (!f[y].empty()) q.emplace(a[y + 2][i] + get(y), y);
      }
      remake();
    }
    while (!f[n].empty()) {
      cout << f[n].top() << ' ';
      f[n].pop();
    }
    cout << '\n';
  }
}
```

### CF1988D
相当于给所有点赋上一个值 $t_i$，要求树上相邻点的权值不同，最小化 $\sum_i t_i a_i$。

显然由于要最小化，所以我们的 $t_i$ 必然是其所有儿子的 $\text{mex}(t_s)$（这里从 $1$ 开始，不考虑 $0$），同时所有叶子节点都从 $1$ 开始。

那么考虑 $\max t_i$ 是多少，令 $f(n)$ 表示 $\max t = n$ 的树所需要的最小点数，$f(n) = 1 + \sum_{i = 1}^{n - 1} f(i) = 2^{n - 1}$，那么 $\max t \le \log_2 n + 1$。

写了 $O(n\log^2 n)$ 的暴力 dp，不想优化了。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 3e5 + 9;
int n, a[N], f[N][30];
vector<int> es[N];
void dfs(int x, int ff) {
  for (int y : es[x]) {
    if (y ^ ff) dfs(y, x);
  }
  for (int i = 1; i < 30; ++i) {
    f[x][i] = a[x] * i;
    for (int y : es[x]) {
      if (y ^ ff) {
        int mn = 0x7f7f7f7f7f7f7f7f;
        for (int j = 1; j < 30; ++j) {
          if (j ^ i) cmin(mn, f[y][j]);
        }
        f[x][i] += mn;
      }
    }
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int tt;
  cin >> tt;
  while (tt--) {
    cin >> n;
    for (int i = 1; i <= n; ++i)
      cin >> a[i], memset(f[i], 0x3f, sizeof f[i]), es[i].clear();
    for (int i = 1, x, y; i < n; ++i) {
      cin >> x >> y;
      es[x].push_back(y), es[y].push_back(x);
    }
    dfs(1, 0);
    cout << *min_element(f[1], f[1] + 30) << '\n';
  }
}
```
### P9754 
晚上和同学写大模拟。

对于每个结构体，开一个结构体存：大小，对齐要求，所有成员的名称和类型，成员的地址偏移量。

每个元素开一个结构体存：起始位置，名称和类型。

然后再开一个 vector 存所有元素，两个 map 存每个类型和元素对应的结构体。

然后操作还好，一个个写，4 操作要特判一些东西，不过还好。

大样例有点水，过了还被卡成了 65。

脑抽了，快写完发现其实不用把元素和结构体分开存，可以直接开一个全局结构体把所有元素放里面。

时间复杂度懒得算了，能过。

写了 1.5 h，调试过程还挺简单。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
struct Type {
  vector<pair<string, string>> mber; // type, name
  vector<int> o;
  int a, s; // rule, size
};
struct Var {
  string name, type;
  int be;
};
int up(int x, int y) { return (x + y - 1) / y * y; }
map<string, Type> type;
map<string, Var> var;
vector<Var> pool;
void op1() {
  string s;
  Type now;
  cin >> s;
  int k;
  cin >> k;
  for (int i = 0; i < k; ++i) {
    string t, n;
    cin >> t >> n;
    now.mber.emplace_back(t, n);
  }
  now.o.resize(k);
  now.a = type[now.mber.front().first].a, now.s = 0;
  for (int i = 1; i < k; ++i) {
    auto &nw = type[now.mber[i].first];
    now.o[i] = up(now.o[i - 1] + type[now.mber[i - 1].first].s, nw.a);
    cmax(now.a, nw.a);
  }
  now.s = up(now.o.back() + type[now.mber.back().first].s, now.a);
  type[s] = now;
  cout << now.s << ' ' << now.a << '\n';
}
void op2() {
  string t, n;
  cin >> t >> n;
  Var now;
  if (pool.empty()) now.be = 0;
  else now.be = up(pool.back().be + type[pool.back().type].s, type[t].a);
  now.name = n, now.type = t;
  pool.push_back(now), var[n] = now;
  cout << now.be << '\n';
}
vector<string> split(string s) {
  vector<string> vec;
  vec.push_back("");
  for (auto i : s) {
    if (isalpha(i)) vec.back().push_back(i);
    else vec.push_back("");
  }
  return vec;
}
void op3() {
  string s;
  cin >> s;
  auto path = split(s);
  int cur = var[path[0]].be;
  string typ = var[path[0]].type;
  const size_t psz = path.size();
  for (size_t i = 1; i < psz; ++i) {
    string n = path[i];
    bool found = false;
    for (size_t j = 0; j < type[typ].mber.size(); ++j) {
      auto [x, y] = type[typ].mber[j];
      if (y == n) {
        found = true;
        cur += type[typ].o[j];
        typ = x;
        break;
      }
    }
    if (found == false) {
      cout << "ERR\n";
      return ;
    }
  }
  cout << cur << '\n';
}
void op4() {
  int addr;
  cin >> addr;
  string s;
  int cur = 0;
  vector<string> ans;
  for (size_t i = 0; i < pool.size(); ++i) {
    if (pool[i].be <= addr && pool[i].be + type[pool[i].type].s > addr) {
      cur = pool[i].be, s = pool[i].type;
      ans = {pool[i].name};
      if (type[pool[i].type].mber.empty()) {
        cout << pool[i].name << '\n';
        return ;
      }
      break;
    }
  }
  if (ans.empty()) {
    cout << "ERR\n";
    return ;
  }
  addr -= cur;
  bool got = false;
  while (!got) {
    bool found = false;
    for (size_t i = 0; i < type[s].mber.size(); ++i) {
      auto [x, y] = type[s].mber[i];
      if (type[s].o[i] <= addr && type[s].o[i] + type[x].s > addr) {
        addr -= type[s].o[i];
        ans.push_back(y), s = x;
        found = true;
        if (type[s].mber.empty()) got = true;
        break;
      }
    }
    if (found == false) {
      cout << "ERR\n";
      return ;
    }
  }
  cout << ans[0];
  for (size_t i = 1; i < ans.size(); ++i) cout << "." << ans[i];
  cout << '\n';
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  type["byte"] = {{}, {}, 1, 1}, type["short"] = {{}, {}, 2, 2};
  type["int"] = {{}, {}, 4, 4}, type["long"] = {{}, {}, 8, 8};
  int q;
  cin >> q;
  while (q--) {
    int op;
    cin >> op;
    if (op == 1) op1();
    else if (op == 2) op2();
    else if (op == 3) op3();
    else op4();
  }
}
```

------
2025.10.15
### CF369E
考虑正难则反，我们算没有包含任何一个点的区间个数。

显然这些区间必然是夹在相邻的两个点之间的，所以我们把相邻点的区间求出来，问题就变成了求被包含的区间数量，离线下来扫描线即可。

$O(n\log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 3e5 + 9;
int n, m, ans[N], cnt, c[4 * N];
vector<pair<int, int>> vec[N * 4];
void update(int x, int y) { for (; x > 0; x -= x & -x) c[x] += y; }
int query(int x, int r = 0) { for (; x < 4 * N; x += x & -x) r += c[x]; return r; }
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m; cnt = n;
  for (int i = 1; i <= n; ++i) {
    int l, r;
    cin >> l >> r;
    vec[r].emplace_back(l, 0);
  }
  for (int i = 1; i <= m; ++i) {
    int k, lst = 0;
    cin >> k;
    for (int j = 1; j <= k; ++j) {
      int p;
      cin >> p;
      if (lst + 1 <= p - 1) {
        vec[p - 1].emplace_back(lst + 1, i);
        // cerr << lst + 1 << ' ' << p - 1 << '\n';
      }
      lst = p;
    }
    vec[4 * N - 1].emplace_back(lst + 1, i);
    // cerr << lst + 1 << ' ' << 4 * N - 1 << '\n';
    // cerr << '\n';
  }
  for (int i = 1; i < N * 4; ++i) {
    for (auto [x, y] : vec[i]) {
      if (y == 0) update(x, 1);
      else ans[y] += query(x);
    }
  }
  for (int i = 1; i <= m; ++i) cout << n - ans[i] << '\n';
}
```

### CF546D
显然操作次数等于质因子个数，由于 $a \leq 5\times 10^6$，所以质因子个数不超过 $30$，预处理一下每个数的最小质因子，暴力分解质因数即可。

$O(n \log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 5e6 + 9;
int cnt[N], pre[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  for (int i = N - 1; i >= 2; --i) {
    for (int j = i; j < N; j += i) pre[j] = i;
  }
  for (int i = 2; i < N; ++i) {
    int x = i;
    while (x > 1) x /= pre[x], ++cnt[i];
    cnt[i] += cnt[i - 1];
  }
  int tt;
  cin >> tt;
  while (tt--) {
    int a, b;
    cin >> a >> b;
    cout << cnt[a] - cnt[b] << '\n';
  }
}
```

### CF156D
并查集，先把线索并起来，然后成了 $cnt$ 个连通块。

显然，最小连边就是变成树，$T = cnt - 1$。

然后根据 prufer 序列，连成树的方案是 $n^{cnt - 2}$。

但是每次连边，我们不知道具体连的是连通块中的哪个点，所以还要乘上连通块大小 $s_i$。

$O(n \log n)$，没写按秩合并。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
constexpr int N = 1e5 + 9;
int n, m, k, fa[N], sz[N];
int getf(int x) { return x == fa[x] ? x : fa[x] = getf(fa[x]); }
void mer(int x, int y) {
  if ((x = getf(x)) == (y = getf(y))) return ;
  sz[x] += sz[y];
  fa[y] = x;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> k;
  for (int i = 1; i <= n; ++i) fa[i] = i, sz[i] = 1;
  for (int x, y, i = 1; i <= m; ++i) {
    cin >> x >> y;
    mer(x, y);  
  }
  int res = 1, cnt = 0;
  for (int i = 1; i <= n; ++i)
    if (fa[i] == i) ++cnt, (res *= sz[i]) %= k;
  if (cnt == 1) cout << 1 % k;
  else {
    for (int i = cnt - 2; i >= 1; --i)
      (res *= n) %= k;
    cout << res;
  }
}
```

### P1272
写不动 CF 了。

显然是树形背包，$f_{i, j}$ 表示强制选 $i$，选了 $j$ 个点的最小代价。

初始时 $f_{x, 1} = 0$，转移类似背包，$f_{i, j} = \min_{k, s} f_{i, j - s} + f_{k, s}$，由于每次新加一个儿子 $k$ 进来时，我们可以不选，代价是断掉 $i \to k$ 这条边，所以 $f_{i, j} \leftarrow f_{i , j} + 1$。

$O(np)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 159;
int n, p, f[N][N], g[N], h[N], sz[N];
vector<int> es[N];
void dfs(int x, int ff) {
  sz[x] = 1, f[x][1] = 0;
  for (int y : es[x]) {
    if (y == ff) continue;
    dfs(y, x);
    memcpy(g, f[x], sizeof g);
    sz[x] += sz[y];
    for (int i = 1; i <= p && i <= sz[x]; ++i) {
      ++f[x][i];
      for (int j = 1; j <= min(sz[y], i - 1); ++j)
        cmin(f[x][i], g[i - j] + f[y][j]);
    }
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> p;
  for (int i = 1, x, y; i < n; ++i)
    cin >> x >> y, es[x].push_back(y), es[y].push_back(x);
  memset(f, 0x3f, sizeof f);
  dfs(1, 0);
  int ans = f[1][p];
  for (int i = 2; i <= n; ++i) cmin(ans, f[i][p] + 1);
  cout << ans;
}
```

### P2607
把每个人和其讨厌的人建边，形成一颗基环树。

问题就是求基环树上最大独立集。

基环树显然先找环，然后以环上点为根跑树上最大独立集，求出每个点选/不选的最大价值，然后考虑环。

如果不是环是序列那么是简单的，但是这里我们要求首位不同。

由于 dp 我们不能保证这点，所以直接暴力钦定第一个不选，这样就没有限制了。

可这样会漏一些情况，于是我们观察一下，把环循环位移一下，继续这样统计。那么如果第一个点选更优，我们移动之后这个点是第二个点，它必然会选，所以可以统计到。

$O(n)$，常数比较大。

注意图不一定联通。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e6 + 9;
int n, to[N], a[N], d[N], f[N][2], g[N][2];
bool vis[N];
queue<int> q;
vector<vector<int>> loop;
vector<int> es[N];
void dfs(int x, int ff) {
  f[x][1] = a[x], f[x][0] = 0;
  for (int y : es[x]) {
    if (y == ff || vis[y]) continue;
    dfs(y, x);
    f[x][0] += max(f[y][1], f[y][0]);
    f[x][1] += f[y][0];
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i)
    cin >> a[i] >> to[i], ++d[to[i]], es[to[i]].push_back(i);
  for (int i = 1; i <= n; ++i)
    if (!d[i]) q.push(i);
  for (; !q.empty(); q.pop()) {
    int x = q.front();
    if (!--d[to[x]]) q.push(to[x]);
  }
  for (int i = 1; i <= n; ++i) {
    if (d[i] && !vis[i]) {
      loop.push_back({});
      for (int x = i; !vis[x]; vis[x] = 1, x = to[x])
        loop.back().push_back(x);
    }
  }
  for (auto i : loop)
    for (int j : i) dfs(j, 0);
  // cerr << f[5][0] << ' ' << f[5][1] << '\n';
  int ans = 0;
  for (auto &lp : loop) {
    int res = 0;
    for (int _ = 0; _ < 2; ++_) {
      for (size_t i = 0; i < lp.size(); ++i) {
        if (i == 0) {
          g[i][0] = f[lp[i]][0];
          g[i][1] = -0x3f3f3f3f;
        }
        else {
          g[i][0] = max(g[i - 1][0], g[i - 1][1]) + f[lp[i]][0];
          g[i][1] = g[i - 1][0] + f[lp[i]][1];
        }
      }
      cmax(res, max(g[lp.size() - 1][0], g[lp.size() - 1][1]));
      rotate(lp.begin(), lp.begin() + 1, lp.end());
    }
    ans += res;
  }
  cout << ans;
}
```

### P2607
同上，改成了无向边。
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9;
long double k;
int n, a[N], d[N], f[N][2], g[N][2];
bool vis[N];
queue<int> q;
vector<vector<int>> loop;
vector<int> es[N];
void dfs(int x, int ff) {
  f[x][1] = a[x], f[x][0] = 0;
  for (int y : es[x]) {
    if (y == ff || vis[y]) continue;
    dfs(y, x);
    f[x][0] += max(f[y][1], f[y][0]);
    f[x][1] += f[y][0];
  }
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i)
    cin >> a[i];
  for (int i = 1, x, y; i <= n; ++i)
    cin >> x >> y, ++x, ++y, ++d[x], ++d[y],
    es[x].push_back(y), es[y].push_back(x);
  cin >> k;
  for (int i = 1; i <= n; ++i)
    if (d[i] == 1) q.push(i);
  for (; !q.empty(); q.pop()) {
    int x = q.front();
    for (int y : es[x])
      if (--d[y] == 1) q.push(y);
  }
  for (int i = 1; i <= n; ++i) {
    if (d[i] > 1 && !vis[i]) {
      loop.push_back({});
      for (int x = i; !vis[x]; ) {
        loop.back().push_back(x);
        vis[x] = 1;
        for (int y : es[x])
          if (!vis[y] && d[y] > 1) {
            x = y;
            break;
          }
      }
    }
  }
  for (auto i : loop)
    for (int j : i) dfs(j, 0);
  int ans = 0;
  for (auto &lp : loop) {
    int res = 0;
    for (int _ = 0; _ < 2; ++_) {
      for (size_t i = 0; i < lp.size(); ++i) {
        if (i == 0) {
          g[i][0] = f[lp[i]][0];
          g[i][1] = -0x3f3f3f3f3f3f3f3f;
        }
        else {
          g[i][0] = max(g[i - 1][0], g[i - 1][1]) + f[lp[i]][0];
          g[i][1] = g[i - 1][0] + f[lp[i]][1];
        }
      }
      cmax(res, max(g[lp.size() - 1][0], g[lp.size() - 1][1]));
      rotate(lp.begin(), lp.begin() + 1, lp.end());
    }
    ans += res;
  }
  cout << fixed << setprecision(1) << ans * k;
}
```

### P4322
居然是分数规划。

考虑每个点取或不取 $w_i = 0/1$，答案就是 $\sum_{i} w_i\dfrac {p_i}{s_i}$。

考虑二分答案，$\sum_{i} w_i\dfrac {p_i}{s_i}\geq mid$ 拆开就是 $\sum_{i}w_i(p_i - mid \times s_i)\geq 0$。

令每个人的价值 $v_i = p_i - mid \times s_i$，那么问题就变成了树上选一个大小为 $k$ 联通块，其价值最大，树形背包即可。

写的时候发现自己 size 优化假了，```sz[x] += sz[y]``` 要在背包之后，否则是 $O(n^3)$。

$O(n^2)$，由于每次我都 dfs 求的，所以常数比较大，可以求 dfs 序然后 dp，常数更小，但是卡过了就不管了。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define d64 long double
constexpr int N = 2509;
constexpr d64 eps = 1e-4;
int n, s[N], p[N], fa[N], k, sz[N];
d64 val[N], f[N][N];
vector<int> es[N];
void dfs(int x) {
  sz[x] = 1, f[x][1] = val[x];
  for (int y : es[x]) {
    dfs(y);
    for (int i = min(k + 1, sz[x]); i; --i) {
      for (int j = 0; j <= sz[y] && i + j <= k + 1; ++j)
        cmax(f[x][i + j], f[x][i] + f[y][j]);
    }
    sz[x] += sz[y];
  }
}
bool chk(d64 x) {
  for (int i = 1; i <= n; ++i)
    val[i] = p[i] - x * s[i];
  for (int i = 0; i <= n; ++i)
    for (int j = 0; j <= k + 1; ++j) f[i][j] = -1e9;
  dfs(0);
  return f[0][k + 1] >= 0;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> k >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> s[i] >> p[i] >> fa[i];
    es[fa[i]].push_back(i);
  }
  d64 l = 0, r = 2.5e7;
  while (r - l > eps) {
    d64 mid = (l + r) / 2.;
    if (chk(mid)) l = mid;
    else r = mid;
  }
  cout << fixed << setprecision(3) << l;
}
```

### P8817
预处理每个点 $i \ge 2$，它可以到达的点 $j$，同时 $j$ 也可以到达 $1$，从里面选出最大的 $O(1)$ 个。

然后枚举 $b, c$，枚举其预处理的点作为 $a, d$，判掉相同的情况直接取 $\max$ 即可。

$O(n^2)$。
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2509;
int n, m, k, a[N], dst[N][N];
vector<int> es[N], to[N];
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> k;
  for (int i = 2; i <= n; ++i) cin >> a[i];
  for (int i = 1, x, y; i <= m; ++i) {
    cin >> x >> y;
    es[x].push_back(y), es[y].push_back(x);
  }
  memset(dst, 0x3f, sizeof dst);
  for (int i = 1; i <= n; ++i) {
    queue<int> q;
    dst[i][i] = 0;
    q.push(i);
    while (!q.empty()) {
      int x = q.front();
      q.pop();
      for (int y : es[x])
        if (dst[i][y] > dst[i][x] + 1) {
          dst[i][y] = dst[i][x] + 1;
          q.push(y);
        }
    }
  }
  for (int i = 2; i <= n; ++i) {
    vector<int> vec;
    for (int j = 2; j <= n; ++j) {
      if (dst[1][j] - 1 <= k && dst[i][j] - 1 <= k && j != i)
        vec.push_back(j);
    }
    sort(vec.begin(), vec.end(), [&](int x, int y) -> bool { return a[x] > a[y]; });
    for (int j = 0; j < 3 && j < vec.size(); ++j) to[i].push_back(vec[j]);
  }
  int ans = 0;
  for (int i = 2; i <= n; ++i) {
    for (int j = 2; j <= n; ++j) {
      if (i == j || dst[i][j] - 1 > k) continue;
      for (int b : to[i]) {
        if (i == b || j == b) continue; 
        for (int c : to[j]) {
          if (i == c || j == c || b == c) continue;
          ans = max(ans, a[i] + a[j] + a[b] + a[c]);
        }
      }
    }
  }
  cout << ans;
}
```
### P8818
不想动脑了，显然 $a$ 存一下最小最大，负数最大，正数最小。

然后 $b$ 直接存最小最大。

最后直接仿照暴力，枚举 $a, b$ 选的，分别取 $\min, \max$ 即可。

不用分讨，很好。

$O(n \log n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 1e5 + 9, inf = 0x3f3f3f3f;
int n, m, q, a[N], b[N];
int sta[20][N][4], stb[20][N][4];
int get(int x, int y, int t) {
  if (t < 2) return max(x, y);
  else return min(x, y);
}
int querya(int x, int y, int t) {
  int d = __lg(y - x + 1);
  return get(sta[d][x][t], sta[d][y - (1 << d) + 1][t], t);
}
int queryb(int x, int y, int t) {
  int d = __lg(y - x + 1);
  return get(stb[d][x][t], stb[d][y - (1 << d) + 1][t], t);
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> m >> q;
  for (int i = 1; i <= n; ++i) {
    cin >> a[i];
    sta[0][i][0] = sta[0][i][2] = a[i];
    sta[0][i][1] = -inf, sta[0][i][3] = inf;
    if (a[i] >= 0) sta[0][i][3] = a[i];
    if (a[i] <= 0) sta[0][i][1] = a[i];
  }
  for (int i = 1; i <= m; ++i) {
    cin >> b[i];
    stb[0][i][0] = stb[0][i][2] = b[i];
  }
  for (int i = 1; i < 20; ++i) {
    for (int j = 1; j + (1 << i) - 1 <= n; ++j) {
      for (int k = 0; k < 4; ++k)
        sta[i][j][k] = get(sta[i - 1][j][k], sta[i - 1][j + (1 << (i - 1))][k], k);
    }
  }
  for (int i = 1; i < 20; ++i) {
    for (int j = 1; j + (1 << i) - 1 <= m; ++j) {
      for (int k = 0; k < 4; k += 2)
        stb[i][j][k] = get(stb[i - 1][j][k], stb[i - 1][j + (1 << (i - 1))][k], k);
    }
  }
  while (q--) {
    int l1, r1, l2, r2;
    cin >> l1 >> r1 >> l2 >> r2;
    int ans = -inf * inf;
    // cerr << '\n';
    for (int i = 0; i < 4; ++i) {
      int tmp = inf * inf, A = querya(l1, r1, i);
      if (A == inf || A == -inf) continue;
      // cerr << A << '\n';
      for (int j = 0; j < 4; j += 2) tmp = min(tmp, A * queryb(l2, r2, j));
      ans = max(ans, tmp);
    }
    cout << ans << '\n';
  }
}
```

### P9755
先二分，然后对于每个点再二分求出最晚的种树时间。

接着考虑贪心，一开始写了一个无正确性的做法并获得了官方数据 $100$ 分。

正确做法应该是，令每个点最晚时间 $f_i = \min_{j} f_j - 1$，$j$ 是 $i$ 的儿子。

然后我们记一下 $f_i$ 小于等于 $i$ 的点个数是否超过 $i$，超过显然不行，否则是可以的。

$O(n\log^2 n)$

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
#define int long long
#define i128 __int128
constexpr int N = 1e5 + 9, inf = 0x3f3f3f3f3f3f3f3f;
int n, a[N], b[N], c[N], d[N], ed[N], f[N], ct[N];
vector<int> es[N];
i128 cal(int i, int l, int r) {
  assert(l <= r);
  if (l >= d[i]) return r - l + 1;
  int cr = min(d[i] - 1, r);
  return b[i] * (cr - l + 1) + (i128) c[i] * (cr + l) * (cr - l + 1) / 2 + r - cr;
}
int calc(int i, int x) {
  int l = 0, r = min(n, x);
  while (l < r) {
    int mid = (l + r + 1) >> 1;
    if (cal(i, mid, x) >= a[i]) l = mid;
    else r = mid - 1;
  }
  return l;
}
void dfs(int x, int ff) {
  vector<int> vec;
  for (int y : es[x]) {
    if (y ^ ff) dfs(y, x), cmin(f[x], f[y] - 1), vec.push_back(f[y]);
  }
  // sort(vec.begin(), vec.end());
  // for (size_t i = 0; i < vec.size(); ++i)
  //   cmin(f[x], (int) (vec[i] - i - 1));
    // cmin(f[x], vec[i] - 1);
}
bool chk(int day) {
  // cerr << "DAY: " << day << '\n';
  for (int i = 1; i <= n; ++i) {
    f[i] = ed[i] = calc(i, day);
    if (ed[i] == 0) return false;
    // cerr << ed[i] << ' ';
  }
  // cerr << '\n';
  dfs(1, 0);
  for (int i = 1; i <= n; ++i) ct[i] = 0;
  for (int i = 1; i <= n; ++i) {
    if (f[i] < 1) return false;
    ++ct[f[i]];
  }
  for (int i = 1; i <= n; ++i) {
    ct[i] += ct[i - 1];
    if (ct[i] > i) return false;
  }
  return true;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n;
  for (int i = 1; i <= n; ++i) cin >> a[i] >> b[i] >> c[i];
  for (int i = 1, x, y; i < n; ++i)
    cin >> x >> y, es[x].push_back(y), es[y].push_back(x);
  for (int i = 1; i <= n; ++i) {
    // b + dc < 1
    int l = 1, r = 0x3f3f3f3f;
    while (l < r) {
      int mid = (l + r) >> 1;
      if (b[i] + c[i] * mid < 1) r = mid;
      else l = mid + 1;
    }
    d[i] = l;
  }
  int l = 1, r = 1e9;
  while (l < r) {
    int mid = (l + r) >> 1;
    if (chk(mid)) r = mid;
    else l = mid + 1;
  }
  cout << l;
}
```

### P9753
哈希加栈的做法显然。

考虑 dp，令 $f_i$ 表示以 $i$ 结尾的子串个数。

答案即为 $\sum_{i} f_i$。
考虑令 $g_i$ 为小于 $i$ 最大的点，满足 $[g_i, i]$ 是合法的，如果没有就是 $0$。那么显然有 $s_i = s_{g_i}$，每次我们暴力的去跳 $g_i\leftarrow g_{g_i} - 1$，直到与 $s_i$ 相等，由于 $[g_{g_i}, g_i]$ 是合法的，所以每次必然是跳一个合法的串。

复杂度 $O(|\sum | n)$，证明没时间先不写了。

```cpp
#include <bits/stdc++.h>
using namespace std;
template<class T> inline bool cmax(T &x, T y) { if (x < y) return x = y, true; return false; }
template<class T> inline bool cmin(T &x, T y) { if (x > y) return x = y, true; return false; }
constexpr int N = 2e6 + 9;
int n, f[N], g[N];
string s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> s;
  s = ' ' + s;
  for (int i = 1; i <= n; ++i) {
    g[i] = i - 1;
    while (g[i] >= 0 && s[i] != s[g[i]]) g[i] = g[g[i]] - 1;
    if (g[i] > 0) f[i] += f[g[i] - 1] + 1;
  }
  cout << accumulate(f + 1, f + n + 1, 0ll);
}
```

--------
算了就到这吧，文章要爆了，之后再开新的吧。
