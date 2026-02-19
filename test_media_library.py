import unittest
from media_library import MediaItem, MediaParser

class TestMediaParser(unittest.TestCase):
    def test_parse_root_folder_strict(self):
        folder = "To Your Eternity [Zaki][1080p][BD Encode][SVT-AV1][OPUS2.0]"
        path = "/test/path"
        item = MediaParser.parse_root_folder(folder, path)

        self.assertEqual(item.name, "To Your Eternity")
        self.assertEqual(item.group, "Zaki")
        self.assertEqual(item.resolution, "1080p")
        self.assertEqual(item.source, "BD Encode")
        self.assertEqual(item.video_codec, "SVT-AV1")
        self.assertEqual(item.audio_codec, "OPUS2.0")

    def test_parse_root_folder_another(self):
        folder = "86 - Eighty Six [Zaki][1080p][BD Encode][H.264][DTS-HD&AAC2.0]"
        path = "/test/path2"
        item = MediaParser.parse_root_folder(folder, path)

        self.assertEqual(item.name, "86 - Eighty Six")
        self.assertEqual(item.group, "Zaki")
        self.assertEqual(item.resolution, "1080p")
        self.assertEqual(item.source, "BD Encode")
        self.assertEqual(item.video_codec, "H.264")
        self.assertEqual(item.audio_codec, "DTS-HD&AAC2.0")

    def test_parse_season_override_full(self):
        parent = MediaItem("Show", "Group", "1080p", "BD", "H.265", "AC3")
        season_folder = "Season 03 [WEB-DL][H.264][AAC2.0]"
        path = "/test/path/season03"

        # Override tags: WEB-DL (Source), H.264 (Video), AAC2.0 (Audio)
        item = MediaParser.parse_season_override(season_folder, parent, path)

        self.assertEqual(item.name, "Show")
        self.assertEqual(item.season, "Season 03")
        self.assertEqual(item.group, "Group") # Inherited
        self.assertEqual(item.resolution, "1080p") # Inherited
        self.assertEqual(item.source, "WEB-DL") # Overridden
        self.assertEqual(item.video_codec, "H.264") # Overridden
        self.assertEqual(item.audio_codec, "AAC2.0") # Overridden

    def test_parse_season_override_partial(self):
        parent = MediaItem("Show", "Group", "1080p", "BD", "H.265", "AC3")
        season_folder = "Season 02 [WEB-DL]"
        path = "/test/path/season02"

        # Override: WEB-DL (Source)
        item = MediaParser.parse_season_override(season_folder, parent, path)

        self.assertEqual(item.season, "Season 02")
        self.assertEqual(item.source, "WEB-DL")
        self.assertEqual(item.video_codec, "H.265") # Inherited

    def test_parse_season_no_override(self):
        parent = MediaItem("Show", "Group", "1080p", "BD", "H.265", "AC3")
        season_folder = "Season 01"
        path = "/test/path/season01"

        item = MediaParser.parse_season_override(season_folder, parent, path)

        self.assertEqual(item.season, "Season 01")
        self.assertEqual(item.source, "BD")
        self.assertEqual(item.video_codec, "H.265")

if __name__ == '__main__':
    unittest.main()
