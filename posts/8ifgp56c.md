---
title: "字符串"
date: 2026-11-09T07:41:36+08:00
author: "Mr_Min"
category: "4"
tags: ["4", "洛谷"]
source: "https://www.luogu.com.cn/article/8ifgp56c"
luogu_id: "8ifgp56c"
---

### AC 自动机
kmp 可以线性求出一个文本串中，一个模式串出现的所有位置，AC 自动机则可以求出一个文本串中，多个模式串出现的所有位置。

本质上，AC 自动机即为一个建立在多个模式串上的 kmp。

#### 定义
令模式串为 $s_i$，文本串为 $t$，对 $s_i$ 建立以 $0$ 为根的字典树，令 $nxt_{u, c}$ 表示字典树上 $u$ 节点走 $c$ 字符到的点，$ed_u$ 表示该节点是否为某个模式串的终止节点，$fail_u$ 表示从 $0$ 到 $u$ 构成的字符串，其最长的后缀满足为某个模式串的前缀对应的字典树上的节点。相当于 kmp 中我们求的 border，但是在 AC 自动机中 $fail$ 并不要求是自身的前缀，只要在字典树上存在这个节点即可。

#### 构建

考虑构建 AC 自动机，唯一的问题是如何求出 $fail_u$。

考虑 bfs，我们从根节点出发，一路拓展。设当前在 $u$，我们考虑是否存在 $v = nxt_{u, c}$，若存在，我们令 $fail_v = nxt_{fail_u, c}$，这是显然的，并继续拓展 $v$；若不存在，则为了方便后续的查询不用像 kmp 一样显式跳 $fail$，我们可以令 $nxt_{u, c} = nxt_{fail_u, c}$。

于是我们便完成了 AC 自动机的建立。

#### 用途

考虑其最基本的用途，即查询 $t$ 中，$s_i$ 出现的信息。

我们从根开始，按 $t_i$ 在 AC 自动机上遍历，设当前为 $u$，则我们可以 check $u, fail_u, fail_{fail_u}, \dots$ 这些点，若其为模式串终点即 $ed_u > 0$，则存在一个模式串匹配文本串，且匹配的末位已经确定。

直接跳 fail 会出现大量重复，考虑记忆化一下，通常情况我们只需要求模式串出现次数，因此可以将已经跳过的点标记，这样复杂度与模式串出现次数相关。

若模式串会出现多次，我们可以在 fail 树上标记这个点，之后跑在 fail 树上遍历一遍即可做到线性。

若保证匹配数只有 $O(1)$，则暴力查询的复杂度是正确的。

```
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1e6 + 9;
int n, ch[N][26], cnt[N], fail[N], rt, tot;
void ins(int &u, const string &str, int p) {
  if (!u) u = ++tot;
  if (str.size() == p) return ++cnt[u], void();
  ins(ch[u][str[p] - 'a'], str, p + 1);
}
void build() {
  queue<int> q;
  for (int i = 0; i < 26; ++i)
    if (ch[rt][i]) fail[ch[rt][i]] = rt, q.push(ch[rt][i]);
    else ch[rt][i] = rt;
  while (!q.empty()) {
    int x = q.front();
    q.pop();
    for (int i = 0; i < 26; ++i) {
      if (ch[x][i]) {
        fail[ch[x][i]] = ch[fail[x]][i];
        q.push(ch[x][i]);
      }
      else ch[x][i] = ch[fail[x]][i];
    }
  }
}
int query(const string &str) {
  int u = rt, res = 0;
  for (auto i : str) {
    u = ch[u][i - 'a'];
    for (int j = u; j != rt && cnt[j] != -1; j = fail[j])
      res += cnt[j], cnt[j] = -1;
  }
  return res;
}
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n, rt = ++tot;
  for (int i = 1; i <= n; ++i) {
    string s;
    cin >> s;
    ins(rt, s, 0);
  }
  build();
  string s;
  cin >> s;
  cout << query(s);
}
```

