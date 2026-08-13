from pathlib import Path

from yomikoe.engines import DummyTranscriptionEngine
from yomikoe.pipeline import transcribe_audio


def test_pipeline_uses_replaceable_transcription_engine(
    tmp_path: Path,
) -> None:
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"dummy audio")

    engine = DummyTranscriptionEngine()

    result = transcribe_audio(
        audio_file,
        engine,
    )

    assert result["audio"]["path"] == audio_file
    assert result["transcription"].language == "ja"
    assert len(result["transcription"].segments) == 1

    segment = result["transcription"].segments[0]

    assert segment.start == 0.0
    assert segment.end == 0.0
    assert segment.text == "[Dummy transcription]"
