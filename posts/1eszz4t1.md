---
title: "字符串"
date: 2025-08-07T10:08:23+08:00
author: "Mr_Min"
category: "个人记录"
tags: ["个人记录", "洛谷"]
source: "https://www.luogu.com.cn/article/1eszz4t1"
luogu_id: "1eszz4t1"
---

```cpp
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
struct strhash { // 1-index
  int n;
  vector<hash_t> h1, h2, pw;
  template <class T> void init(int m, T a) {
    h1.resize(m + 2), h2.resize(m + 2), pw.resize(m + 2);
    n = m, pw[0] = 1;
    for (int i = 1; i <= m; ++i) pw[i] = pw[i - 1] * seed;
    for (int i = 1; i <= m; ++i) h1[i] = h1[i - 1] * seed + hash_t::shift(a[i]);
    for (int i = m; i >= 1; --i) h2[i] = h2[i + 1] * seed + hash_t::shift(a[i]);
  }
  hash_t queryp(int l, int r) const {
    assert(1 <= l && r <= n);
    return h1[r] - h1[l - 1] * pw[r - l + 1];
  }
  u64 query1(int l, int r) const {
    return queryp(l, r).h;
  }
  hash_t querys(int l, int r) const {
    assert(1 <= l && r <= n);
    return h2[l] - h2[r + 1] * pw[r - l + 1];
  }
  u64 query2(int l, int r) const {
    return querys(l, r).h;
  }
};
```
