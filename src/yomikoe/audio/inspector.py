from pathlib import Path


def inspect_audio(audio_file: Path) -> dict[str, str | int]:
    """Inspect basic information about an audio file."""

    return {
        "filename": audio_file.name,
        "path": str(audio_file.resolve()),
        "size_bytes": audio_file.stat().st_size,
        "extension": audio_file.suffix.lower(),
    }