import math

import pytest

from yomikoe.engines import TranscriptionResult, TranscriptionSegment


def test_transcription_segment_accepts_valid_values() -> None:
    segment = TranscriptionSegment(
        start=0.0,
        end=1.5,
        text="こんにちは",
    )

    assert segment.start == 0.0
    assert segment.end == 1.5
    assert segment.text == "こんにちは"


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (-1.0, 1.0),
        (0.0, 0.0),
        (2.0, 1.0),
        (math.nan, 1.0),
        (0.0, math.nan),
        (math.inf, 1.0),
        (0.0, math.inf),
        (-math.inf, 1.0),
        (0.0, -math.inf),
    ],
)
def test_transcription_segment_rejects_invalid_timestamps(
    start: float,
    end: float,
) -> None:
    with pytest.raises(ValueError):
        TranscriptionSegment(
            start=start,
            end=end,
            text="こんにちは",
        )


@pytest.mark.parametrize("text", ["", " ", "   ", "\t", "\n"])
def test_transcription_segment_rejects_empty_or_whitespace_text(
    text: str,
) -> None:
    with pytest.raises(ValueError):
        TranscriptionSegment(
            start=0.0,
            end=1.0,
            text=text,
        )


@pytest.mark.parametrize("text", [None, 123, object()])
def test_transcription_segment_rejects_non_string_text(
    text: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        TranscriptionSegment(
            start=0.0,
            end=1.0,
            text=text,  # type: ignore[arg-type]
        )


def test_transcription_result_accepts_valid_values() -> None:
    segments = [
        TranscriptionSegment(
            start=0.0,
            end=1.0,
            text="こんにちは",
        ),
        TranscriptionSegment(
            start=1.0,
            end=2.0,
            text="世界",
        ),
    ]

    result = TranscriptionResult(
        language="ja",
        segments=segments,
    )

    assert result.language == "ja"
    assert result.segments == segments


@pytest.mark.parametrize("language", ["", " ", "\t", "\n"])
def test_transcription_result_rejects_empty_language(
    language: str,
) -> None:
    with pytest.raises(ValueError):
        TranscriptionResult(language=language)


@pytest.mark.parametrize("language", [None, 123, object()])
def test_transcription_result_rejects_non_string_language(
    language: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        TranscriptionResult(
            language=language,  # type: ignore[arg-type]
        )


def test_transcription_result_rejects_out_of_order_segments() -> None:
    segments = [
        TranscriptionSegment(
            start=2.0,
            end=3.0,
            text="世界",
        ),
        TranscriptionSegment(
            start=0.0,
            end=1.0,
            text="こんにちは",
        ),
    ]

    with pytest.raises(ValueError):
        TranscriptionResult(
            language="ja",
            segments=segments,
        )


def test_transcription_result_accepts_empty_segments() -> None:
    result = TranscriptionResult(language="ja")

    assert result.segments == []
