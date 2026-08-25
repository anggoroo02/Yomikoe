import pytest

from yomikoe.engines import TranscriptionResult, TranscriptionSegment
from yomikoe.subtitle import generate_subtitle, write_srt
from yomikoe.subtitle.models import Subtitle, SubtitleCue
from yomikoe.subtitle.writers.srt import format_timestamp


def test_generate_subtitle_creates_subtitle_model() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=0.0,
                end=1.5,
                text="こんにちは",
            ),
            TranscriptionSegment(
                start=2.0,
                end=3.5,
                text="世界",
            ),
        ],
    )

    subtitle = generate_subtitle(transcription)

    assert subtitle.language == "ja"
    assert len(subtitle.cues) == 2

    assert subtitle.cues[0].text == "こんにちは"
    assert subtitle.cues[1].text == "世界"


def test_write_srt_serializes_subtitle() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=0.0,
                end=1.5,
                text="こんにちは",
            ),
        ],
    )

    subtitle = generate_subtitle(transcription)

    srt = write_srt(subtitle)

    expected = "1\n00:00:00,000 --> 00:00:01,500\nこんにちは\n"

    assert srt.strip() == expected.strip()


def test_generate_subtitle_handles_empty_transcription() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[],
    )

    subtitle = generate_subtitle(transcription)

    assert subtitle.language == "ja"
    assert subtitle.cues == []

    assert write_srt(subtitle) == ""


def test_write_srt_serializes_multiple_cues() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=0.0,
                end=1.5,
                text="こんにちは",
            ),
            TranscriptionSegment(
                start=2.25,
                end=3.75,
                text="世界",
            ),
        ],
    )

    subtitle = generate_subtitle(transcription)

    srt = write_srt(subtitle)

    expected = (
        "1\n"
        "00:00:00,000 --> 00:00:01,500\n"
        "こんにちは\n"
        "\n"
        "2\n"
        "00:00:02,250 --> 00:00:03,750\n"
        "世界\n"
    )

    assert srt == expected


def test_write_srt_formats_milliseconds() -> None:
    transcription = TranscriptionResult(
        language="ja",
        segments=[
            TranscriptionSegment(
                start=1.234,
                end=5.678,
                text="テスト",
            ),
        ],
    )

    subtitle = generate_subtitle(transcription)

    assert write_srt(subtitle) == ("1\n00:00:01,234 --> 00:00:05,678\nテスト\n")


def test_subtitle_cue_accepts_valid_values() -> None:
    cue = SubtitleCue(
        start=0.0,
        end=1.5,
        text="こんにちは",
    )

    assert cue.start == 0.0
    assert cue.end == 1.5
    assert cue.text == "こんにちは"


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (-1.0, 1.0),
        (0.0, 0.0),
        (2.0, 1.0),
        (float("nan"), 1.0),
        (0.0, float("nan")),
        (float("inf"), 1.0),
        (0.0, float("inf")),
        (-float("inf"), 1.0),
        (0.0, -float("inf")),
    ],
)
def test_subtitle_cue_rejects_invalid_timestamps(
    start: float,
    end: float,
) -> None:
    with pytest.raises(ValueError):
        SubtitleCue(
            start=start,
            end=end,
            text="こんにちは",
        )


@pytest.mark.parametrize("text", ["", " ", "   ", "\t", "\n"])
def test_subtitle_cue_rejects_empty_or_whitespace_text(
    text: str,
) -> None:
    with pytest.raises(ValueError):
        SubtitleCue(
            start=0.0,
            end=1.0,
            text=text,
        )


