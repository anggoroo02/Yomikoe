from collections.abc import Callable
from pathlib import Path

from yomikoe.audio import LoadedAudio
from yomikoe.engines import (
    TranscriptionProgress,
    TranscriptionResult,
    TranscriptionSegment,
)
from yomikoe.pipeline import transcribe_audio


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


def test_transcribe_audio_returns_pipeline_result(
    tmp_path: Path,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    engine = SpyTranscriptionEngine()

    result = transcribe_audio(
        audio_file,
        engine,
    )

    assert result["audio"] is engine.received_audio
    assert result["transcription"] is engine.result


def test_transcribe_audio_forwards_progress_callback(
    tmp_path: Path,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    engine = SpyTranscriptionEngine()

    def progress_callback(progress: TranscriptionProgress) -> None:
        pass

    transcribe_audio(
        audio_file,
        engine,
        progress_callback=progress_callback,
    )

    assert engine.received_callback is progress_callback
