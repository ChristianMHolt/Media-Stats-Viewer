import unittest
from unittest.mock import MagicMock
import sys

# Mock customtkinter before importing app
sys.modules["customtkinter"] = MagicMock()
sys.modules["tkinter"] = MagicMock()

# Now import app
from app import get_item_tag
from media_library import MediaItem

class TestVerificationLogic(unittest.TestCase):
    def test_rejected_status(self):
        # Any item with status "rejected" should be "red" (Bad)

        # Case 1: Was Blue (Airing)
        item = MediaItem("Show", "Group", "Airing", "Airing", "Airing", "Airing", is_airing=True)
        self.assertEqual(get_item_tag(item, "rejected"), "red")

        # Case 2: Was Green (Great)
        item = MediaItem("Show", "Group", "1080p", "BD Remux", "H.264", "AAC")
        self.assertEqual(get_item_tag(item, "rejected"), "red")

        # Case 3: Was Light Green (Good)
        item = MediaItem("Show", "Group", "1080p", "BD Encode", "SVT-AV1", "OPUS")
        self.assertEqual(get_item_tag(item, "rejected"), "red")

        # Case 4: Was Orange (Okay)
        item = MediaItem("Show", "Group", "1080p", "BD Encode", "x265", "AAC")
        self.assertEqual(get_item_tag(item, "rejected"), "red")

    def test_verified_status(self):
        # "verified" -> "light_green" (Good), unless it was "green" (Great).

        # Case 1: Was Green (Great) -> Stay Green
        item = MediaItem("Show", "Group", "1080p", "BD Remux", "H.264", "AAC")
        self.assertEqual(get_item_tag(item, "verified"), "green")

        # Case 2: Was Blue (Airing) -> Become Light Green
        item = MediaItem("Show", "Group", "Airing", "Airing", "Airing", "Airing", is_airing=True)
        self.assertEqual(get_item_tag(item, "verified"), "light_green")

        # Case 3: Was Light Green (Good) -> Stay Light Green
        item = MediaItem("Show", "Group", "1080p", "BD Encode", "SVT-AV1", "OPUS")
        self.assertEqual(get_item_tag(item, "verified"), "light_green")

        # Case 4: Was Orange (Okay) -> Become Light Green
        item = MediaItem("Show", "Group", "1080p", "BD Encode", "x265", "AAC")
        self.assertEqual(get_item_tag(item, "verified"), "light_green")

        # Case 5: Was Red (Bad) -> Become Light Green
        item = MediaItem("Show", "Group", "1080p", "WEB-DL", "H.264", "AAC")
        self.assertEqual(get_item_tag(item, "verified"), "light_green")

    def test_no_status(self):
        # Should behave as before (None or empty string)
        item = MediaItem("Show", "Group", "Airing", "Airing", "Airing", "Airing", is_airing=True)
        self.assertEqual(get_item_tag(item, None), "blue")
        self.assertEqual(get_item_tag(item), "blue")

        item = MediaItem("Show", "Group", "1080p", "WEB-DL", "H.264", "AAC")
        self.assertEqual(get_item_tag(item), "red")

if __name__ == "__main__":
    unittest.main()
