from typing import TypedDict

class AudioMetadata(TypedDict):
    filename: str
    path: str
    size_bytes: int
    extension: str
    duration_seconds: float | None