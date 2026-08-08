from collections.abc import Callable

from yomikoe.audio.models import LoadedAudio
from yomikoe.engines.models import (
    TranscriptionProgress,
    TranscriptionResult,
    TranscriptionSegment,
)


class DummyTranscriptionEngine:
    """Dummy transcription engine used for development."""

    def transcribe(
        self,
        loaded_audio: LoadedAudio,
        progress_callback: Callable[
            [TranscriptionProgress],
            None,
        ]
        | None = None,
    ) -> TranscriptionResult:
        duration = loaded_audio["metadata"]["duration_seconds"]
        segment_end = duration or 0.0

        segment = TranscriptionSegment(
            start=0.0,
            end=segment_end,
            text="[Dummy transcription]",
        )

        if progress_callback is not None and duration is not None:
            progress_callback(
                TranscriptionProgress(
                    current_seconds=duration,
                    total_seconds=duration,
                )
            )

        return TranscriptionResult(
            language="ja",
            segments=[segment],
        )
