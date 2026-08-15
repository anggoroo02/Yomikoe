from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from yomikoe.cli import app
from yomikoe.engines import (
    TranscriptionEngine,
    TranscriptionProgress,
    TranscriptionResult,
    TranscriptionSegment,
)

runner = CliRunner()


def make_transcription_result() -> TranscriptionResult:
    return TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=0.0,
                end=1.5,
                text="こんにちは",
            )
        ],
    )


def make_pipeline_result(
    audio_file: Path,
    transcription: TranscriptionResult | None = None,
) -> dict:
    return {
        "audio": {
            "path": audio_file,
            "metadata": {
                "filename": audio_file.name,
                "path": str(audio_file.resolve()),
                "size_bytes": audio_file.stat().st_size,
                "extension": audio_file.suffix.lower(),
                "duration_seconds": None,
            },
        },
        "transcription": transcription or make_transcription_result(),
    }


def make_engine() -> MagicMock:
    engine = MagicMock(spec=TranscriptionEngine)
    engine.backend = "cpu"
    return engine


def test_version() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Yomikoe 0.1.0-dev0" in result.stdout


def test_transcribe_rejects_missing_file() -> None:
    result = runner.invoke(
        app,
        ["transcribe", "missing.mp3"],
    )

    assert result.exit_code == 1
    assert "Error: File not found: missing.mp3" in result.stderr


def test_transcribe_rejects_directory(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["transcribe", str(tmp_path)],
    )

    assert result.exit_code == 1
    assert f"Error: Path is not a file: {tmp_path}" in result.stderr


def test_transcribe_rejects_unsupported_format(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.txt"
    audio_file.write_text("not audio")

    with patch("yomikoe.cli.FasterWhisperEngine"):
        result = runner.invoke(
            app,
            ["transcribe", str(audio_file)],
        )

    assert result.exit_code == 1
    assert "Unsupported audio format: .txt" in result.stderr


def test_transcribe_writes_default_output(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    engine = make_engine()
    pipeline_result = make_pipeline_result(audio_file)

    with (
        patch("yomikoe.cli.FasterWhisperEngine", return_value=engine),
        patch(
            "yomikoe.cli.transcribe_audio",
            return_value=pipeline_result,
        ),
    ):
        result = runner.invoke(
            app,
            ["transcribe", str(audio_file)],
        )

    assert result.exit_code == 0

    output_file = tmp_path / "sample.srt"

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == (
        "1\n00:00:00,000 --> 00:00:01,500\nこんにちは\n"
    )

    assert f"Output    : {output_file}" in result.stdout


def test_transcribe_writes_custom_output(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    output_file = tmp_path / "custom.srt"

    engine = make_engine()
    pipeline_result = make_pipeline_result(audio_file)

    with (
        patch("yomikoe.cli.FasterWhisperEngine", return_value=engine),
        patch(
            "yomikoe.cli.transcribe_audio",
            return_value=pipeline_result,
        ),
    ):
        result = runner.invoke(
            app,
            [
                "transcribe",
                str(audio_file),
                "--output",
                str(output_file),
            ],
        )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Output    : {output_file}" in result.stdout


def test_transcribe_creates_nested_output_directory(
    tmp_path: Path,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    output_file = tmp_path / "subtitles" / "japanese" / "result.srt"

    engine = make_engine()
    pipeline_result = make_pipeline_result(audio_file)

    with (
        patch("yomikoe.cli.FasterWhisperEngine", return_value=engine),
        patch(
            "yomikoe.cli.transcribe_audio",
            return_value=pipeline_result,
        ),
    ):
        result = runner.invoke(
            app,
            [
                "transcribe",
                str(audio_file),
                "-o",
                str(output_file),
            ],
        )

    assert result.exit_code == 0
    assert output_file.exists()


def test_transcribe_reports_output_write_error(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    output_file = tmp_path / "result.srt"

    engine = make_engine()
    pipeline_result = make_pipeline_result(audio_file)

    with (
        patch("yomikoe.cli.FasterWhisperEngine", return_value=engine),
        patch(
            "yomikoe.cli.transcribe_audio",
            return_value=pipeline_result,
        ),
        patch(
            "pathlib.Path.write_text",
            side_effect=OSError("permission denied"),
        ),
    ):
        result = runner.invoke(
            app,
            [
                "transcribe",
                str(audio_file),
                "--output",
                str(output_file),
            ],
        )

    assert result.exit_code == 1
    assert "Error: Could not write subtitle file:" in result.stderr
    assert "Reason: permission denied" in result.stderr


def test_transcribe_displays_progress(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    engine = make_engine()
    pipeline_result = make_pipeline_result(audio_file)

    def fake_transcribe_audio(
        audio_file: Path,
        engine: TranscriptionEngine,
        progress_callback: (Callable[[TranscriptionProgress], None] | None) = None,
    ) -> dict:
        assert progress_callback is not None

        progress_callback(
            TranscriptionProgress(
                current_seconds=5.0,
                total_seconds=10.0,
            )
        )

        return pipeline_result

    with (
        patch("yomikoe.cli.FasterWhisperEngine", return_value=engine),
        patch(
            "yomikoe.cli.transcribe_audio",
            side_effect=fake_transcribe_audio,
        ),
    ):
        result = runner.invoke(
            app,
            ["transcribe", str(audio_file)],
        )

    assert result.exit_code == 0
    assert "Transcribing... 50%" in result.stdout


def test_transcribe_verbose_displays_progress_duration(
    tmp_path: Path,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    engine = make_engine()
    pipeline_result = make_pipeline_result(audio_file)

    pipeline_result["audio"]["metadata"]["duration_seconds"] = 10.0

    def fake_transcribe_audio(
        audio_file: Path,
        engine: TranscriptionEngine,
        progress_callback: (Callable[[TranscriptionProgress], None] | None) = None,
    ) -> dict:
        assert progress_callback is not None

        progress_callback(
            TranscriptionProgress(
                current_seconds=5.0,
                total_seconds=10.0,
            )
        )

        return pipeline_result

    with (
        patch("yomikoe.cli.FasterWhisperEngine", return_value=engine),
        patch(
            "yomikoe.cli.transcribe_audio",
            side_effect=fake_transcribe_audio,
        ),
    ):
        result = runner.invoke(
            app,
            [
                "transcribe",
                str(audio_file),
                "--verbose",
            ],
        )

    assert result.exit_code == 0
    assert "Transcribing... 50% | 00:00:05 / 00:00:10" in result.stdout