### 后缀数组
#### 定义
$sa_i$ 表示将 $s$ 的后缀按字典序从小到大排序后排名为 $i$ 的后缀的起始位置。

$rk_i$ 为以 $i$ 为起始位置的后缀的排名。

$h_i$ 表示 $\mathrm{lcp}(sa_i, sa_{i - 1})$，$h_1$ 不考虑。

#### 求法
##### 倍增排序
考虑枚举 $w = 2^0, 2^1, \dots$，那么我们每次将 $s_{i\dots i + w - 1}$ 排序，当 $w >= n$ 时即为 $sa_i$。

考虑从 $w \to 2w$ 要怎么排序，我们发现 $s_{i\dots i + 2w - 1} = s_{i\dots i + w - 1} + s_{i +w\dots i + 2w - 1}$，所以我们直接按 $(rk_i, rk_{i + w})$ 排序即可，$i > n$ 时 $rk_i = 0$。

直接做 2log，但是 $rk$ 值域只有 $n$，可以直接计数排序，做到 1log。

然后考虑一些常数优化。

首先双关键字排序，我们可以先排第二关键字，再排第一关键字（要求稳定排序）。于是我们先对 $rk_{i +w}$ 排序，这就相对于把 $n - w + 1\sim n$ 全部放到开头，剩余部分不变，因此第二关键字不用排序，扫一遍即可。

然后正常计数排序即可，$O(n\log n)$。

求 $h$ 考虑枚举后缀起始位置 $i$，我们维护一个 $k = h_{rk_i}$，当从 $i\to i + 1$ 时，我们容易发现 $sa_{rk_i - 1} + 1$ 与 $i + 1$ 的 $\mathrm{lcp}$ 至少为 $k - 1$，因此令 $h_{i + 1} = k - 1$，再暴力扩展即可，复杂度 $O(n)$。

```cpp
struct SA {
  int n;
  vector<int> sa, rk, id, h;
  void bucsort(int m, const auto &key) {
    vector<int> buc(m + 1);
    for (int i = 1; i <= n; ++i) ++buc[rk[i]];
    for (int i = 1; i <= m; ++i) buc[i] += buc[i - 1];
    for (int i = n; i >= 1; --i) sa[buc[rk[id[i]]]--] = id[i];
    for (int i = 1; i <= n; ++i) id[sa[i]] = id[sa[i - 1]] + (key(sa[i - 1]) != key(sa[i]));
    rk.swap(id);
  }
  void build(const string &s) {
    n = s.size() - 1, rk.resize(n + 1), sa.resize(n + 1), id.resize(n + 1), h.resize(n + 1);
    for (int i = 1; i <= n; ++i) rk[i] = s[i], sa[i] = id[i] = i;
    bucsort(128, [&](int x) { return rk[x]; });
    for (int w = 1, p = 0; w <= n; w <<= 1, p = 0) {
      for (int i = n - w + 1; i <= n; ++i) id[++p] = i;
      for (int i = 1; i <= n; ++i)
        if (sa[i] > w) id[++p] = sa[i] - w;
      bucsort(rk[sa[n]], [&](int x) { return make_pair(rk[x], x + w <= n ? rk[x + w] : 0); });
      if (rk[sa[n]] == n) break;
    }
    for (int i = 1, k = 0; i <= n; ++i) {
      if (k) --k;
      while (s[i + k] == s[sa[rk[i] - 1] + k]) ++k;
      h[rk[i]] = k;
    }
  }
};
```

##### SA-IS
挖坑。

#### 简单用法

查询任意两个后缀的 $\mathrm{lcp}$，$\mathrm{lcp}(i, j) = \min_{rk_i < k \le rk_j}h_k$。

### runs
#### 定义
$(l, r, p)$ 为 run 当且仅当 $s_{l\dots r}$ 的最小整周期为 $p$ 且 $r - l +1 \ge 2p$，且 $l, r$ 均无法再向两侧延伸。

