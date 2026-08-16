from collections.abc import Callable

from yomikoe.audio import LoadedAudio
from yomikoe.engines import (
    DummyTranscriptionEngine,
    TranscriptionProgress,
)


def test_dummy_engine_transcribes_audio(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    engine = DummyTranscriptionEngine()
    audio = loaded_audio_factory(10.0)

    result = engine.transcribe(audio)

    assert result.language == "ja"
    assert len(result.segments) == 1

    segment = result.segments[0]

    assert segment.start == 0.0
    assert segment.end == 10.0
    assert segment.text == "[Dummy transcription]"


def test_dummy_engine_handles_unknown_duration(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    engine = DummyTranscriptionEngine()
    audio = loaded_audio_factory(None)

    result = engine.transcribe(audio)

    segment = result.segments[0]

    assert segment.start == 0.0
    assert segment.end == 0.0
    assert segment.text == "[Dummy transcription]"


def test_dummy_engine_reports_progress(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    engine = DummyTranscriptionEngine()
    audio = loaded_audio_factory(10.0)

    progress_updates: list[TranscriptionProgress] = []

    def progress_callback(progress: TranscriptionProgress) -> None:
        progress_updates.append(progress)

    engine.transcribe(
        audio,
        progress_callback=progress_callback,
    )

    assert progress_updates == [
        TranscriptionProgress(
            current_seconds=10.0,
            total_seconds=10.0,
        )
    ]


def test_dummy_engine_does_not_report_progress_without_duration(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    engine = DummyTranscriptionEngine()
    audio = loaded_audio_factory(None)

    progress_updates: list[TranscriptionProgress] = []

    def progress_callback(progress: TranscriptionProgress) -> None:
        progress_updates.append(progress)

    engine.transcribe(
        audio,
        progress_callback=progress_callback,
    )

    assert progress_updates == []
