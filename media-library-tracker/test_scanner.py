import sys
import os
import json

# Ensure we can import from backend
sys.path.append(os.getcwd())

from backend.scanner import scan_library

DUMMY_LIBRARY_PATH = "dummy_library"

def test_scanner():
    items = scan_library(DUMMY_LIBRARY_PATH)
    print(f"Found {len(items)} items.")

    # Use json for pretty printing
    # Convert Pydantic models to dict
    print(json.dumps([item.dict() for item in items], indent=2))

    # Verify specific items
    to_your_eternity = next((item for item in items if "To Your Eternity" in item.name), None)
    assert to_your_eternity is not None
    assert to_your_eternity.stats.group == "Zaki"
    assert to_your_eternity.stats.resolution == "1080p"
    assert len(to_your_eternity.children) == 3

    # Check Season 3 override
    s3 = next((child for child in to_your_eternity.children if "Season 03" in child.name), None)
    assert s3 is not None
    assert s3.stats.source == "WEB-DL" # Overridden
    assert s3.stats.video_codec == "H.264" # Overridden
    assert s3.stats.audio_codec == "AAC2.0" # Overridden
    assert s3.stats.resolution == "1080p" # Inherited
    assert s3.stats.group == "Zaki" # Inherited

    print("\nVerification Successful!")

if __name__ == "__main__":
    test_scanner()
