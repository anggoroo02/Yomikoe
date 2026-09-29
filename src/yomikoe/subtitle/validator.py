import re
from pathlib import Path

_TIMESTAMP_PATTERN = re.compile(
    r"^(?P<hours>\d{2}):(?P<minutes>\d{2}):"
    r"(?P<seconds>\d{2}),(?P<milliseconds>\d{3})$"
)


def _parse_timestamp(timestamp: str) -> int:
    match = _TIMESTAMP_PATTERN.fullmatch(timestamp)

    if match is None:
        raise ValueError("invalid SRT timestamp")

    hours = int(match.group("hours"))
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    milliseconds = int(match.group("milliseconds"))

    if minutes >= 60 or seconds >= 60:
        raise ValueError("invalid SRT timestamp")

    return hours * 3_600_000 + minutes * 60_000 + seconds * 1_000 + milliseconds


def _parse_timestamp_line(line: str) -> tuple[int, int]:
    parts = line.split(" --> ")

    if len(parts) != 2:
        raise ValueError("invalid SRT timestamp")

    start = _parse_timestamp(parts[0])
    end = _parse_timestamp(parts[1])

    return start, end


def validate_srt_artifact(
    output_file: Path,
    expected_cue_count: int,
) -> None:
    """Validate an SRT artifact written to disk."""
    if expected_cue_count < 0:
        raise ValueError("expected_cue_count must be >= 0")

    if not output_file.is_file():
        raise ValueError("SRT artifact must be a file")

    try:
        content = output_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError("SRT artifact could not be read") from exc

    if not content:
        if expected_cue_count == 0:
            return

        raise ValueError("SRT cue count does not match expected cue count")

    blocks = [block for block in content.split("\n\n") if block.strip()]

    if len(blocks) != expected_cue_count:
        raise ValueError("SRT cue count does not match expected cue count")

    for index, block in enumerate(blocks, start=1):
        lines = block.splitlines()

        if len(lines) < 3:
            raise ValueError("invalid SRT cue")

        if lines[0] != str(index):
            raise ValueError("invalid SRT cue numbering")

        start, end = _parse_timestamp_line(lines[1])

        if end <= start:
            raise ValueError("SRT cue end must be greater than start")

        if not any(line.strip() for line in lines[2:]):
            raise ValueError("SRT cue text must not be empty or whitespace")
