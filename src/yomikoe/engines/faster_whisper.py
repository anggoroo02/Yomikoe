from collections.abc import Callable

from faster_whisper import WhisperModel

from yomikoe.audio import LoadedAudio
from yomikoe.engines.models import (
    TranscriptionProgress,
    TranscriptionResult,
    TranscriptionSegment,
)


class FasterWhisperEngine:
    """Transcription engine backed by Faster-Whisper."""

    def __init__(
        self,
        model_name: str = "small",
        device: str = "auto",
        compute_type: str = "default",
    ) -> None:
        self._model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(
        self,
        loaded_audio: LoadedAudio,
        progress_callback: Callable[
            [TranscriptionProgress],
            None,
        ]
        | None = None,
    ) -> TranscriptionResult:
        audio_path = str(loaded_audio["path"])
        duration = loaded_audio["metadata"]["duration_seconds"]

        segments, info = self._model.transcribe(audio_path)

        result_segments = []

        for segment in segments:
            result_segments.append(
                TranscriptionSegment(
                    start=segment.start,
                    end=segment.end,
                    text=segment.text.strip(),
                )
            )

            if progress_callback is not None and duration is not None:
                progress_callback(
                    TranscriptionProgress(
                        current_seconds=segment.end,
                        total_seconds=duration,
                    )
                )

        return TranscriptionResult(
            language=info.language,
            segments=result_segments,
        )
