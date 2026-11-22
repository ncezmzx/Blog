#!/usr/bin/env python3
"""Compatibility entry point; cookie handling now lives in sync_articles itself."""

from __future__ import annotations

import sync_articles


if __name__ == "__main__":
    raise SystemExit(sync_articles.main())
