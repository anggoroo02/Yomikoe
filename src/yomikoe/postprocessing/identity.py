from yomikoe.engines import TranscriptionResult


class IdentityTranscriptionProcessor:
    """Return transcription results unchanged."""

    def process(
        self,
        transcription: TranscriptionResult,
    ) -> TranscriptionResult:
        """Return the transcription without modification."""
        return transcription
