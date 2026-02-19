import os
import re
from typing import List, Optional
from .models import MediaItem, MediaStats

# Regex Patterns
RESOLUTION_PATTERN = re.compile(r'\b(\d{3,4}p|4K|2160p|UHD|SD|HD)\b', re.IGNORECASE)
VIDEO_CODEC_PATTERN = re.compile(r'\b(H\.?264|H\.?265|x264|x265|HEVC|AV1|VP9|MPEG-?4|DivX|XviD|ProRes)\b', re.IGNORECASE)
# Relaxed Audio Codec Pattern to handle versions like AAC2.0, OPUS2.0
AUDIO_CODEC_PATTERN = re.compile(r'\b(AAC|DTS|DTS-HD|AC3|EAC3|FLAC|MP3|OPUS|TrueHD|Atmos|PCM|Vorbis)', re.IGNORECASE)
SOURCE_PATTERN = re.compile(r'\b(BD|BluRay|WEB-DL|WEBRip|DVD|HDTV|Remux|Encode|ISO)\b', re.IGNORECASE)

def parse_stats(bracket_contents: List[str]) -> MediaStats:
    stats = MediaStats()

    # We make a copy to remove items as we identify them, to help identify Group
    remaining = bracket_contents[:]

    for content in bracket_contents:
        # Check Resolution
        if not stats.resolution and RESOLUTION_PATTERN.search(content):
            stats.resolution = content
            if content in remaining: remaining.remove(content)
            continue

        # Check Source
        if not stats.source and SOURCE_PATTERN.search(content):
            stats.source = content
            if content in remaining: remaining.remove(content)
            continue

        # Check Video Codec
        if not stats.video_codec and VIDEO_CODEC_PATTERN.search(content):
            stats.video_codec = content
            if content in remaining: remaining.remove(content)
            continue

        # Check Audio Codec
        if not stats.audio_codec and AUDIO_CODEC_PATTERN.search(content):
            stats.audio_codec = content
            if content in remaining: remaining.remove(content)
            continue

    # Heuristic for Group: Usually the first item, or whatever is left.
    # User example: [Zaki][1080p]...
    # If "Zaki" didn't match anything, it's likely the group.
    if remaining:
        stats.group = remaining[0] # Assume the first unidentified bracket is the group

    return stats

def parse_folder_name(folder_name: str) -> tuple[str, MediaStats]:
    # Extract content in brackets
    brackets = re.findall(r'\[(.*?)\]', folder_name)

    # Extract Name (everything before first bracket)
    name_match = re.split(r'\[', folder_name, 1)
    name = name_match[0].strip() if name_match else folder_name.strip()

    stats = parse_stats(brackets)
    return name, stats

def merge_stats(base: MediaStats, override: MediaStats) -> MediaStats:
    return MediaStats(
        group=override.group or base.group,
        resolution=override.resolution or base.resolution,
        source=override.source or base.source,
        video_codec=override.video_codec or base.video_codec,
        audio_codec=override.audio_codec or base.audio_codec,
    )

def scan_library(library_path: str) -> List[MediaItem]:
    media_items = []

    if not os.path.exists(library_path):
        return []

    for entry_name in os.listdir(library_path):
        entry_path = os.path.join(library_path, entry_name)

        if os.path.isdir(entry_path):
            name, stats = parse_folder_name(entry_name)

            # Check for seasons
            children = []
            try:
                sub_entries = sorted(os.listdir(entry_path))
                for sub_name in sub_entries:
                    sub_path = os.path.join(entry_path, sub_name)
                    if os.path.isdir(sub_path) and (sub_name.lower().startswith("season") or sub_name.lower().startswith("specials")):
                        sub_name_parsed, sub_stats_raw = parse_folder_name(sub_name)
                        # Inherit/Override stats
                        merged_stats = merge_stats(stats, sub_stats_raw)
                        children.append(MediaItem(
                            name=sub_name_parsed, # e.g., "Season 03"
                            stats=merged_stats,
                            path=sub_path,
                            is_season=True
                        ))
            except OSError:
                pass # Permission denied or other error

            media_items.append(MediaItem(
                name=name,
                stats=stats,
                path=entry_path,
                children=children
            ))

    return media_items
