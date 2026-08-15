from pathlib import Path

from yomikoe.audio.models import AudioMetadata, LoadedAudio
from yomikoe.engines import (
    DummyTranscriptionEngine,
    TranscriptionProgress,
)


def make_loaded_audio(duration: float | None) -> LoadedAudio:
    metadata = AudioMetadata(
        filename="sample.mp3",
        path=str(Path("sample.mp3").resolve()),
        size_bytes=100,
        extension=".mp3",
        duration_seconds=duration,
    )

    return LoadedAudio(
        path=Path("sample.mp3"),
        metadata=metadata,
    )


def test_dummy_engine_transcribes_audio() -> None:
    engine = DummyTranscriptionEngine()
    audio = make_loaded_audio(10.0)

    result = engine.transcribe(audio)

    assert result.language == "ja"
    assert len(result.segments) == 1

    segment = result.segments[0]

    assert segment.start == 0.0
    assert segment.end == 10.0
    assert segment.text == "[Dummy transcription]"


def test_dummy_engine_handles_unknown_duration() -> None:
    engine = DummyTranscriptionEngine()
    audio = make_loaded_audio(None)

    result = engine.transcribe(audio)

    segment = result.segments[0]

    assert segment.start == 0.0
    assert segment.end == 0.0
    assert segment.text == "[Dummy transcription]"


def test_dummy_engine_reports_progress() -> None:
    engine = DummyTranscriptionEngine()
    audio = make_loaded_audio(10.0)

    progress_updates: list[TranscriptionProgress] = []

    def progress_callback(progress: TranscriptionProgress) -> None:
        progress_updates.append(progress)

    engine.transcribe(
        audio,
        progress_callback=progress_callback,
    )

    assert len(progress_updates) == 1

    progress = progress_updates[0]

    assert progress.current_seconds == 10.0
    assert progress.total_seconds == 10.0


def test_dummy_engine_does_not_report_progress_without_duration() -> None:
    engine = DummyTranscriptionEngine()
    audio = make_loaded_audio(None)

    progress_updates: list[TranscriptionProgress] = []

    def progress_callback(progress: TranscriptionProgress) -> None:
        progress_updates.append(progress)

    engine.transcribe(
        audio,
        progress_callback=progress_callback,
    )

    assert progress_updates == []
