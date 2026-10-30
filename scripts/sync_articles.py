#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync every article of a Luogu column author into this repository as Markdown.

Luogu's front-end embeds the *original Markdown source* of an article inside a
``<script id="lentille-context" type="application/json">`` blob.  Reading that
blob -- instead of the rendered page -- keeps the LaTeX intact: the rendered
HTML flattens every formula into unreadable unicode (``\\sum_{i=1}^n i`` turns
into ``∑i=1ni``).

Two sources are tried for every article:

1. ``https://www.luogu.com.cn/article/<id>`` -- the authoritative source.
2. ``https://www.luogu.ac.cn/api/v1/article/<id>`` -- the 洛谷档案馆 archive,
   used when Luogu answers with the "安全访问中心" interstitial.

Luogu's CDN answers the first request with a ``302`` back to the same URL and
a short lived ``C3VK`` cookie, so a cookie jar is required to complete the
handshake.

Usage::

    python3 scripts/sync_articles.py --uid 551389 --out posts --index posts/index.md
    python3 scripts/sync_articles.py --only sywuq2b7 6aqykgs6

Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPCookieProcessor, Request, build_opener

LUOGU = "https://www.luogu.com.cn"
ARCHIVE_API = "https://www.luogu.ac.cn/api/v1"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
BEIJING = timezone(timedelta(hours=8))
REPO_ROOT = Path(__file__).resolve().parent.parent

LENTILLE_RE = re.compile(
    r'<script[^>]*\bid=["\']lentille-context["\'][^>]*>(?P<json>.*?)</script>', re.DOTALL
)
ARTICLE_LINK_RE = re.compile(r"/article/([0-9a-z]{6,12})")
INTERSTITIAL_RE = re.compile(r"安全访问中心|即将离开洛谷")


class SyncError(RuntimeError):
    """Raised when an article can neither be fetched nor parsed."""


@dataclass
class Article:
    """A single Luogu article plus the metadata needed for the blog front-matter."""

    article_id: str
    title: str
    content: str
    author: str = ""
    author_uid: int = 0
    category: str = ""
    published: datetime | None = None
    tags: list[str] = field(default_factory=list)

    @property
    def source_url(self) -> str:
        return f"{LUOGU}/article/{self.article_id}"


def make_opener() -> Any:
    """An opener with a cookie jar, needed for Luogu's C3VK redirect handshake."""
    return build_opener(HTTPCookieProcessor(CookieJar()))


def http_get(url: str, *, attempts: int = 4, timeout: float = 30.0, cookie: str | None = None) -> str:
    """GET *url* and return the decoded body."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.6",
        "Referer": f"{LUOGU}/",
        "Cache-Control": "no-cache",
    }
    if cookie:
        headers["Cookie"] = cookie

    opener = make_opener()
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = Request(url, headers=headers)
            with opener.open(request, timeout=timeout) as response:  # noqa: S310
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except HTTPError as exc:
            last_error = exc
            if exc.code not in {408, 425, 429, 500, 502, 503, 504} or attempt == attempts:
                break
        except (URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt == attempts:
                break
        time.sleep(2.0 * attempt)
    raise SyncError(f"failed to fetch {url}: {last_error}")


def extract_lentille(html: str) -> dict[str, Any]:
    """Return the parsed ``lentille-context`` payload of a Luogu page."""
    match = LENTILLE_RE.search(html)
    if not match:
        raise SyncError("页面中没有 lentille-context 数据（可能返回了反爬页面）")
    return json.loads(match.group("json"))


def parse_datetime(value: Any) -> datetime | None:
    """Best-effort parsing of the many timestamp shapes Luogu uses."""
    if value in (None, "", 0):
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    text = str(value).strip()
    if text.isdigit():
        return datetime.fromtimestamp(int(text), tz=timezone.utc)
    candidate = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        try:
            parsed = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def load_catalogue() -> dict[str, dict[str, str]]:
    """Read ``data/articles.json`` (id -> title/category) if it exists."""
    path = REPO_ROOT / "data" / "articles.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {item["id"]: item for item in payload.get("articles", [])}


def load_catalogue_author() -> tuple[int, str]:
    """Read the author uid/name recorded in ``data/articles.json``."""
    path = REPO_ROOT / "data" / "articles.json"
    if not path.exists():
        return 551389, "Mr_Min"
    payload = json.loads(path.read_text(encoding="utf-8"))
    author = payload.get("author") or {}
    return int(author.get("uid") or 551389), str(author.get("name") or "Mr_Min")


def _walk(node: Any) -> Any:
    """Yield every dict inside a nested JSON structure."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk(value)


