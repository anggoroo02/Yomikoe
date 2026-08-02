import typer

from yomikoe import __version__

app = typer.Typer(
    name="yomikoe",
    help="Offline Japanese Audio Subtitle Generator",
)


@app.command()
def version():
    """Show application version."""
    typer.echo(f"Yomikoe {__version__}")


@app.command()
def transcribe(audio_file: str):
    """Transcribe an audio file."""
    typer.echo(f"Input file: {audio_file}")
    typer.echo("Transcription engine is not implemented yet.")


if __name__ == "__main__":
    app()