其中 $e = \frac{r - l +1}p \ge 2$ 为 run 的指数。

#### 性质
##### 性质 1
长度为 $n$ 的串 $s$ 中的 runs 数量不超过 $n$，指数和不超过 $3n$。

不会证。
##### 性质 2
两个周期分别为 $p, q$ 的 run，重叠部分长度 $< p +q - \gcd(p, q)$。

证明：由周期引理可知，若长为 $m$ 的串 $s$ 存在周期 $p, q$ 满足 $m\le p + q - \gcd(p, q)$ 则 $\gcd(p, q)$ 也为 $s$ 的周期。因此若重叠部分 $\ge p + q - \gcd(p, q)$，则该部分存在周期 $\gcd(p, q)$，则两个 run 都存在周期 $\gcd(p, q)$，而这与 run 的周期最小性和极大性矛盾，所以不可能。

周期引理之后再补。
#### 求 runs
类似优秀的拆分，我们可以枚举周期 $p$，然后每隔 $p$ 设置检查点，则 run 必然会跨过两个相邻的检查点，于是我们对于两个检查点为起点的前后缀分别求 $\mathrm{lcs},\mathrm{lcp}$ 最后用基数排序再去重即可。

$O(n\log n)$。

模板题写的 2log，因为基数排序被卡空间了。

