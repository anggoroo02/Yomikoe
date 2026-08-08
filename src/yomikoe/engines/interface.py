from collections.abc import Callable
from typing import Protocol

from yomikoe.audio import LoadedAudio

from .models import TranscriptionProgress, TranscriptionResult


class TranscriptionEngine(Protocol):
    """Interface for transcription engines."""

    def transcribe(
        self,
        loaded_audio: LoadedAudio,
        progress_callback: Callable[
            [TranscriptionProgress],
            None,
        ]
        | None = None,
    ) -> TranscriptionResult:
        """Transcribe loaded audio into a transcription result."""
        ...
