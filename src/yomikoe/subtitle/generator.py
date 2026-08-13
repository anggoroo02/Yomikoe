from yomikoe.engines import (
    TranscriptionResult,
)
from yomikoe.subtitle.models import (
    Subtitle,
    SubtitleCue,
)


def generate_subtitle(
    transcription: TranscriptionResult,
) -> Subtitle:
    """Convert transcription result into subtitle model."""

    return Subtitle(
        language=transcription.language,
        cues=[
            SubtitleCue(
                start=segment.start,
                end=segment.end,
                text=segment.text.strip(),
            )
            for segment in transcription.segments
        ],
    )
