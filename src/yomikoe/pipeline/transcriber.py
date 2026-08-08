from collections.abc import Callable
from pathlib import Path

from yomikoe.audio import load_audio
from yomikoe.engines import (
    TranscriptionEngine,
    TranscriptionProgress,
    TranscriptionResult,
)
from yomikoe.pipeline.models import PipelineResult


def transcribe(
    audio_file: Path,
    engine: TranscriptionEngine,
) -> TranscriptionResult:
    loaded_audio = load_audio(audio_file)

    return engine.transcribe(loaded_audio)


def transcribe_audio(
    audio_file: Path,
    engine: TranscriptionEngine,
    progress_callback: Callable[[TranscriptionProgress], None] | None = None,
) -> PipelineResult:
    loaded_audio = load_audio(audio_file)

    transcription = engine.transcribe(
        loaded_audio,
        progress_callback=progress_callback,
    )

    return PipelineResult(
        audio=loaded_audio,
        transcription=transcription,
    )
