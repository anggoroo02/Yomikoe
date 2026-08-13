from pathlib import Path

import pytest

from yomikoe.audio import UnsupportedAudioFormatError, load_audio


def test_load_audio_accepts_supported_format(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    result = load_audio(audio_file)

    assert result["path"] == audio_file
    assert result["metadata"]["filename"] == "sample.mp3"
    assert result["metadata"]["extension"] == ".mp3"


def test_load_audio_rejects_unsupported_format(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.txt"
    audio_file.write_text("not audio")

    with pytest.raises(UnsupportedAudioFormatError):
        load_audio(audio_file)