@pytest.mark.parametrize("text", [None, 123, object()])
def test_subtitle_cue_rejects_non_string_text(
    text: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        SubtitleCue(
            start=0.0,
            end=1.0,
            text=text,  # type: ignore[arg-type]
        )


def test_subtitle_accepts_valid_values() -> None:
    cues = [
        SubtitleCue(
            start=0.0,
            end=1.0,
            text="こんにちは",
        ),
        SubtitleCue(
            start=1.0,
            end=2.0,
            text="世界",
        ),
    ]

    subtitle = Subtitle(
        language="ja",
        cues=cues,
    )

    assert subtitle.language == "ja"
    assert subtitle.cues == cues


@pytest.mark.parametrize("language", ["", " ", "\t", "\n"])
def test_subtitle_rejects_empty_language(language: str) -> None:
    with pytest.raises(ValueError):
        Subtitle(language=language)


@pytest.mark.parametrize("language", [None, 123, object()])
def test_subtitle_rejects_non_string_language(language: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        Subtitle(
            language=language,  # type: ignore[arg-type]
        )


def test_subtitle_rejects_out_of_order_cues() -> None:
    cues = [
        SubtitleCue(
            start=2.0,
            end=3.0,
            text="世界",
        ),
        SubtitleCue(
            start=0.0,
            end=1.0,
            text="こんにちは",
        ),
    ]

    with pytest.raises(ValueError):
        Subtitle(
            language="ja",
            cues=cues,
        )


def test_subtitle_accepts_empty_cues() -> None:
    subtitle = Subtitle(language="ja")

    assert subtitle.cues == []


@pytest.mark.parametrize(
    ("start", "end", "expected_start", "expected_end"),
    [
        (1.2344, 2.3454, "00:00:01,234", "00:00:02,345"),
        (1.2345, 2.3455, "00:00:01,235", "00:00:02,346"),
        (1.2346, 2.3456, "00:00:01,235", "00:00:02,346"),
        (59.9994, 60.9994, "00:00:59,999", "00:01:00,999"),
        (59.9995, 60.9995, "00:01:00,000", "00:01:01,000"),
    ],
)
def test_write_srt_rounds_timestamps_to_nearest_millisecond(
    start: float,
    end: float,
    expected_start: str,
    expected_end: str,
) -> None:
    subtitle = Subtitle(
        language="ja",
        cues=[
            SubtitleCue(
                start=start,
                end=end,
                text="テスト",
            ),
        ],
    )

    assert write_srt(subtitle) == (f"1\n{expected_start} --> {expected_end}\nテスト\n")


@pytest.mark.parametrize(
    ("start", "end", "expected_start", "expected_end"),
    [
        (0.0, 0.001, "00:00:00,000", "00:00:00,001"),
        (59.999, 60.0, "00:00:59,999", "00:01:00,000"),
        (3599.999, 3600.0, "00:59:59,999", "01:00:00,000"),
        (86399.999, 86400.0, "23:59:59,999", "24:00:00,000"),
    ],
)
def test_write_srt_handles_timestamp_boundary_values(
    start: float,
    end: float,
    expected_start: str,
    expected_end: str,
) -> None:
    subtitle = Subtitle(
        language="ja",
        cues=[
            SubtitleCue(
                start=start,
                end=end,
                text="境界値",
            ),
        ],
    )

    assert write_srt(subtitle) == (f"1\n{expected_start} --> {expected_end}\n境界値\n")


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (-0.001, 1.0),
        (0.0, 0.0),
        (1.0, 0.999),
        (float("nan"), 1.0),
        (0.0, float("nan")),
        (float("inf"), 1.0),
        (0.0, float("inf")),
        (-float("inf"), 1.0),
        (0.0, -float("inf")),
    ],
)
def test_write_srt_rejects_invalid_cues(
    start: float,
    end: float,
) -> None:
    with pytest.raises(ValueError):
        subtitle = Subtitle(
            language="ja",
            cues=[
                SubtitleCue(
                    start=start,
                    end=end,
                    text="不正な字幕",
                ),
            ],
        )

        write_srt(subtitle)


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0.0, "00:00:00,000"),
        (1.234, "00:00:01,234"),
        (1.2345, "00:00:01,235"),
        (59.9995, "00:01:00,000"),
        (60.0, "00:01:00,000"),
        (3661.234, "01:01:01,234"),
    ],
)
def test_format_timestamp_rounds_half_up(
    seconds: float,
    expected: str,
) -> None:
    assert format_timestamp(seconds) == expected


@pytest.mark.parametrize(
    "seconds",
    [
        -1.0,
        float("nan"),
        float("inf"),
        -float("inf"),
    ],
)
def test_format_timestamp_rejects_invalid_values(seconds: float) -> None:
    with pytest.raises(ValueError):
        format_timestamp(seconds)
