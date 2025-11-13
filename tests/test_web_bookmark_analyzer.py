"""
Tests for the WebBookmarkAnalyzer module.
"""

import unittest
import os
from cognitive_tribunal.modules.web_bookmark_analyzer import WebBookmarkAnalyzer

class TestWebBookmarkAnalyzer(unittest.TestCase):
    """
    Unit tests for the WebBookmarkAnalyzer.
    """

    def setUp(self):
        """
        Set up a dummy bookmark file for testing.
        """
        self.dummy_bookmarks_html = """
        <!DOCTYPE NETSCAPE-Bookmark-file-1>
        <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
        <TITLE>Bookmarks</TITLE>
        <H1>Bookmarks</H1>
        <DL><p>
            <DT><H3 ADD_DATE="1678886400" LAST_MODIFIED="1678886400" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks bar</H3>
            <DL><p>
                <DT><A HREF="https://www.google.com/" ADD_DATE="1609459200">Google</A>
                <DT><A HREF="https://github.com/" ADD_DATE="1577836800">GitHub</A>
            </DL><p>
        </DL><p>
        """
        self.dummy_file_path = "test_bookmarks.html"
        with open(self.dummy_file_path, "w", encoding="utf-8") as f:
            f.write(self.dummy_bookmarks_html)

    def tearDown(self):
        """
        Clean up the dummy bookmark file.
        """
        if os.path.exists(self.dummy_file_path):
            os.remove(self.dummy_file_path)

    def test_analyze_bookmarks(self):
        """
        Test that the analyzer correctly parses a bookmark file.
        """
        analyzer = WebBookmarkAnalyzer()
        results = analyzer.analyze_bookmarks(self.dummy_file_path)

        self.assertEqual(results["stats"]["total_bookmarks"], 2)
        self.assertEqual(len(results["bookmarks"]), 2)

        first_bookmark = results["bookmarks"][0]
        self.assertEqual(first_bookmark["title"], "Google")
        self.assertEqual(first_bookmark["url"], "https://www.google.com/")
        self.assertEqual(first_bookmark["add_date"], "2021-01-01T00:00:00")

        second_bookmark = results["bookmarks"][1]
        self.assertEqual(second_bookmark["title"], "GitHub")
        self.assertEqual(second_bookmark["url"], "https://github.com/")
        self.assertEqual(second_bookmark["add_date"], "2020-01-01T00:00:00")

if __name__ == '__main__':
    unittest.main()
