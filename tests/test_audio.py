from pathlib import Path

import pytest

from yomikoe.audio import (
    UnsupportedAudioFormatError,
    inspect_audio,
    load_audio,
)


@pytest.mark.parametrize(
    "extension",
    [".wav", ".mp3", ".m4a", ".flac", ".ogg"],
)
def test_load_audio_accepts_supported_formats(
    tmp_path: Path,
    extension: str,
) -> None:
    audio_file = tmp_path / f"sample{extension}"
    audio_file.write_bytes(b"dummy audio")

    result = load_audio(audio_file)

    assert result["path"] == audio_file
    assert result["metadata"]["filename"] == f"sample{extension}"
    assert result["metadata"]["extension"] == extension


def test_load_audio_accepts_uppercase_extension(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.MP3"
    audio_file.write_bytes(b"dummy audio")

    result = load_audio(audio_file)

    assert result["path"] == audio_file
    assert result["metadata"]["extension"] == ".mp3"


def test_load_audio_rejects_unsupported_format(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.txt"
    audio_file.write_text("not audio")

    with pytest.raises(
        UnsupportedAudioFormatError,
        match=r"Unsupported audio format: \.txt",
    ):
        load_audio(audio_file)


def test_inspect_audio_returns_basic_metadata(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    result = inspect_audio(audio_file)

    assert result["filename"] == "sample.mp3"
    assert result["path"] == str(audio_file.resolve())
    assert result["size_bytes"] == len(b"dummy audio")
    assert result["extension"] == ".mp3"
    assert result["duration_seconds"] is None