def parse_listing(html: str) -> dict[str, dict[str, str]]:
    """Extract ``{id: {"title": ..., "category": ...}}`` from an article-list page.

    The ids always come from the ``/article/<id>`` links in the page; titles and
    categories are additionally recovered from the embedded ``lentille-context``
    JSON when it exposes them.
    """
    link_ids = set(ARTICLE_LINK_RE.findall(html))
    found: dict[str, dict[str, str]] = {i: {"title": "", "category": ""} for i in link_ids}

    try:
        context = extract_lentille(html)
    except (SyncError, ValueError):
        context = {}
    for node in _walk(context):
        identifier = None
        for key in ("id", "articleId", "article_id", "identifier"):
            value = node.get(key)
            if isinstance(value, str) and value in link_ids:
                identifier = value
                break
        if identifier is None:
            continue
        title = node.get("title") or node.get("name") or ""
        category = node.get("category") or node.get("categoryName") or ""
        if isinstance(category, dict):
            category = category.get("name") or category.get("title") or ""
        found[identifier] = {
            "title": str(title),
            "category": str(category),
        }
    return found


def discover_articles(uid: int) -> dict[str, dict[str, str]]:
    """Walk the author's article-list pages and collect every article."""
    found: dict[str, dict[str, str]] = {}
    for page in range(1, 100):
        html = http_get(f"{LUOGU}/user/{uid}/article?page={page}")
        items = parse_listing(html)
        new = {i: v for i, v in items.items() if i not in found}
        if not new:
            break
        found.update(new)
        if len(items) < 10:
            break
    return found


