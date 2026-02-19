import os

def create_dummy_library():
    base_dir = "dummy_library"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    structures = [
        # Show with mixed seasons
        {
            "path": "To Your Eternity [Zaki][1080p][BD Encode][SVT-AV1][OPUS2.0]",
            "subdirs": [
                "Season 01",
                "Season 03 [WEB-DL][H.264][AAC2.0]"
            ]
        },
        # Show without seasons (files in root)
        {
            "path": "86 - Eighty Six [Zaki][1080p][BD Encode][H.264][DTS-HD&AAC2.0]",
            "subdirs": []
        },
        # Movie
        {
            "path": "Movie Title [ReleaseGroup][2160p][BluRay][HEVC][TrueHD]",
            "subdirs": []
        },
        # Show with consistent seasons but override on one
        {
            "path": "Another Show [Group][720p][HDTV][x264][AC3]",
            "subdirs": [
                "Season 01",
                "Season 02 [WEB-DL][x264][AAC]"
            ]
        }
    ]

    for item in structures:
        folder_path = os.path.join(base_dir, item["path"])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Create dummy file in root if no subdirs, or just generally
        with open(os.path.join(folder_path, "dummy.mkv"), "w") as f:
            f.write("dummy content")

        for sub in item["subdirs"]:
            sub_path = os.path.join(folder_path, sub)
            if not os.path.exists(sub_path):
                os.makedirs(sub_path)
            with open(os.path.join(sub_path, "episode.mkv"), "w") as f:
                f.write("dummy content")

    print(f"Dummy library created at {os.path.abspath(base_dir)}")

if __name__ == "__main__":
    create_dummy_library()