```cpp
#include <bits/extc++.h>
using namespace std;
constexpr int N = 1e6 + 9;
using u64 = unsigned long long;
int n;
template<size_t U = 20, size_t Z = 64, class T = int> struct st {
  int n;
  vector<size_t> f;
  array<vector<T>, U> st;
  vector<T> pr, sf, arr;
  void build(vector<T> &vec) {
    n = vec.size() - 1, st.fill(vector<T>((n / Z) + 1));
    f.resize(n + 1);
    arr.swap(vec), pr = sf = arr;
    for (int i = 1; i <= n; ++i) {
      if (i == 1 || i % Z == 0) st[0][i / Z] = arr[i];
      else st[0][i / Z] = min(st[0][i / Z], arr[i]);
      if (i / Z == (i - 1) / Z) pr[i] = min(pr[i - 1], pr[i]);
    }
    for (int i = n - 1; i >= 1; --i)
      if ((i + 1) / Z == i / Z) sf[i] = min(sf[i + 1], sf[i]);
    for (int i = 1; i < U; ++i)
      for (int j = 1; j + (1 << i) - 1 <= n / Z; ++j) st[i][j] = min(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
    vector<int> stk(n + 1);
    int tp = 0;
    for (int i = 1; i <= n; ++i) {
      if (i / Z != (i - 1) / Z) tp = 0;
      else f[i] = f[i - 1];
      while (tp && arr[i] < arr[stk[tp]]) f[i] &= ~(1ULL << (stk[tp--] & (Z - 1)));
      stk[++tp] = i, f[i] |= 1ULL << (i & (Z - 1));
    }
  }
  inline T query(int l, int r) {
    if (l / Z == r / Z) return arr[l + __builtin_ctzll(f[r] >> (l & (Z - 1)))];
    T ret = min(pr[r], sf[l]);
    l /= Z, r /= Z, ++l, --r;
    if (l <= r) {
      int d = __lg(r - l + 1);
      ret = min(ret, min(st[d][l], st[d][r - (1 << d) + 1]));
    }
    return ret;
  }
};
int sa[N], rk[N], rk1[N], id[N], buc[N];
vector<int> h;
st<14, 64, int> str, rev;
void bucsort(int m, const auto &key) {
  memset(buc, 0, (m + 1) * sizeof(int));
  for (int i = 1; i <= n; ++i) ++buc[rk[i]];
  for (int i = 1; i <= m; ++i) buc[i] += buc[i - 1];
  for (int i = n; i >= 1; --i) sa[buc[rk[id[i]]]--] = id[i];
  for (int i = 1; i <= n; ++i) id[sa[i]] = id[sa[i - 1]] + (key(sa[i - 1]) != key(sa[i]));
  memcpy(rk, id, (n + 1) * sizeof(int));
}
void build(const string &s) {
  for (int i = 1; i <= n; ++i) rk[i] = s[i], sa[i] = id[i] = i;
  bucsort(128, [&](int x) { return rk[x]; });
  for (int w = 1, p = 0; w <= n; w <<= 1, p = 0) {
    for (int i = n - w + 1; i <= n; ++i) id[++p] = i;
    for (int i = 1; i <= n; ++i)
      if (sa[i] > w) id[++p] = sa[i] - w;
    bucsort(rk[sa[n]], [&](int x) { return make_pair(rk[x], x + w <= n ? rk[x + w] : 0); });
    if (rk[sa[n]] == n) break;
  }
  h.resize(n + 1);
  for (int i = 1, k = 0; i <= n; ++i) {
    if (k) --k;
    while (s[i + k] == s[sa[rk[i] - 1] + k]) ++k;
    h[rk[i]] = k;
  }
}
int lcp(int i, int j) {
  if (i < 1 || j < 1 || i > n || j > n) return 0;
  if (rk1[i] > rk1[j]) swap(i, j);
  return i == j ? n - i + 1 : str.query(rk1[i] + 1, rk1[j]);
};
int lcs(int i, int j) {
  if (i < 1 || j < 1 || i > n || j > n) return 0;
  if (rk[i] > rk[j]) swap(i, j);
  return i == j ? n - i + 1 : rev.query(rk[i] + 1, rk[j]);
};
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  string s;
  cin >> s, n = s.size();
  build(' ' + s);
  memcpy(rk1, rk, sizeof rk);
  str.build(h);
  build(' ' + string(s.rbegin(), s.rend()));
  rev.build(h);
  vector<u64> runs;
  int cnt = 0;
  for (int i = 1; i <= n / 2; ++i)
    for (int j = 1; j + i <= n; j += i) ++cnt;
  runs.reserve(cnt);
  for (int i = 1; i <= n / 2; ++i) {
    for (int j = 1; j + i <= n; j += i) {
      int x = j, y = j + i;
      int lp = lcp(x, y), ls = lcs(n - x + 2, n - y + 2);
      if (lp + ls < i) continue;
      u64 l = x - ls, r = y + lp - 1;
      runs.push_back(l << 40 | r << 20 | i);
    }
  }
  sort(runs.begin(), runs.end());
  int m = unique(runs.begin(), runs.end(), [&](u64 x, u64 y) -> bool { return ((x ^ y) >> 20) == 0; }) - runs.begin();
  cout << m << '\n';
  for (int i = 0; i < m; ++i) cout << (runs[i] >> 40) << ' ' << (runs[i] >> 20 & 1048575) << ' ' << (runs[i] & 1048575) << '\n';
}
```
### Lyndon 串

#### 定义
$s$ 为 Lyndon 串，当且仅当 $s$ 字典序严格小于其所有真后缀，等价于 $s$ 严格小于其所有非平凡循环移位。

#### 性质

##### 性质1
若 $u < v$ 且 $u, v$ 均为 Lyndon 串，则 $uv$ 为 Lyndon 串。

证明显然。

##### 性质 2
若 $s$ 的最小整周期为 $n$ 则 $s$ 循环移位后必然存在一个 Lyndon 串。

证明同样显然。

#### Lyndon 分解
将一个串 $s$ 分解为若干个字典序单调不增的 Lyndon 串。

Lyndon 分解必然存在且唯一。
##### 栈

根据性质 1，用栈维护 Lyndon 分解，不断合并即可，用字符串哈希维护，二分比较大小，$O(n\log n)$。

##### Duval

