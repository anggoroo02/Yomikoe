from yomikoe.engines import TranscriptionResult, TranscriptionSegment
from yomikoe.subtitle import generate_subtitle, write_srt


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
