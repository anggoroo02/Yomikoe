from typing import Protocol

from yomikoe.engines import TranscriptionResult


class TranscriptionProcessor(Protocol):
    """Interface for post-processing transcription results."""

    def process(
        self,
        transcription: TranscriptionResult,
    ) -> TranscriptionResult:
        """Process a transcription result."""
        ...
