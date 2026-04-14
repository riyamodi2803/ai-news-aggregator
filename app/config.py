from app.settings import settings
from app.sources.registry import DEFAULT_SOURCES

# Backward-compatible module for any legacy imports.
DATABASE_URL = None
YOUTUBE_CHANNELS = [
    source["channel_id"]
    for source in DEFAULT_SOURCES
    if source.get("source_type") == "youtube" and source.get("channel_id")
]