from yomikoe.engines import TranscriptionResult, TranscriptionSegment
from yomikoe.postprocessing import IdentityTranscriptionProcessor


def test_identity_processor_returns_transcription_unchanged() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=0.0,
                end=1.5,
                text="こんにちは",
            ),
            TranscriptionSegment(
                start=1.5,
                end=3.0,
                text="世界",
            ),
        ],
    )

    processor = IdentityTranscriptionProcessor()

    result = processor.process(transcription)

    assert result is transcription