def save_catalogue(path: Path, articles: dict[str, dict[str, str]], uid: int, name: str) -> None:
    """Write the machine readable catalogue of every known article."""
    payload = {
        "author": {"uid": uid, "name": name, "profile": f"{LUOGU}/user/{uid}"},
        "article_list": f"{LUOGU}/user/{uid}/article",
        "count": len(articles),
        "articles": [
            {
                "id": article_id,
                "title": meta.get("title", ""),
                "category": meta.get("category", ""),
                "source": f"{LUOGU}/article/{article_id}",
            }
            for article_id, meta in articles.items()
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_from_luogu(article_id: str, cookie: str | None = None) -> Article:
    """Fetch the raw Markdown straight from the Luogu front-end."""
    html = http_get(f"{LUOGU}/article/{article_id}", cookie=cookie)
    if INTERSTITIAL_RE.search(html):
        raise SyncError("洛谷返回了安全访问页（需要代理或 Cookie）")
    context = extract_lentille(html)
    data = context.get("data")
    data = data if isinstance(data, dict) else {}
    node = data.get("article") if isinstance(data.get("article"), dict) else None
    if node is None:
        for value in data.values():
            if isinstance(value, dict) and "content" in value:
                node = value
                break
    if node is None:
        raise SyncError("未能定位文章数据")

    author = node.get("author") if isinstance(node.get("author"), dict) else {}
    author_uid = int(author.get("uid") or node.get("authorUid") or 0)
    category = node.get("category")
    if isinstance(category, dict):
        category = category.get("name") or category.get("title") or ""
    published = None
    for key in ("time", "createdAt", "publishTime", "updatedAt"):
        published = parse_datetime(node.get(key))
        if published:
            break

    return Article(
        article_id=article_id,
        title=str(node.get("title") or "").strip(),
        content=str(node.get("content") or ""),
        author=str(author.get("name") or "").strip(),
        author_uid=author_uid,
        category=str(category or "").strip(),
        published=published,
    )


def fetch_from_archive(article_id: str, cookie: str | None = None) -> Article:
    """Fetch the raw Markdown from the 洛谷档案馆 archive."""
    payload = json.loads(http_get(f"{ARCHIVE_API}/article/{article_id}", cookie=cookie))
    if not isinstance(payload, dict) or "content_md" not in payload:
        message = payload.get("message") if isinstance(payload, dict) else payload
        raise SyncError(str(message))
    author = payload.get("author") or {}
    return Article(
        article_id=article_id,
        title=str(payload.get("title") or "").strip(),
        content=str(payload.get("content_md") or ""),
        author=str(author.get("name") or "").strip(),
        author_uid=int(author.get("uid") or 0),
        published=parse_datetime(payload.get("source_time")),
    )


def fetch_article(article_id: str, cookie: str | None = None) -> Article:
    """Try every source in turn and return the first successful article."""
    errors: list[str] = []
    for source in (fetch_from_luogu, fetch_from_archive):
        try:
            return source(article_id, cookie=cookie)
        except (SyncError, URLError, OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{source.__name__}: {exc}")
    raise SyncError("; ".join(errors))


def yaml_escape(value: str) -> str:
    """Escape a string for use inside a double-quoted YAML scalar."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render(article: Article) -> str:
    """Render one article as a Markdown file with YAML front-matter."""
    published = (article.published or datetime.now(tz=timezone.utc)).astimezone(BEIJING)
    published = published.replace(microsecond=0)
    tags = list(dict.fromkeys([article.category, "洛谷"])) if article.category else ["洛谷"]
    tag_list = ", ".join(f'"{yaml_escape(tag)}"' for tag in tags)

    front_matter = "\n".join(
        [
            "---",
            f'title: "{yaml_escape(article.title)}"',
            f"date: {published.isoformat()}",
            f'author: "{yaml_escape(article.author)}"',
            f'category: "{yaml_escape(article.category)}"',
            f"tags: [{tag_list}]",
            f'source: "{article.source_url}"',
            f'luogu_id: "{article.article_id}"',
            "---",
            "",
        ]
    )
    return f"{front_matter}\n{article.content.strip()}\n"


def render_table(articles: list[Article]) -> str:
    """Render the article table shared by ``posts/index.md`` and the README."""
    epoch = datetime.min.replace(tzinfo=timezone.utc)
    ordered = sorted(articles, key=lambda a: (a.published or epoch), reverse=True)
    lines = [
        "| 发布日期 | 标题 | 分类 | 原文 |",
        "| --- | --- | --- | --- |",
    ]
    for article in ordered:
        published = (article.published or epoch).astimezone(BEIJING)
        title = article.title.replace("|", "\\|")
        lines.append(
            f"| {published.strftime('%Y-%m-%d')} | [{title}]({article.article_id}.md) "
            f"| {article.category} | [洛谷]({article.source_url}) |"
        )
    return "\n".join(lines)


def write_index(articles: list[Article], index_path: Path) -> None:
    """Write a human readable index of every synced article."""
    header = "<!-- 由 scripts/sync_articles.py 自动生成，请勿手动修改 -->"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(f"{header}\n\n{render_table(articles)}\n", encoding="utf-8")


def read_posts(posts_dir: Path) -> list[Article]:
    """Read the front-matter of every already synced post (used by ``--reindex``)."""
    articles: list[Article] = []
    for path in sorted(posts_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        fields: dict[str, str] = {}
        for line in parts[1].strip().splitlines():
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"')
        articles.append(
            Article(
                article_id=fields.get("luogu_id", path.stem),
                title=fields.get("title", ""),
                content=parts[2],
                author=fields.get("author", ""),
                category=fields.get("category", ""),
                published=parse_datetime(fields.get("date")),
            )
        )
    return articles


def update_readme(readme_path: Path, articles: list[Article]) -> bool:
    """Refresh the article table between the ``posts:start`` / ``posts:end`` markers."""
    if not readme_path.exists():
        return False
    text = readme_path.read_text(encoding="utf-8")
    start, end = "<!-- posts:start -->", "<!-- posts:end -->"
    if start not in text or end not in text:
        return False
    head, _, rest = text.partition(start)
    _, _, tail = rest.partition(end)
    readme_path.write_text(
        f"{head}{start}\n\n{render_table(articles)}\n\n{end}{tail}", encoding="utf-8"
    )
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uid", type=int, default=551389, help="洛谷用户 UID")
    parser.add_argument("--out", default="posts", help="输出目录（默认 posts）")
    parser.add_argument("--index", default="posts/index.md", help="索引文件路径")
    parser.add_argument("--delay", type=float, default=1.5, help="每篇文章之间的间隔秒数")
    parser.add_argument("--cookie", default=None, help="可选的洛谷 Cookie")
    parser.add_argument("--only", nargs="*", help="只同步这些文章 id")
    parser.add_argument("--readme", default="README.md", help="需要更新文章列表的 README")
    parser.add_argument("--reindex", action="store_true", help="不联网，只根据已有文章重建索引")
    args = parser.parse_args(argv)

    if args.reindex:
        articles = read_posts(Path(args.out))
        write_index(articles, Path(args.index))
        if update_readme(Path(args.readme), articles):
            print(f"已更新 {args.readme} 的文章列表", file=sys.stderr)
        print(f"完成：{len(articles)} 篇，索引写入 {args.index}", file=sys.stderr)
        return 0

    catalogue = load_catalogue()
    known: dict[str, dict[str, str]] = {
        item["id"]: {"title": item.get("title", ""), "category": item.get("category", "")}
        for item in catalogue.values()
    }

    # 每次都重新扫描专栏列表，这样新发表的文章才能被发现；
    # 扫描失败时退回 data/articles.json 里已知的列表。
    discovered: dict[str, dict[str, str]] = {}
    if not args.only:
        try:
            discovered = discover_articles(args.uid)
            print(f"扫描到 {len(discovered)} 篇文章", file=sys.stderr)
        except (SyncError, URLError, OSError, ValueError) as exc:
            print(f"扫描专栏列表失败（{exc}），改用已知列表", file=sys.stderr)

    merged: dict[str, dict[str, str]] = {}
    for article_id, meta in discovered.items():
        old = known.get(article_id, {})
        merged[article_id] = {
            "title": old.get("title") or meta.get("title", ""),
            "category": old.get("category") or meta.get("category", ""),
        }
    for article_id, old in known.items():
        merged.setdefault(article_id, {"title": old.get("title", ""), "category": old.get("category", "")})

    ids = list(args.only) if args.only else list(merged)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"开始同步 {len(ids)} 篇文章……", file=sys.stderr)

    synced: list[Article] = []
    failures: list[tuple[str, str]] = []
    for index, article_id in enumerate(ids, start=1):
        try:
            article = fetch_article(article_id, cookie=args.cookie)
        except SyncError as exc:
            failures.append((article_id, str(exc)))
            print(f"[{index}/{len(ids)}] {article_id} 失败: {exc}", file=sys.stderr)
            continue

        # 列表页可能混有其它作者的文章，按作者 uid 过滤掉。
        if args.uid and article.author_uid and article.author_uid != args.uid:
            print(f"[{index}/{len(ids)}] {article_id} 跳过（属于 uid {article.author_uid}）", file=sys.stderr)
            continue

        meta = merged.get(article_id, {})
        article.title = article.title or meta.get("title", "")
        article.category = meta.get("category") or article.category
        if not article.author:
            article.author = "Mr_Min"
        merged[article_id] = {"title": article.title, "category": article.category}

        target = out_dir / f"{article_id}.md"
        target.write_text(render(article), encoding="utf-8")
        synced.append(article)
        print(
            f"[{index}/{len(ids)}] {article_id} -> {target} "
            f"({len(article.content)} 字符, {article.published}, {article.category})",
            file=sys.stderr,
        )
        time.sleep(args.delay)

    write_index(synced, Path(args.index))
    if update_readme(Path(args.readme), synced):
        print(f"已更新 {args.readme} 的文章列表", file=sys.stderr)
    save_catalogue(
        REPO_ROOT / "data" / "articles.json",
        merged,
        args.uid,
        load_catalogue_author()[1],
    )
    print(f"完成：{len(synced)}/{len(ids)} 篇，索引写入 {args.index}", file=sys.stderr)
    if failures:
        print("失败列表：" + ", ".join(aid for aid, _ in failures), file=sys.stderr)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
