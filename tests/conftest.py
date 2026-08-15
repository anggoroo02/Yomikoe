from collections.abc import Callable
from pathlib import Path

import pytest

from yomikoe.audio import LoadedAudio
from yomikoe.audio.models import AudioMetadata
from yomikoe.engines import (
    TranscriptionProgress,
    TranscriptionResult,
    TranscriptionSegment,
)


@pytest.fixture
def loaded_audio_factory(
    tmp_path: Path,
) -> Callable[[float | None], LoadedAudio]:
    def factory(duration_seconds: float | None = 10.0) -> LoadedAudio:
        audio_file = tmp_path / "sample.mp3"
        audio_file.write_bytes(b"dummy audio")

        metadata = AudioMetadata(
            filename="sample.mp3",
            path=str(audio_file.resolve()),
            size_bytes=len(b"dummy audio"),
            extension=".mp3",
            duration_seconds=duration_seconds,
        )

        return LoadedAudio(
            path=audio_file,
            metadata=metadata,
        )

    return factory


class SpyTranscriptionEngine:
    """Test double that records how the pipeline invokes the engine."""

    def __init__(self) -> None:
        self.received_audio: LoadedAudio | None = None
        self.received_callback: Callable[[TranscriptionProgress], None] | None = None
        self.result = TranscriptionResult(
            language="ja",
            segments=[
                TranscriptionSegment(
                    start=0.0,
                    end=1.5,
                    text="こんにちは",
                )
            ],
        )

    def transcribe(
        self,
        loaded_audio: LoadedAudio,
        progress_callback: Callable[[TranscriptionProgress], None] | None = None,
    ) -> TranscriptionResult:
        self.received_audio = loaded_audio
        self.received_callback = progress_callback

        return self.result


@pytest.fixture
def spy_engine() -> SpyTranscriptionEngine:
    return SpyTranscriptionEngine()
