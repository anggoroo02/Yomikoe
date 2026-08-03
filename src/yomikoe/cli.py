from pathlib import Path
from yomikoe.audio import (
    UnsupportedAudioFormatError,
    load_audio,
)

import typer

from yomikoe import __version__


app = typer.Typer(
    name="yomikoe",
    help="Offline Japanese Audio Subtitle Generator",
)


def exit_with_error(message: str) -> None:
    """Print an error message and exit with a non-zero status."""
    typer.echo(message, err=True)
    raise typer.Exit(code=1)


def format_duration(seconds: float | None) -> str:
    """Format duration in HH:MM:SS."""
    if seconds is None:
        return "Unknown"

    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02}"

@app.command()
def version():
    """Show application version."""
    typer.echo(f"Yomikoe {__version__}")


@app.command()
def transcribe(audio_file: Path):
    """Transcribe an audio file."""
    if not audio_file.exists():
        exit_with_error(f"Error: File not found: {audio_file}")

    if not audio_file.is_file():
        exit_with_error(f"Error: Path is not a file: {audio_file}")

    try:
        loaded_audio = load_audio(audio_file)
    except UnsupportedAudioFormatError as exc:
        exit_with_error(str(exc))

    loaded_audio = load_audio(audio_file)
    metadata = loaded_audio["metadata"]

    typer.echo(f"File      : {metadata['filename']}")
    typer.echo(f"Extension : {metadata['extension']}")
    typer.echo(f"Size      : {metadata['size_bytes']} bytes")
    typer.echo(
        f"Duration  : {format_duration(metadata['duration_seconds'])}"
    )

    typer.echo()
    typer.echo("Transcription engine is not implemented yet.")


if __name__ == "__main__":
    app()