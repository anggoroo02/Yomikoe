from faster_whisper import WhisperModel

from yomikoe.audio import LoadedAudio
from yomikoe.engines.models import (
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
        audio: LoadedAudio,
    ) -> TranscriptionResult:
        audio_path = str(audio["path"])

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

        return TranscriptionResult(
            language=info.language,
            segments=result_segments,
        )