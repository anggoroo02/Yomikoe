from collections.abc import Callable

from faster_whisper import WhisperModel

from yomikoe.audio import LoadedAudio
from yomikoe.engines.backend import (
    ComputeBackend,
    resolve_backend,
)
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
        backend: ComputeBackend = ComputeBackend.AUTO,
        compute_type: str = "default",
        language: str = "ja",
    ) -> None:
        self._model_name = model_name
        self._compute_type = compute_type
        self._language = language
        self._requested_backend = backend

        self._backend = resolve_backend(backend)

        self._model = WhisperModel(
            model_name,
            device=self._backend.value,
            compute_type=compute_type,
        )

    class ComputeBackendError(RuntimeError):
        """Raised when the selected compute backend cannot be used."""

    @property
    def backend(self) -> ComputeBackend:
        """Return the resolved compute backend."""
        return self._backend

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

        try:
            segments, info = self._model.transcribe(
                audio_path,
                language=self._language,
            )
        except RuntimeError:
            if self._requested_backend is not ComputeBackend.AUTO:
                raise

            if self._backend is not ComputeBackend.CUDA:
                raise

            self._backend = ComputeBackend.CPU

            self._model = WhisperModel(
                self._model_name,
                device=ComputeBackend.CPU.value,
                compute_type=self._compute_type,
            )

            segments, info = self._model.transcribe(
                audio_path,
                language=self._language,
            )

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
