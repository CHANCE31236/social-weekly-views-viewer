import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import social_views_viewer as app


class SocialViewsTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        for name, value in {"CONFIG_FILE": self.root / "accounts.json", "STATE_FILE": self.root / "state.json"}.items():
            p = patch.object(app, name, value); p.start(); self.addCleanup(p.stop)
        for name in ("ensure_dirs", "log_error"):
            p = patch.object(app, name); p.start(); self.addCleanup(p.stop)

    def test_account_object_and_legacy_list_load(self):
        account = {"platform": "TikTok", "account": "example", "public_url": "https://www.tiktok.com/@example"}
        for value in ([account], {"accounts": [account]}):
            app.CONFIG_FILE.write_text(json.dumps(value), encoding="utf-8")
            self.assertEqual(app.load_accounts()[0]["account"], "example")

    def test_empty_account_list_remains_empty(self):
        app.save_accounts([])
        self.assertEqual(app.load_accounts(), [])

    def test_invalid_accounts_are_preserved(self):
        for content in ("{", "null", '{"accounts": [5]}'):
            app.CONFIG_FILE.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError): app.load_accounts()
            self.assertEqual(app.CONFIG_FILE.read_text(encoding="utf-8"), content)

    def test_corrupt_saved_views_are_preserved(self):
        for content in ("{", '{"rows": []}', '{"rows": {"account": 5}}'):
            app.STATE_FILE.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError): app.load_state()
            self.assertEqual(app.STATE_FILE.read_text(encoding="utf-8"), content)

    def test_failed_json_replace_keeps_original(self):
        app.CONFIG_FILE.write_text('{"accounts": []}', encoding="utf-8")
        with patch.object(Path, "replace", side_effect=OSError("blocked")):
            with self.assertRaises(OSError): app.save_accounts([{"account": "new"}])
        self.assertEqual(app.CONFIG_FILE.read_text(encoding="utf-8"), '{"accounts": []}')
        self.assertFalse(app.CONFIG_FILE.with_suffix(".json.tmp").exists())

    def test_rename_retains_entered_views(self):
        old = {"platform": "TikTok", "account": "old"}
        new = {"platform": "TikTok", "account": "new"}
        instance = app.SocialViewsApp.__new__(app.SocialViewsApp)
        instance.accounts = [old]
        instance.root = None
        instance.lang = lambda: "en"
        instance.auto_save = Mock()
        instance.build_ui = Mock()
        instance.date_range = SimpleNamespace(get=lambda: "2026-10-01 to 2026-10-07")
        variable = SimpleNamespace(get=lambda: "1234")
        instance.view_vars = {instance.key_for(old): variable}
        with patch.object(app, "AccountDialog", return_value=SimpleNamespace(result=new)):
            instance.edit_account(old)
        self.assertEqual(instance.state["rows"][instance.key_for(new)]["views"], "1234")
        self.assertIs(instance.view_vars[instance.key_for(new)], variable)

    def test_platform_detection_uses_real_host_and_public_profile(self):
        for url in ("https://youtube.com.example.org/@user", "https://example.org/?redirect=tiktok.com"):
            self.assertEqual(app.detect_platform(url), "Other")
        self.assertEqual(app.infer_account("https://business.facebook.com/", "https://instagram.com/example")["platform"], "Instagram")
        self.assertEqual(app.infer_account("https://youtube.com/", "https://facebook.com/example")["platform"], "Facebook")

    def test_unsafe_urls_are_rejected_before_opening(self):
        for url in ("file:///C:/example", "javascript:alert(1)", "https://user:password@example.org", "https://example.org/a b"):
            with patch.object(app.subprocess, "Popen") as opened:
                with self.assertRaises(ValueError): app.open_url(url)
                opened.assert_not_called()

    def test_numbers_require_valid_whole_value(self):
        for text, expected in (("1,234", 1234), ("1.2K", 1200), ("2万", 20000), ("10+20", 30), ("0", 0)):
            self.assertEqual(app.parse_number_token(text)[1], expected)
        for text in ("-20", "abc123", "123abc", "1+", ""):
            self.assertIsNone(app.parse_number_token(text))

    def test_export_dates_must_be_valid_and_ordered(self):
        self.assertEqual(app.parse_date_range("2026-10-01 to 2026-10-07"), ("2026-10-01", "2026-10-07"))
        for text in ("bad", "2026-02-30 to 2026-03-01", "2026-10-07 to 2026-10-01"):
            with self.assertRaises(ValueError): app.parse_date_range(text)

    def test_csv_formula_like_text_is_escaped_and_numbers_stay_numeric(self):
        path = self.root / "report.csv"
        app.write_csv(path, [["account", "views"], ["=1+1", 25], ["\tABC", 0], ["ordinary", 10]])
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        self.assertEqual(rows[1], ["'=1+1", "25"])
        self.assertEqual(rows[2][0], "'\tABC")
        self.assertEqual(rows[3][0], "ordinary")

    @unittest.skipUnless(importlib.util.find_spec("openpyxl"), "Excel dependency is not installed")
    def test_excel_text_remains_literal(self):
        from openpyxl import load_workbook
        path = self.root / "report.xlsx"
        self.assertTrue(app.write_xlsx(path, [["account", "views"], ["=1+1", 25], ["#N/A", 0]]))
        book = load_workbook(path)
        try:
            self.assertEqual(book.active["A2"].value, "=1+1")
            self.assertEqual(book.active["A2"].data_type, "s")
            self.assertEqual(book.active["A3"].data_type, "s")
            self.assertEqual(book.active["B2"].data_type, "n")
        finally:
            book.close()


if __name__ == "__main__":
    unittest.main()
