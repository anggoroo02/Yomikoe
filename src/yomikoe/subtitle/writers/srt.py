from yomikoe.subtitle.models import Subtitle


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp."""

    milliseconds = int(round(seconds * 1000))

    hours = milliseconds // 3_600_000
    milliseconds %= 3_600_000

    minutes = milliseconds // 60_000
    milliseconds %= 60_000

    secs = milliseconds // 1000
    milliseconds %= 1000

    return (
        f"{hours:02}:"
        f"{minutes:02}:"
        f"{secs:02},"
        f"{milliseconds:03}"
    )

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
        lines.append(
            f"{format_timestamp(cue.start)} --> "
            f"{format_timestamp(cue.end)}"
        )
        lines.append(cue.text)
        lines.append("")

    return "\n".join(lines)