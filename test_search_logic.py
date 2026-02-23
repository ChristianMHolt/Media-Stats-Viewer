import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock customtkinter to avoid GUI errors in headless environment
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

# Now import app
import app

class TestSearchLogic(unittest.TestCase):
    def setUp(self):
        # Access the SearchEngine class from the fast_search module/object in app
        self.SearchEngine = app.fast_search.SearchEngine
        self.engine = self.SearchEngine()

    def test_search_basic(self):
        items = ["The Matrix", "Matrix Reloaded", "Avatar", "Titanic"]
        self.engine.add_items(items)

        # Test exact match (case insensitive)
        indices = self.engine.search("matrix")
        # Should match "The Matrix" (0) and "Matrix Reloaded" (1)
        self.assertEqual(sorted(indices), [0, 1])

    def test_search_and_logic(self):
        items = ["Resolution 1080p x265", "Resolution 720p x264", "Resolution 1080p x264"]
        self.engine.add_items(items)

        # Test "1080p x265" -> should match index 0 only
        indices = self.engine.search("1080p x265")
        self.assertEqual(indices, [0])

        # Test "x264 1080p" -> should match index 2 only (order independent)
        indices = self.engine.search("x264 1080p")
        self.assertEqual(indices, [2])

    def test_search_empty(self):
        items = ["A", "B"]
        self.engine.add_items(items)
        indices = self.engine.search("")
        self.assertEqual(indices, [])

    def test_search_no_match(self):
        items = ["A", "B"]
        self.engine.add_items(items)
        indices = self.engine.search("C")
        self.assertEqual(indices, [])

if __name__ == '__main__':
    unittest.main()
