from yomikoe.audio.models import LoadedAudio
from yomikoe.engines.models import (
    TranscriptionResult,
    TranscriptionSegment,
)


class DummyTranscriptionEngine:
    """Dummy transcription engine used for development."""

    def transcribe(
        self,
        audio: LoadedAudio,
    ) -> TranscriptionResult:
        duration = audio["metadata"]["duration_seconds"] or 0.0

        segment = TranscriptionSegment(
            start=0.0,
            end=duration,
            text="[Dummy transcription]",
        )

        return TranscriptionResult(
            language="ja",
            segments=[segment],
        )
