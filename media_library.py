import os
import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class MediaItem:
    name: str
    group: str
    resolution: str
    source: str
    video_codec: str
    audio_codec: str
    season: Optional[str] = None
    path: str = ""
    is_airing: bool = False

    def __post_init__(self):
        # Clean up name if needed
        self.name = self.name.strip()

class MediaParser:
    # Compile regexes for heuristic matching
    RES_REGEX = re.compile(r'(\d{3,4}p|4K|2K|8K)', re.IGNORECASE)
    SOURCE_REGEX = re.compile(r'(BD[- ]?Encode|WEB[- ]?DL|BluRay|HDTV|DVD|Remux)', re.IGNORECASE)
    VIDEO_REGEX = re.compile(r'(H\.?264|x264|H\.?265|x265|HEVC|AV1|SVT[- ]?AV1|VP9)', re.IGNORECASE)
    AUDIO_REGEX = re.compile(r'(AAC|DTS|FLAC|OPUS|AC3|E-AC3|TrueHD|Atmos)', re.IGNORECASE)

    @staticmethod
    def parse_root_folder(folder_name: str, path: str) -> Optional[MediaItem]:
        """
        Parses a root folder name assuming the format:
        Name [Group][Resolution][Source][Video Codec][Audio Codec]
        """
        # Check if the folder has brackets
        if '[' not in folder_name or ']' not in folder_name:
            # Fallback: just return the name as name, others empty
            return MediaItem(name=folder_name, group="", resolution="", source="", video_codec="", audio_codec="", path=path)

        # Split by first bracket to get Name
        try:
            name_part, rest = folder_name.split('[', 1)
            name = name_part.strip()

            # The rest is "Group][Resolution]..." so we add back the '[' for splitting or just split by ']['
            # Better approach: find all content inside brackets
            # But we need strict order

            # Reconstruct the bracket part
            bracket_content = '[' + rest
            # Find all matches of content inside []
            tags = re.findall(r'\[(.*?)\]', bracket_content)

            if len(tags) >= 5:
                # Assume strict order
                group = tags[0]
                resolution = tags[1]
                source = tags[2]
                video_codec = tags[3]
                audio_codec = tags[4]
                return MediaItem(name, group, resolution, source, video_codec, audio_codec, path=path)
            else:
                # If fewer tags, maybe use heuristics or fill sequentially?
                # The user implied strict format. If fewer, we might map what we have or leave empty.
                # Let's map sequentially for now, or use heuristics if strict fails?
                # Let's try to fill as much as possible.
                group = tags[0] if len(tags) > 0 else ""
                resolution = tags[1] if len(tags) > 1 else ""
                source = tags[2] if len(tags) > 2 else ""
                video_codec = tags[3] if len(tags) > 3 else ""
                audio_codec = tags[4] if len(tags) > 4 else ""
                return MediaItem(name, group, resolution, source, video_codec, audio_codec, path=path)
        except Exception as e:
            print(f"Error parsing {folder_name}: {e}")
            return MediaItem(name=folder_name, group="", resolution="", source="", video_codec="", audio_codec="", path=path)

    @staticmethod
    def parse_season_override(season_folder: str, parent_item: MediaItem, path: str) -> MediaItem:
        """
        Parses a season folder name: Season XX [Overriding info]
        Merges with parent_item.
        """
        # Extract season name (everything before first [)
        if '[' in season_folder:
            season_name, rest = season_folder.split('[', 1)
            season_name = season_name.strip()
            bracket_content = '[' + rest
            tags = re.findall(r'\[(.*?)\]', bracket_content)
        else:
            season_name = season_folder.strip()
            tags = []

        # Start with parent's attributes
        new_item = MediaItem(
            name=parent_item.name,
            group=parent_item.group,
            resolution=parent_item.resolution,
            source=parent_item.source,
            video_codec=parent_item.video_codec,
            audio_codec=parent_item.audio_codec,
            season=season_name,
            path=path
        )

        # Check for [Airing]
        is_airing_tag_found = any(tag.lower() == "airing" for tag in tags)

        if is_airing_tag_found:
            new_item.is_airing = True
            new_item.resolution = "Airing"
            new_item.source = "Airing"
            new_item.video_codec = "Airing"
            new_item.audio_codec = "Airing"
        else:
            # Apply overrides based on heuristics
            for tag in tags:
                if MediaParser.RES_REGEX.search(tag):
                    new_item.resolution = tag
                elif MediaParser.SOURCE_REGEX.search(tag):
                    new_item.source = tag
                elif MediaParser.VIDEO_REGEX.search(tag):
                    new_item.video_codec = tag
                elif MediaParser.AUDIO_REGEX.search(tag):
                    new_item.audio_codec = tag
                # If nothing matches, it might be Group or just unknown.
                # We assume Group isn't overridden usually unless it matches nothing else?
                # Or if it's the first tag and doesn't match others?
                # User example: Season 03 [WEB-DL][H.264][AAC2.0] -> Source, Video, Audio.
                # So no group override in example. We'll skip unknown tags or log them.

        return new_item

class LibraryScanner:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def scan(self) -> List[MediaItem]:
        items = []
        if not os.path.isdir(self.root_path):
            return items

        # Iterate only top level directories first
        try:
            for entry in os.scandir(self.root_path):
                if entry.is_dir():
                    # Parse as a potential show/movie
                    parent_item = MediaParser.parse_root_folder(entry.name, entry.path)

                    # Check for seasons
                    has_seasons = False
                    try:
                        sub_entries = list(os.scandir(entry.path))
                        # Sort to ensure consistent order (optional)
                        sub_entries.sort(key=lambda x: x.name)

                        for sub in sub_entries:
                            if sub.is_dir() and sub.name.lower().startswith("season"):
                                has_seasons = True
                                season_item = MediaParser.parse_season_override(sub.name, parent_item, sub.path)
                                items.append(season_item)
                    except OSError:
                        pass # Permission issue or not a dir

                    # If no seasons found, add the parent item itself as the entry (Movie or Show without season folders)
                    if not has_seasons:
                        # Only add if it's not empty? Or assume valid?
                        items.append(parent_item)

        except OSError as e:
            print(f"Error scanning directory: {e}")

        return items
