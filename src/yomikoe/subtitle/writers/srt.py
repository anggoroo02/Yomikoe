from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from yomikoe.subtitle.models import Subtitle


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp."""

    try:
        value = Decimal(str(seconds))
    except InvalidOperation, ValueError:
        raise ValueError("timestamp must be finite and non-negative") from None

    if not value.is_finite() or value < 0:
        raise ValueError("timestamp must be finite and non-negative")

    milliseconds = int(
        (value * 1000).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
    )

    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def write_srt(
    subtitle: Subtitle,
) -> str:
    """Convert subtitle model into SRT text."""
    lines: list[str] = []
    for index, cue in enumerate(
        subtitle.cues,
        start=1,
    ):
        lines.append(str(index))
        lines.append(f"{format_timestamp(cue.start)} --> {format_timestamp(cue.end)}")
        lines.append(cue.text)
        lines.append("")

    return "\n".join(lines)
