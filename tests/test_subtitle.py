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

    expected = (
        "1\n"
        "00:00:00,000 --> 00:00:01,500\n"
        "こんにちは\n"
    )

    assert srt.strip() == expected.strip()