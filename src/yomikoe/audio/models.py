from pathlib import Path
from typing import TypedDict


class AudioMetadata(TypedDict):
    filename: str
    path: str
    size_bytes: int
    extension: str
    duration_seconds: float | None


class LoadedAudio(TypedDict):
    path: Path
    metadata: AudioMetadata
