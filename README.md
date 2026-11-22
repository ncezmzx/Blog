# Blog

本仓库收录了洛谷用户 [Mr_Min](https://www.luogu.com.cn/user/551389)（UID 551389）在
[个人专栏](https://www.luogu.com.cn/user/551389/article) 发布的专栏文章，
并以 Markdown 形式保存在 [`posts/`](posts/) 下。

正文取自洛谷前端内嵌的原始 Markdown（而非渲染后的 HTML），因此**公式的 LaTeX 源码、
代码块与图片引用都完整保留**，可以直接用 Jekyll / Hugo / Hexo 等静态博客生成器渲染。

## 目录结构

| 路径 | 说明 |
| --- | --- |
| [`posts/<文章 id>.md`](posts/) | 每篇文章一个文件，正文为原文 Markdown |
| [`posts/index.md`](posts/index.md) | 按发布时间倒序排列的文章索引（自动生成） |
| [`data/articles.json`](data/articles.json) | 文章 id / 标题 / 分类的结构化索引 |
| [`scripts/sync_articles.py`](scripts/sync_articles.py) | 同步脚本 |
| [`.github/workflows/sync-luogu-articles.yml`](.github/workflows/sync-luogu-articles.yml) | 每天自动同步的 CI 工作流 |

文件名使用洛谷文章 id（如 `sywuq2b7.md`），便于与原文一一对应。

## Front-matter

每篇文章开头都有 YAML front-matter：

```yaml
---
title: "review"                              # 标题
date: 2026-09-03T23:23:43+08:00              # 发布时间（东八区）
author: "Mr_Min"                             # 作者
category: "数据结构"                          # 洛谷专栏分类
tags: ["数据结构", "洛谷"]                     # 标签
source: "https://www.luogu.com.cn/article/sywuq2b7"
luogu_id: "sywuq2b7"                         # 洛谷文章 id
---
```

## 如何同步

```bash
python3 scripts/sync_articles.py --uid 551389 --out posts --index posts/index.md
```

脚本会：

1. 每次重新抓取 `https://www.luogu.com.cn/user/<uid>/article` 的全部分页，从内嵌 JSON
   （包括 `lid` 字段）或文章链接中提取 id，并按列表返回的总数校验扫描完整性；
   `data/articles.json` 仅用于合并已知文章和补全元数据，不代替在线扫描；
2. 逐篇抓取文章页，解析 `<script id="lentille-context">` 中内嵌的原始 Markdown；
   若洛谷返回反爬页面，则回退到 [洛谷档案馆](https://www.luogu.ac.cn) 的 API；
3. 写出 `posts/<id>.md` 与 `posts/index.md`，并更新本 README 的文章列表。

仓库中的 [CI 工作流](.github/workflows/sync-luogu-articles.yml) 每天自动执行两次，
并把结果提交回分支。若洛谷对匿名访问限制较严，可在仓库中配置 `LUOGU_COOKIE` secret，
脚本自动读取同名环境变量，并在**列表扫描和正文抓取**时都带上该 Cookie；
也可以用 `--cookie` 显式指定（优先于环境变量）。

若列表返回反爬/登录页面、分页重复或未达到声明的总数，脚本会报错退出并保留已有文件，
不会再把“扫描 0 篇、只更新旧目录”当作同步成功。可在 Actions 中手动运行工作流重试；
`--only <id> ...` 仍可跳过扫描同步指定文章，`--reindex` 可离线重建索引。

运行离线回归测试：

```bash
python3 -m unittest discover -s tests -v
```

## 文章列表

<!-- posts:start -->

| 发布日期 | 标题 | 分类 | 原文 |
| --- | --- | --- | --- |
| 2026-11-16 | [不知道有什么用](x50t1ye5.md) | 1 | [洛谷](https://www.luogu.com.cn/article/x50t1ye5) |
| 2026-11-13 | [网络流和二分图相关](4ucuq35k.md) | 4 | [洛谷](https://www.luogu.com.cn/article/4ucuq35k) |
| 2026-11-09 | [字符串](8ifgp56c.md) | 4 | [洛谷](https://www.luogu.com.cn/article/8ifgp56c) |
| 2026-11-06 | [CSP 游记](tjy9hbj2.md) | 5 | [洛谷](https://www.luogu.com.cn/article/tjy9hbj2) |
| 2026-10-31 | [反射容斥](ymmxpy1f.md) | 4 | [洛谷](https://www.luogu.com.cn/article/ymmxpy1f) |
| 2026-10-30 | [2026.10.20 \| 喵喵题](rgzauen6.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/rgzauen6) |
| 2026-10-30 | [QOJ10092. Interactive Primality](vnedtiot.md) | 题解 | [洛谷](https://www.luogu.com.cn/article/vnedtiot) |
| 2026-10-30 | [3-smooth](489of6fu.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/489of6fu) |
| 2026-10-29 | [2026.10.29 \| k-简并图](6aqykgs6.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/6aqykgs6) |
| 2026-10-28 | [题解：P6908 [ICPC 2015 WF] Evolution in Parallel](bp1ujflk.md) | 题解 P6908 | [洛谷](https://www.luogu.com.cn/article/bp1ujflk) |
| 2026-10-28 | [题解：P6958 [NEERC 2017] The Great Wall](3wghkige.md) | 题解 P6958 | [洛谷](https://www.luogu.com.cn/article/3wghkige) |
| 2026-10-26 | [题解：AT_utpc2024_p Perfect Suika Game on a Tree](1svyin1u.md) | 题解 AT_utpc2024_p | [洛谷](https://www.luogu.com.cn/article/1svyin1u) |
| 2026-10-24 | [题解：P17148 [ICPC 2017 Xi'an R] Naomi with Array](7p7xxib2.md) | 题解 P17148 | [洛谷](https://www.luogu.com.cn/article/7p7xxib2) |
| 2026-10-24 | [题解：P7650 [BalticOI 2007] Ranklist Sorting (Day 1)](jkiackr5.md) | 题解 P7650 | [洛谷](https://www.luogu.com.cn/article/jkiackr5) |
| 2026-10-21 | [题解：AT_npcapc_2024_o New School Term](8g197jnx.md) | 题解 AT_npcapc_2024_o | [洛谷](https://www.luogu.com.cn/article/8g197jnx) |
| 2026-09-03 | [review](sywuq2b7.md) | 数据结构 | [洛谷](https://www.luogu.com.cn/article/sywuq2b7) |
| 2026-03-06 | [模板](bogywyli.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/bogywyli) |
| 2026-02-05 | [？？？？？](bqe58gq8.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/bqe58gq8) |
| 2026-02-04 | [dp 套 dp](5foe608f.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/5foe608f) |
| 2026-02-03 | [dp 优化](bapdutdb.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/bapdutdb) |
| 2026-02-02 | [博弈论](yubi1jt6.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/yubi1jt6) |
| 2026-01-31 | [组合计数](caoh8hih.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/caoh8hih) |
| 2025-12-09 | [异或](ggp37eg7.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/ggp37eg7) |
| 2025-11-23 | [2025.11.23](pvn7jqu0.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/pvn7jqu0) |
| 2025-11-22 | [一些东西](lmrduaop.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/lmrduaop) |
| 2025-11-22 | [2025.11.22](23umu1mi.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/23umu1mi) |
| 2025-11-20 | [2025.11.20](fr04it0h.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/fr04it0h) |
| 2025-11-19 | [2025.11.19](bxpcsekk.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/bxpcsekk) |
| 2025-11-17 | [记录 续 续 续 续](7kctpgxf.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/7kctpgxf) |
| 2025-11-17 | [2025.11.17](zb6jc54x.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/zb6jc54x) |
| 2025-11-17 | [2025.11.17](di2hccd5.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/di2hccd5) |
| 2025-11-17 | [换根 lca](4dswj1tm.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/4dswj1tm) |
| 2025-11-15 | [2025.11.15](ozduto88.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/ozduto88) |
| 2025-11-14 | [2025.11.14](uhkow7zc.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/uhkow7zc) |
| 2025-11-13 | [2025.11.13](41ztefms.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/41ztefms) |
| 2025-11-12 | [2025.11.12](kw6qktxd.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/kw6qktxd) |
| 2025-11-11 | [2025.11.11](9j4x2ars.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/9j4x2ars) |
| 2025-11-10 | [2025.11.10](25fh5u9b.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/25fh5u9b) |
| 2025-11-05 | [记录 续 续 续](fl5ccfv8.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/fl5ccfv8) |
| 2025-11-04 | [CSP2025 游记](tky2vcxu.md) | 生活·游记 | [洛谷](https://www.luogu.com.cn/article/tky2vcxu) |
| 2025-10-28 | [2025.10.28 模拟赛](pthfi5ih.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/pthfi5ih) |
| 2025-10-27 | [2025.10.27 模拟赛](y0n1ijvl.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/y0n1ijvl) |
| 2025-10-24 | [2025.10.24 模拟赛](lrxknfwu.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/lrxknfwu) |
| 2025-10-22 | [记录 续 续](0zt6kmcr.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/0zt6kmcr) |
| 2025-10-18 | [2025.10.18](1epqa5ic.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/1epqa5ic) |
| 2025-10-16 | [记录 续](cn2jwcqz.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/cn2jwcqz) |
| 2025-10-11 | [记录 2](opi28na4.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/opi28na4) |
| 2025-10-10 | [记录](nxgwm1e4.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/nxgwm1e4) |
| 2025-10-06 | [2025.10.06](dvg7sfnz.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/dvg7sfnz) |
| 2025-10-05 | [2025.10.05](p7l37czb.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/p7l37czb) |
| 2025-10-04 | [2025.10.04](xfebv8pi.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/xfebv8pi) |
| 2025-10-03 | [2025.10.03](mgopvqmn.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/mgopvqmn) |
| 2025-10-03 | [2025.10.02](uopsyx6n.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/uopsyx6n) |
| 2025-10-03 | [2025.10.01](7hjop5oj.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/7hjop5oj) |
| 2025-09-09 | [modint](28wm9h8v.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/28wm9h8v) |
| 2025-09-04 | [高位前缀和](3xulybkw.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/3xulybkw) |
| 2025-09-04 | [一些神秘题](lbqovftx.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/lbqovftx) |
| 2025-08-30 | [图论](owfcnm5i.md) | 算法·理论 | [洛谷](https://www.luogu.com.cn/article/owfcnm5i) |
| 2025-08-28 | [自然数幂次和](17bpshkd.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/17bpshkd) |
| 2025-08-26 | [数论](jxykezke.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/jxykezke) |
| 2025-08-26 | [位运算](dyiymqz1.md) | 算法·理论 | [洛谷](https://www.luogu.com.cn/article/dyiymqz1) |
| 2025-08-25 | [曼哈顿距离](r03dpuhy.md) | 算法·理论 | [洛谷](https://www.luogu.com.cn/article/r03dpuhy) |
| 2025-08-23 | [2025.8.22](cxiwk48n.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/cxiwk48n) |
| 2025-08-23 | [2025.8.23](zydp7560.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/zydp7560) |
| 2025-08-20 | [2025.8.20](r5u6pxjj.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/r5u6pxjj) |
| 2025-08-19 | [2025.8.19](v8po59rb.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/v8po59rb) |
| 2025-08-15 | [Dinic](d6beeged.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/d6beeged) |
| 2025-08-09 | [2025.8.9](14mtj3m4.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/14mtj3m4) |
| 2025-08-07 | [字符串](1eszz4t1.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/1eszz4t1) |
| 2025-08-06 | [2025.8.6](uxvedl47.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/uxvedl47) |
| 2025-08-05 | [2025.8.5](9k55z8rq.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/9k55z8rq) |
| 2025-08-02 | [2025.8.2](fonw740n.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/fonw740n) |
| 2025-08-01 | [2025.7.29](ov82ly2r.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/ov82ly2r) |
| 2025-07-26 | [2025.7.26](z0t9i9nk.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/z0t9i9nk) |
| 2025-07-25 | [2025.7.25](ebv38s8u.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/ebv38s8u) |
| 2025-07-24 | [DP 优化](adpqu113.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/adpqu113) |
| 2025-07-23 | [2025.7.23](69oge4gt.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/69oge4gt) |
| 2025-07-22 | [2025.7.22](m5jv8y2s.md) | 个人记录 | [洛谷](https://www.luogu.com.cn/article/m5jv8y2s) |

<!-- posts:end -->