我们考虑将 $s$ 划分为两部分 $a, b$，其中 $a$ 的 Lyndon 分解已经求出，我们在 $b$ 中扫，由于 Lyndon 串的最小整周期为 $n$，所以我们扫过的部分必然有 $< n$ 的周期，因此设扫到的部分为 $u^k v$。

考虑下一个字符：
- 若加入后可以满足周期，直接加入。
- 若比周期里的字符大，则加入后整个串为一个 Lyndon 串，周期为 $n$，更新一下。
- 若更小，则划分原串，求出 Lyndon 分解。

$O(n)$。

[P6114 【模板】Lyndon 分解](https://www.luogu.com.cn/problem/P6114)

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 5e6 + 9;
int n, ans;
string s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> s, n = s.size(), s = ' ' + s;
  for (int i = 1; i <= n; ) {
    int j = i, k = i + 1;
    while (j <= n && k <= n) {
      if (s[j] == s[k]) ++j, ++k;
      else if (s[j] < s[k]) j = i, ++k;
      else break;
    }
    while (i <= j) {
      ans ^= k - j + i - 1;
      i += k - j;
    }
  }
  cout << ans;
}
```

#### 最小表示法
容易发现，令 $s \leftarrow s +s$，求 Lyndon 分解后，找到起点 $\le n$ 的最后一个 Lyndon 串，以此为起点向后找 $n$ 个即为最小表示法。

正确性显然。

[P13270 【模板】最小表示法](https://www.luogu.com.cn/problem/P13270)

```cpp
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 1e7 + 9;
int n;
string s;
signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  cin >> n >> s, s = ' ' + s + s;
  int p = 0;
  for (int i = 1; i <= n; ) {
    p = i;
    int j = i, k = i + 1;
    while (j <= 2 * n && k <= 2 * n) {
      if (s[j] == s[k]) ++j, ++k;
      else if (s[j] < s[k]) j = i, ++k;
      else break;
    }
    while (i <= j) i += k - j;
  }
  for (int i = p; i < p + n; ++i) cout << s[i];
}
```

#### 练习
##### [QOJ18004 Call You With Your Name](https://qoj.ac/problem/18004/statement/zh_cn)

> 给定只含小写字母的非空字符串 $s_0$ 和 $n$ 个正整数 $l_i$。参数为 $l_i$ 的操作将当前字符串 $s$ 替换为无限循环串 $s^\omega$ 的前 $l_i$ 个字符。每个操作恰好执行一次，顺序任意；求使最终字符串字典序最大的操作编号排列。
>
> $\sum |s_0| \le 10^5, \sum n \le 10^5, 1 \le l_i \le 10^9.$


观察发现若 $l_a \ge l_b$ 且 $l_a$ 比 $l_b$ 先操作，那么 $l_a$ 这个操作是无效的，于是我们只有后缀最小值需要操作。

因为若 $s_1 > s_2$ 则操作后 $s_1 \ge s_2$，因此贪心选择即可。

于是我们可以按 $l_i$ 从小到大依次贪心选择是否选取此操作，若操作 $l_i$ 会使字典序变大就选取否则不选。

字典序比较可以直接二分，那么就需要求前缀哈希值和单点字符。

问题变成如何快速计算 $s_0$ 在经过 $l_{p_1}< l_{p_2}< \dots < l_{p_m}$ 操作后，一段前缀的哈希值和一个位置的字符。

可以直接递归处理，每层二分其在本层操作前的位置，每层至少 $\div 2$，所以最多递归 $\log$ 层，复杂度 $O(\log^2 n)$。

然后外层比较还有一个二分，于是复杂度是 $O(n\log^3n)$。

[code](https://qoj.ac/submission/3372039)

##### [QOJ18209 Call You With Your Name 3](https://qoj.ac/problem/18209/statement/zh_cn)
> 称不是 Lyndon 串的非空串为好的。给定小写字母串 $s$，将其划分为若干好的连续子串，使每段字典序单调不降。判断是否存在这样的划分；若存在，输出各段的结束位置。

> $\sum |s| \le 2 \times 10^6.$


因为 Lyndon 串的定义是大于所有后缀，考虑从后往前 dp，令 $f_i$ 表示以 $i$ 开头的子串为 $s_{i,\dots,f_i}$。

先跑一遍 SA，则所有非 $rk$ 的后缀最小值都是合法的，令其 $f_i = n$。

随后我们观察一下，假设有一段合法子串 $s[i:p]$（$p< n$），显然存在 $s[i:p] > s[q:p]$，因为不是 Lyndon 串，同时存在 $s[i:n] < s[q:n]$，因为是极长。这两个条件显然可以推出 $s[q:p]$ 是 $s[i:p]$ 的前缀，于是我们得到了合法子串的充要条件。

于是我们枚举 $q$，令 $p$ 为大于 $q$ 的最小的存在划分的起点，那么我们只要找到所有以 $s[q:p]$ 为前缀的 $s[i:p]$ 更新即可。

具体的，直接按 $rk$ 排序，每次找 $rk_q$ 附近的后缀，求 $\mathrm{lcp}$ 判断是否为前缀即可，用 set 维护，每个位置最多被删一次，复杂度是 $O(n\log n)$。

[code](https://qoj.ac/submission/3364692)

##### [QOJ22878 Call You With Your Name 4](https://qoj.ac/problem/22878/statement/zh_cn)

> 给定长度为 $n$ 的小写英文字母串 $s$，每次可以把一个字符改成任意小写英文字母。求使它成为 Lyndon 串的最少修改次数。
>
> $\sum n^2 \le 9 \times 10^6.$


首先会议 duval 的过程，我们维护了一个 $u^kv$，因为此题要改成 Lyndon 串，所以前缀必然是 $u^kv$ 的形式。

先考虑答案上界，一个显然的修改方案是先将前 $S$ 个字符改为 $a$，再每隔 $S$ 个字符改一个变成 $z$，这显然是合法的，$S = \sqrt n$ 时，次数最小 $2\sqrt n +O(1)$。

考虑直接暴搜，我们考虑维护 duval 的指针 $i, j, k$，其中 $i$ 是已分解的前缀，不需要，于是只用维护 $j, k$ 和一个答案 $ans$。

再 duval 中 $k$ 是不断增大，直到无法形成 $u^kv$ 的形式，但在我们的目标是 Lyndon 串，不会出现这种情况，所以 $k$ 从 $1\sim n$，于是我们可以修改 $s_k$，然后维护 $j, ans$。

但是这样状态数很多，考虑剪枝。如果我们搜出来一个前缀 $s_{1\dots p}$ 是 Lyndon 串，那我们记录一个 $f_p$ 表示最小代价，然后枚举 $k$ 时，只要 $f_k$ 小于等于当前代价直接剪枝。

这样显然是对的，因为一个我们把一个 Lyndon 串的前缀改成一个 Lyndon 串，则整串还是 Lyndon 串。因此若一个前缀是 Lyndon 串，则最后的答案串替换成这个前缀代价**不降**，所以可以直接删去超过 $f_k$ 的情况。

最后分析状态数，如果 $s_j = s_k$ 那么 $(j, k) \to (j + 1, k + 1)$，若 $s_j < s_k$ 那么 $(j, k)\to (1, k + 1)$。

其中 $(1, k)$ 的状态必然更新 $f_k$，因此不超过 $O(n\sqrt n)$。

而 $(1, k)$ 只有满足 $s_1 = s_k$ 这一种情况会转移到 $(2, k + 1)$，而且一旦出现 $s_j < s_k$ 就会回到 $(1, *)$，因此 $(j, *)$ 最多只有 $O(n^2\sqrt n)$ 种。

最后复杂度 $O(n^2\sqrt n)$，注意到实际上状态数很少，轻松通过。

[code](https://qoj.ac/submission/3381466)
