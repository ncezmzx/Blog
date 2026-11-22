#!/usr/bin/env python3
"""Run the article sync, ensuring the configured cookie is used for discovery.

The sync module already accepts a cookie for article fetches, but its listing
scanner currently calls http_get without forwarding that cookie. Inject it only
for the author-list requests until discovery accepts a cookie directly.
"""

from __future__ import annotations

import os
import sys

import sync_articles


def cookie_from_args() -> str | None:
    """Return the --cookie argument, falling back to the Actions secret."""
    try:
        index = sys.argv.index("--cookie")
    except ValueError:
        return os.environ.get("LUOGU_COOKIE") or None
    if index + 1 >= len(sys.argv):
        return os.environ.get("LUOGU_COOKIE") or None
    return sys.argv[index + 1] or os.environ.get("LUOGU_COOKIE") or None


_cookie = cookie_from_args()
_original_http_get = sync_articles.http_get


def _http_get_with_discovery_cookie(url: str, **kwargs: object) -> str:
    """Attach the login cookie to article-list pages as well as article pages."""
    if "/user/" in url and "/article" in url and not kwargs.get("cookie"):
        kwargs["cookie"] = _cookie
    return _original_http_get(url, **kwargs)


sync_articles.http_get = _http_get_with_discovery_cookie
raise SystemExit(sync_articles.main())
