from pathlib import Path

from yomikoe.audio import load_audio
from yomikoe.engines import (
    TranscriptionEngine,
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
) -> PipelineResult:
    loaded_audio = load_audio(audio_file)

    transcription = engine.transcribe(
        loaded_audio,
    )

    return PipelineResult(
        audio=loaded_audio,
        transcription=transcription,
    )