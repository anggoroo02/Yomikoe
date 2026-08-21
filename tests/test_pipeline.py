from pathlib import Path

from yomikoe.engines import TranscriptionProgress
from yomikoe.pipeline import transcribe_audio
from yomikoe.pipeline.transcriber import transcribe
from yomikoe.postprocessing import IdentityTranscriptionProcessor


def test_transcribe_audio_returns_pipeline_result(
    tmp_path: Path,
    spy_engine,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    result = transcribe_audio(
        audio_file,
        spy_engine,
    )

    assert result["audio"] is spy_engine.received_audio
    assert result["transcription"] is spy_engine.result


def test_transcribe_audio_forwards_progress_callback(
    tmp_path: Path,
    spy_engine,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    def progress_callback(progress: TranscriptionProgress) -> None:
        pass

    transcribe_audio(
        audio_file,
        spy_engine,
        progress_callback=progress_callback,
    )

    assert spy_engine.received_callback is progress_callback


def test_transcribe_audio_uses_identity_processor_by_default(
    tmp_path: Path,
    spy_engine,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    result = transcribe_audio(
        audio_file,
        spy_engine,
    )

    assert result["transcription"] is spy_engine.result


def test_transcribe_audio_applies_processor(
    tmp_path: Path,
    spy_engine,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    processor = IdentityTranscriptionProcessor()

    result = transcribe_audio(
        audio_file,
        spy_engine,
        processor=processor,
    )

    assert result["transcription"] is spy_engine.result


def test_transcribe_returns_engine_result(
    tmp_path: Path,
    spy_engine,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    result = transcribe(
        audio_file,
        spy_engine,
    )

    assert result is spy_engine.result
    assert spy_engine.received_audio is not None
    assert spy_engine.received_audio["path"] == audio_file
