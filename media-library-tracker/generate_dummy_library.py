import os

DUMMY_LIBRARY_PATH = "dummy_library"

FOLDERS = [
    "86 - Eighty Six [Zaki][1080p][BD Encode][H.264][DTS-HD&AAC2.0]",
    "To Your Eternity [Zaki][1080p][BD Encode][SVT-AV1][OPUS2.0]",
    "Fullmetal Alchemist Brotherhood [Coalgirls][1080p][BluRay][H.264][FLAC]",
    "Spirited Away [Ghibli][1080p][BluRay][x264][DTS-ES]",
    "Attack on Titan [Commie][720p][TV][H.264][AAC]",
]

SEASON_OVERRIDES = {
    "To Your Eternity [Zaki][1080p][BD Encode][SVT-AV1][OPUS2.0]": [
        "Season 01",
        "Season 02",
        "Season 03 [WEB-DL][H.264][AAC2.0]"
    ],
    "Attack on Titan [Commie][720p][TV][H.264][AAC]": [
        "Season 1",
        "Season 2 [1080p][BD][H.264][FLAC]"
    ]
}

def create_dummy_library():
    if not os.path.exists(DUMMY_LIBRARY_PATH):
        os.makedirs(DUMMY_LIBRARY_PATH)
        print(f"Created {DUMMY_LIBRARY_PATH}")

    for folder in FOLDERS:
        path = os.path.join(DUMMY_LIBRARY_PATH, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Created {folder}")

        if folder in SEASON_OVERRIDES:
            for season in SEASON_OVERRIDES[folder]:
                season_path = os.path.join(path, season)
                os.makedirs(season_path, exist_ok=True)
                print(f"  Created season: {season}")

if __name__ == "__main__":
    create_dummy_library()
