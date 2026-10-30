---
title: "QOJ10092. Interactive Primality"
date: 2026-10-30T10:08:14+08:00
author: "Mr_Min"
category: "题解"
tags: ["题解", "洛谷"]
source: "https://www.luogu.com.cn/article/vnedtiot"
luogu_id: "vnedtiot"
---

好难好难。

> 有一个数 $1\le x \le 10^{18}$，你可以进行至多 $875$ 次询问，每次询问一个数 $k\le 10^{18}$，交互库会回答你 $x +k$ 是否为质数。你需要求出 $x$。

首先若 $x + k$ 为质数，意味着对于任意一个 $m < x + k$，$x +k \not \equiv 0\pmod m\iff x \not \equiv -k \pmod m$。

也就是说，每次询问到是质数，我们就可以对于一个模数 $m$，排除一个余数。

考虑用多个小模数，最后用 CRT 合并，取 $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 37, 43, 47, 53$，没有选 $31$ 是因为这 $15$ 个数合并刚好是 $1.05 \times 10^{18}$。

考虑先随机询问，直到问到一个质数。

此时从所有模数中去掉一个余数，之后考虑从每个模数随机选一个余数，然后用 crt 合并出 $k$，询问这个 $k$ 便可以一次性筛掉多个余数。由于质数分布是稠密的，询问次数不多。

但是这样还是卡不进 $875$，考虑随机选余数合并 $k$ 的过程。

如果一个模数 $p$ 的余数唯一确定 $k$，那么 $x\equiv k\pmod p$，我们选一个询问 $a$，若 $p\mid a + k$，则 $x\equiv k\equiv k - a - k\equiv -a\pmod p$，不用问。

如果没有确定，那么随一个询问 $a$，如果存在一个没有被排除的余数 $k$，满足 $p\mid a + k$，那么有 $x\not \equiv -a \equiv -a +a + k \equiv k\pmod p$，可以排掉 $k$。

这样就可以砍掉大量无用的询问。

```cpp
#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
mt19937 rng(1813815162);
uniform_int_distribution<i64> rg(1, (i64) 1e18);
namespace CRT {
  __int128 exgcd(__int128 a, __int128 b, __int128 &x, __int128 &y) {
    if (!b) return x = 1, y = 0, a;
    __int128 g = exgcd(b, a % b, y, x);
    return y -= a / b * x, g;
  }
  pair<__int128, __int128> inv_gcd(__int128 a, __int128 b) {
    a %= b;
    if (a < 0) a += b;
    __int128 x, y, g = exgcd(a, b, x, y);
    if (g != 1) x = (x % (b / g) + (b / g)) % (b / g);
    else x = (x % b + b) % b;
    return {g, x};
  }
  __int128 safe_mod(__int128 a, __int128 m) {
    a %= m;
    return a < 0 ? a + m : a;
  }
  pair<__int128, __int128> crt(vector<i64> r, vector<i64> m) {
    __int128 r0 = 0, m0 = 1;
    for (int i = 0; i < (int)r.size(); i++) {
      __int128 r1 = safe_mod(r[i], m[i]), m1 = m[i];
      if (m0 < m1) swap(r0, r1), swap(m0, m1);
      if (m0 % m1 == 0) {
        if (r0 % m1 != r1) return {0, 0};
        continue;
      }
      __int128 g, im;
      tie(g, im) = inv_gcd(m0, m1);
      if ((r1 - r0) % g) return {0, 0};
      __int128 u1 = m1 / g;
      __int128 t = (r1 - r0) / g % u1 * im % u1;
      r0 += t * m0;
      m0 *= u1;
      if (r0 < 0) r0 += m0;
    }
    return {r0, m0};
  }
}
set<int> s[15];
vector<i64> pr = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53};
bool ask(i64 x) {
  cout << "? " << x << endl;
  string s;
  cin >> s;
  if (s == "Busted") assert(0);
  return s == "Prime";
}
i64 solve() {
  for (int i = 0; i < 15; ++i)
    for (int j = 0; j < pr[i]; ++j) s[i].insert(j);
  int flg = false;
  while (true) {
    i64 w = rg(rng);
    if (flg) {
      vector<i64> r;
      for (int i = 0; i < 15; ++i) {
        int w = rng() % pr[i];
        if (s[i].size() == 1) {
          while ((w + *s[i].begin()) % pr[i] == 0) {
            w = rng() % pr[i];
          }
        }
        else {
          while (!s[i].count((pr[i] - w) % pr[i])) {
            w = rng() % pr[i];
          }
        }
        r.push_back(w);
      }
      w = CRT::crt(r, pr).first;
    }
    // for (int i = 0; i < r.size(); ++i) cerr << r[i] << ' ';
    // cerr << '\n';
    if (w > 1e18 || w <= 0) continue;
    if (ask(w)) {
      flg = true;
      bool ok = true;
      for (int i = 0; i < 15; ++i) {
        s[i].erase((pr[i] - w % pr[i]) % pr[i]);
        if (s[i].size() > 1) ok = false;
      }
      if (ok) break;
    }
  }
  vector<i64> r;
  for (int i = 0; i < 15; ++i) r.push_back(*s[i].begin());
  return CRT::crt(r, pr).first;
}
signed main() {
  int tt;
  cin >> tt;
  while (tt--) {
    i64 t = solve();
    // assert(1 <= t && t <= 1e18);
    cout << "! " << t << endl;
    string s;
    cin >> s;
  }
}
```
