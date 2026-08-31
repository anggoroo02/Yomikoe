from pathlib import Path

from yomikoe.engines import DummyTranscriptionEngine
from yomikoe.pipeline import transcribe_audio
from yomikoe.subtitle import generate_subtitle, write_srt


def test_transcription_pipeline_generates_srt(tmp_path: Path) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    result = transcribe_audio(
        audio_file,
        DummyTranscriptionEngine(),
    )

    transcription = result["transcription"]

    assert transcription.language == "ja"
    assert len(transcription.segments) == 1

    subtitle = generate_subtitle(transcription)
    srt = write_srt(subtitle)

    assert srt == ("1\n00:00:00,000 --> 00:00:01,000\n[Dummy transcription]\n")

    output_file = tmp_path / "sample.srt"
    output_file.write_text(srt, encoding="utf-8")

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == srt
