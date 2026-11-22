"""Offline regression tests for Luogu discovery and the sync entry point."""

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import sync_articles as sync


def listing(ids, *, count=None, key="lid"):
    articles = {"result": [{key: aid, "title": f"Title {aid}",
                             "category": {"name": "题解"}} for aid in ids]}
    if count is not None:
        articles["count"] = count
    return '<script id="lentille-context" type="application/json">' + json.dumps(
        {"data": {"articles": articles}}
    ) + '</script>'


class ListingTests(unittest.TestCase):
    def test_json_only_lid_without_html_links(self):
        self.assertEqual(sync.parse_listing(listing(["new00001"])), {
            "new00001": {"title": "Title new00001", "category": "题解"}
        })

    def test_other_supported_identifier_keys(self):
        for key in ("id", "articleId", "article_id", "identifier"):
            with self.subTest(key=key):
                self.assertIn("new00001", sync.parse_listing(listing(["new00001"], key=key)))

    def test_ignore_unrelated_links_when_structured_list_exists(self):
        page = listing(["new00001"]) + '<a href="/article/other001">Other</a>'
        self.assertEqual(list(sync.parse_listing(page)), ["new00001"])

    def test_legacy_html_links(self):
        self.assertIn("new00001", sync.parse_listing('<a href="/article/new00001">Post</a>'))

    def test_invalid_pages_are_not_empty_columns(self):
        for page in ("安全访问中心", "<html>Login</html>", '<script id="lentille-context">{}</script>',
                     '<script id="lentille-context">not json</script>',
                     listing(["invalid!"])):
            with self.subTest(page=page), self.assertRaises(sync.SyncError):
                sync.parse_listing(page)

    def test_real_empty_list(self):
        self.assertEqual(sync.parse_listing(listing([], count=0)), {})

    def test_discovers_78_and_forwards_cookie_on_every_page(self):
        ids = [f"post{i:04d}" for i in range(78)]
        pages = [listing(ids[i:i + 20], count=78) for i in range(0, 78, 20)]
        with patch.object(sync, "http_get", side_effect=pages) as get:
            self.assertEqual(list(sync.discover_articles(551389, cookie="test-cookie")), ids)
        self.assertEqual(get.call_count, 4)
        for page, call in enumerate(get.call_args_list, 1):
            self.assertEqual(call.args, (f"{sync.LUOGU}/user/551389/article?page={page}",))
            self.assertEqual(call.kwargs, {"cookie": "test-cookie"})

    def test_short_page_is_not_end_of_listing(self):
        pages = [listing(["post0001", "post0002"], count=3), listing(["post0003"], count=3)]
        with patch.object(sync, "http_get", side_effect=pages):
            self.assertEqual(len(sync.discover_articles(1)), 3)

    def test_without_total_continue_until_explicit_empty_page(self):
        pages = [listing(["post0001"]), listing(["post0002"]), listing([])]
        with patch.object(sync, "http_get", side_effect=pages):
            self.assertEqual(len(sync.discover_articles(1)), 2)

    def test_repeated_page_is_failure(self):
        page = listing(["post0001"], count=78)
        with patch.object(sync, "http_get", return_value=page), self.assertRaisesRegex(sync.SyncError, "重复"):
            sync.discover_articles(1)

    def test_premature_empty_page_is_failure(self):
        with patch.object(sync, "http_get", side_effect=[listing(["post0001"], count=78), listing([], count=78)]):
            with self.assertRaisesRegex(sync.SyncError, "提前结束"):
                sync.discover_articles(1)

    def test_blocked_later_page_is_failure(self):
        with patch.object(sync, "http_get", side_effect=[listing(["post0001"], count=78), "安全访问中心"]):
            with self.assertRaises(sync.SyncError):
                sync.discover_articles(1)

    def test_changing_count_is_failure(self):
        with patch.object(sync, "http_get", side_effect=[listing(["post0001"], count=2), listing(["post0002"], count=3)]):
            with self.assertRaisesRegex(sync.SyncError, "总数变化"):
                sync.discover_articles(1)


class MainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.posts = self.root / "posts"
        self.posts.mkdir()
        (self.root / "README.md").write_text("<!-- posts:start -->\nold\n<!-- posts:end -->", encoding="utf-8")
        self.args = ["--out", str(self.posts), "--index", str(self.posts / "index.md"),
                     "--readme", str(self.root / "README.md"), "--delay", "0"]
        self.enterContext(patch.object(sync, "REPO_ROOT", self.root))
        self.enterContext(contextlib.redirect_stderr(io.StringIO()))

    def test_failed_discovery_never_updates_cached_73(self):
        known = {f"post{i:04d}": {"id": f"post{i:04d}", "title": "old"} for i in range(73)}
        with patch.object(sync, "load_catalogue", return_value=known), \
             patch.object(sync, "discover_articles", side_effect=sync.SyncError("blocked")), \
             patch.object(sync, "fetch_article") as fetch, patch.object(sync, "save_catalogue") as save:
            before = (self.root / "README.md").read_bytes()
            self.assertEqual(sync.main(self.args), 1)
            fetch.assert_not_called()
            save.assert_not_called()
            self.assertEqual((self.root / "README.md").read_bytes(), before)
            self.assertFalse((self.posts / "index.md").exists())

    def test_new_five_articles_are_added_to_existing_73(self):
        ids = [f"post{i:04d}" for i in range(78)]
        known = {aid: {"id": aid, "title": "old"} for aid in ids[:73]}
        pages = [listing(ids[i:i + 20], count=78) for i in range(0, 78, 20)]
        def fetch(aid, cookie=None):
            self.assertEqual(cookie, "env-cookie")
            return sync.Article(aid, "title", "markdown", author_uid=551389)
        with patch.dict(os.environ, {"LUOGU_COOKIE": "env-cookie"}), \
             patch.object(sync, "load_catalogue", return_value=known), \
             patch.object(sync, "http_get", side_effect=pages) as get, \
             patch.object(sync, "fetch_article", side_effect=fetch):
            self.assertEqual(sync.main(self.args), 0)
            self.assertTrue(all(c.kwargs["cookie"] == "env-cookie" for c in get.call_args_list))
        payload = json.loads((self.root / "data/articles.json").read_text())
        self.assertEqual(payload["count"], 78)
        self.assertEqual(len(list(self.posts.glob("*.md"))), 79)  # includes index
        for aid in ids[73:]:
            self.assertIn(aid, (self.posts / "index.md").read_text())
            self.assertIn(aid, (self.root / "README.md").read_text())

    def test_explicit_cookie_overrides_environment(self):
        with patch.dict(os.environ, {"LUOGU_COOKIE": "env-cookie"}), \
             patch.object(sync, "discover_articles", side_effect=sync.SyncError("blocked")) as discover:
            self.assertEqual(sync.main(self.args + ["--cookie", "explicit-cookie"]), 1)
            discover.assert_called_once_with(551389, cookie="explicit-cookie")

    def test_only_skips_discovery_and_preserves_old_index_entries(self):
        (self.posts / "old00001.md").write_text(sync.render(sync.Article("old00001", "old", "body")))
        with patch.object(sync, "discover_articles") as discover, \
             patch.object(sync, "fetch_article", return_value=sync.Article("new00001", "new", "body")):
            self.assertEqual(sync.main(self.args + ["--only", "new00001"]), 0)
            discover.assert_not_called()
        index = (self.posts / "index.md").read_text()
        self.assertIn("old00001", index)
        self.assertIn("new00001", index)

    def test_failed_fetch_preserves_existing_post_in_index(self):
        (self.posts / "old00001.md").write_text(sync.render(sync.Article("old00001", "old", "body")))
        with patch.object(sync, "fetch_article", side_effect=sync.SyncError("blocked")):
            self.assertEqual(sync.main(self.args + ["--only", "old00001"]), 1)
        self.assertIn("old00001", (self.posts / "index.md").read_text())


if __name__ == "__main__":
    unittest.main()
