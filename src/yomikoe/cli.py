from pathlib import Path
from yomikoe.audio import inspect_audio

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

    metadata = inspect_audio(audio_file)

    typer.echo(f"File      : {metadata['filename']}")
    typer.echo(f"Extension : {metadata['extension']}")
    typer.echo(f"Size      : {metadata['size_bytes']} bytes")

    typer.echo()
    typer.echo("Transcription engine is not implemented yet.")


if __name__ == "__main__":
    app()