import unittest
from media_library import MediaItem
import sys
from unittest.mock import MagicMock

# Mock customtkinter before importing app
sys.modules["customtkinter"] = MagicMock()
sys.modules["tkinter"] = MagicMock()

try:
    from app import get_item_tag
except ImportError:
    pass

class TestAppLogic(unittest.TestCase):
    def test_get_item_tag(self):
        # Case 1: Airing -> Blue
        item = MediaItem("Show", "Group", "Airing", "Airing", "Airing", "Airing")
        item.is_airing = True
        self.assertEqual(get_item_tag(item), "blue")

        # Case 2: WEB-DL -> Red
        item = MediaItem("Show", "Group", "1080p", "WEB-DL", "H.264", "AAC")
        self.assertEqual(get_item_tag(item), "red")

        # Case 2b: WEB DL (space)
        item = MediaItem("Show", "Group", "1080p", "WEB DL", "H.264", "AAC")
        self.assertEqual(get_item_tag(item), "red")

        # Case 3: BD Encode + SVT-AV1 -> Light Green
        item = MediaItem("Show", "Group", "1080p", "BD Encode", "SVT-AV1", "OPUS")
        self.assertEqual(get_item_tag(item), "light_green")

        # Case 3b: BD Encode + SVT-AV1 (hyphen/space variations)
        item = MediaItem("Show", "Group", "1080p", "BD-Encode", "SVT AV1", "OPUS")
        self.assertEqual(get_item_tag(item), "light_green")

        # Case 4: BD Encode + Not SVT-AV1 -> Orange
        item = MediaItem("Show", "Group", "1080p", "BD Encode", "H.264", "AAC")
        self.assertEqual(get_item_tag(item), "orange")

        item = MediaItem("Show", "Group", "1080p", "BD Encode", "x265", "AAC")
        self.assertEqual(get_item_tag(item), "orange")

        # Case 5: BD Remux + H.264/MPEG2 -> Green
        item = MediaItem("Show", "Group", "1080p", "BD Remux", "H.264", "AAC")
        self.assertEqual(get_item_tag(item), "green")

        # Case 5b: DVD + MPEG2 -> Green
        item = MediaItem("Show", "Group", "480p", "DVD", "MPEG2", "AC3")
        self.assertEqual(get_item_tag(item), "green")

        # Case 5c: DVD + x264 -> Green (since H.264 or MPEG2)
        item = MediaItem("Show", "Group", "480p", "DVD", "x264", "AC3")
        self.assertEqual(get_item_tag(item), "green")

        # Case 6: Unknown/Other -> No tag
        item = MediaItem("Show", "Group", "1080p", "HDTV", "H.264", "AAC")
        self.assertEqual(get_item_tag(item), "")

        # Check Remux strictness
        item = MediaItem("Show", "Group", "1080p", "Remux", "H.264", "AAC")
        self.assertEqual(get_item_tag(item), "")

if __name__ == "__main__":
    unittest.main()
