from collections.abc import Callable
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from yomikoe.audio import LoadedAudio
from yomikoe.engines import (
    DummyTranscriptionEngine,
    FasterWhisperEngine,
    TranscriptionEngine,
    TranscriptionResult,
    TranscriptionSegment,
)
from yomikoe.engines.backend import ComputeBackend


def make_loaded_audio(tmp_path: Path) -> LoadedAudio:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    return LoadedAudio(
        path=audio_file,
        metadata={
            "filename": "sample.mp3",
            "path": str(audio_file.resolve()),
            "size_bytes": len(b"dummy audio"),
            "extension": ".mp3",
            "duration_seconds": 10.0,
        },
    )


def make_dummy_engine() -> TranscriptionEngine:
    return DummyTranscriptionEngine()


def make_faster_whisper_engine() -> TranscriptionEngine:
    model = Mock()
    model.transcribe.return_value = (
        [
            Mock(
                start=0.0,
                end=1.5,
                text="こんにちは",
            )
        ],
        Mock(language="ja"),
    )

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            return FasterWhisperEngine(
                backend=ComputeBackend.CPU,
            )


@pytest.mark.parametrize(
    "engine_factory",
    [
        make_dummy_engine,
        make_faster_whisper_engine,
    ],
    ids=[
        "dummy",
        "faster-whisper",
    ],
)
def test_engine_contract_returns_transcription_result(
    tmp_path: Path,
    engine_factory: Callable[[], TranscriptionEngine],
) -> None:
    engine = engine_factory()

    result = engine.transcribe(
        make_loaded_audio(tmp_path),
    )

    assert isinstance(result, TranscriptionResult)
    assert isinstance(result.language, str)

    for segment in result.segments:
        assert isinstance(segment, TranscriptionSegment)


@pytest.mark.parametrize(
    "engine_factory",
    [
        make_dummy_engine,
        make_faster_whisper_engine,
    ],
    ids=[
        "dummy",
        "faster-whisper",
    ],
)
def test_engine_contract_accepts_progress_callback(
    tmp_path: Path,
    engine_factory: Callable[[], TranscriptionEngine],
) -> None:
    engine = engine_factory()

    result = engine.transcribe(
        make_loaded_audio(tmp_path),
        progress_callback=Mock(),
    )

    assert isinstance(result, TranscriptionResult)
