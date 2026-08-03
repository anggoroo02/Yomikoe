from pathlib import Path

from yomikoe.audio.exceptions import UnsupportedAudioFormatError
from yomikoe.audio.inspector import inspect_audio
from yomikoe.audio.models import LoadedAudio

SUPPORTED_AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
    ".ogg",
}

def supported_audio_formats() -> str:
    return "\n".join(
        f"- {extension}" for extension in SUPPORTED_AUDIO_EXTENSIONS
    )


def load_audio(audio_file: Path) -> LoadedAudio:
    """Load an audio file and its metadata."""
    extension = audio_file.suffix.lower()

    if extension not in SUPPORTED_AUDIO_EXTENSIONS:
        supported_formats = "\n".join(
            f"- {ext}" for ext in sorted(SUPPORTED_AUDIO_EXTENSIONS)
        )

        raise UnsupportedAudioFormatError(
            f"Unsupported audio format: {extension}\n\n"
            f"Supported formats:\n"
            f"{supported_audio_formats()}"
        )

    return LoadedAudio(
        path=audio_file,
        metadata=inspect_audio(audio_file),
    )