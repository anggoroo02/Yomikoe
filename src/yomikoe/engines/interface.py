from typing import Protocol

from yomikoe.audio import LoadedAudio

from .models import TranscriptionResult


class TranscriptionEngine(Protocol):
    """Interface for transcription engines."""

    def transcribe(
        self,
        audio: LoadedAudio,
    ) -> TranscriptionResult:
        """Transcribe an audio file."""
        ...
