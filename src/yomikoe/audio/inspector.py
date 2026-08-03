from pathlib import Path
from mutagen import File as MutagenFile


def inspect_audio(audio_file: Path) -> dict[str, str | int | float | None]:
    """Inspect basic information about an audio file."""
    audio = None
    duration = None

    try:
        audio = MutagenFile(audio_file)
        if audio is not None and audio.info is not None:
            duration = audio.info.length
    except Exception:
        # TODO: Catch specific Mutagen exceptions instead of Exception.
        pass

    return {
        "filename": audio_file.name,
        "path": str(audio_file.resolve()),
        "size_bytes": audio_file.stat().st_size,
        "extension": audio_file.suffix.lower(),
        "duration_seconds": duration,
    }