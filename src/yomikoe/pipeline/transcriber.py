from pathlib import Path

from yomikoe.audio import load_audio
from yomikoe.engines import (
    DummyTranscriptionEngine,
    TranscriptionResult,
)


def transcribe(audio_file: Path) -> TranscriptionResult:
    """Run the transcription pipeline."""

    loaded_audio = load_audio(audio_file)

    engine = DummyTranscriptionEngine()

    return engine.transcribe(loaded_audio)
