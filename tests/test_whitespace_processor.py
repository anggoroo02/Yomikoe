from yomikoe.engines import TranscriptionResult, TranscriptionSegment
from yomikoe.postprocessing.whitespace import WhitespaceProcessor


def test_whitespace_processor_normalizes_segment_text() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=0.0,
                end=1.0,
                text="  こんにちは   世界  ",
            ),
        ],
    )

    result = WhitespaceProcessor().process(transcription)

    assert result.segments[0].text == "こんにちは 世界"


def test_whitespace_processor_preserves_metadata() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=1.5,
                end=3.0,
                text="  こんにちは  ",
            ),
        ],
    )

    result = WhitespaceProcessor().process(transcription)

    assert result.language == "ja"
    assert result.segments[0].start == 1.5
    assert result.segments[0].end == 3.0


def test_whitespace_processor_does_not_modify_original() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=0.0,
                end=1.0,
                text="  こんにちは   世界  ",
            ),
        ],
    )

    WhitespaceProcessor().process(transcription)

    assert transcription.segments[0].text == "  こんにちは   世界  "
