from pydantic import BaseModel
from typing import Optional, List

class MediaStats(BaseModel):
    group: Optional[str] = None
    resolution: Optional[str] = None
    source: Optional[str] = None
    video_codec: Optional[str] = None
    audio_codec: Optional[str] = None

class MediaItem(BaseModel):
    name: str
    stats: MediaStats
    path: str
    is_season: bool = False
    children: List['MediaItem'] = []
