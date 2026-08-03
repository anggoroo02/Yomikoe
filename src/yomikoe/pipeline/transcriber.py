from pathlib import Path

from yomikoe.audio import load_audio
from yomikoe.engines import (
    DummyTranscriptionEngine,
    TranscriptionResult,
)
from yomikoe.pipeline.models import PipelineResult


def transcribe(audio_file: Path) -> TranscriptionResult:
    """Run the transcription pipeline."""

    loaded_audio = load_audio(audio_file)

    engine = DummyTranscriptionEngine()

    return engine.transcribe(loaded_audio)

def transcribe_audio(audio_file: Path) -> PipelineResult:
    """Run the transcription pipeline."""

    loaded_audio = load_audio(audio_file)

    engine = DummyTranscriptionEngine()

    transcription = engine.transcribe(loaded_audio)

    return PipelineResult(
        audio=loaded_audio,
        transcription=transcription,
    )