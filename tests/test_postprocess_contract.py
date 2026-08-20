from yomikoe.engines import TranscriptionResult, TranscriptionSegment
from yomikoe.postprocessing import TranscriptionProcessor


class IdentityTranscriptionProcessor:
    """Return the transcription without modification."""

    def process(
        self,
        transcription: TranscriptionResult,
    ) -> TranscriptionResult:
        return transcription


def make_transcription() -> TranscriptionResult:
    return TranscriptionResult(
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
                text="世界です",
            ),
        ],
    )


def test_identity_processor_returns_transcription() -> None:
    transcription = make_transcription()
    processor = IdentityTranscriptionProcessor()

    result = processor.process(transcription)

    assert result is transcription


def test_identity_processor_preserves_transcription() -> None:
    transcription = make_transcription()
    processor = IdentityTranscriptionProcessor()

    result = processor.process(transcription)

    assert result.language == "ja"
    assert len(result.segments) == 2
    assert result.segments[0].start == 0.0
    assert result.segments[0].end == 1.5
    assert result.segments[0].text == "こんにちは"
    assert result.segments[1].start == 1.5
    assert result.segments[1].end == 3.0
    assert result.segments[1].text == "世界です"


def test_identity_processor_satisfies_transcription_processor_contract() -> None:
    processor: TranscriptionProcessor = IdentityTranscriptionProcessor()

    result = processor.process(make_transcription())

    assert isinstance(result, TranscriptionResult)
