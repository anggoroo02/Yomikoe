from yomikoe.engines import TranscriptionResult, TranscriptionSegment


class WhitespaceProcessor:
    """Normalize whitespace in transcription segments."""

    def process(self, transcription: TranscriptionResult) -> TranscriptionResult:
        segments = [
            TranscriptionSegment(
                start=segment.start,
                end=segment.end,
                text=" ".join(segment.text.split()),
            )
            for segment in transcription.segments
        ]

        return TranscriptionResult(
            language=transcription.language,
            segments=segments,
        )


__all__ = ["WhitespaceProcessor"]
