from pathlib import Path

import typer

from yomikoe import __version__
from yomikoe.audio import UnsupportedAudioFormatError
from yomikoe.engines import FasterWhisperEngine, TranscriptionProgress
from yomikoe.pipeline import transcribe_audio
from yomikoe.subtitle import (
    generate_subtitle,
    write_srt,
)

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


def get_output_path(audio_file: Path) -> Path:
    """Return the default subtitle output path."""
    return audio_file.with_suffix(".srt")


@app.command()
def transcribe(
    audio_file: Path,
    verbose: bool = False,
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output subtitle file path.",
    ),
):
    """Transcribe an audio file."""

    if not audio_file.exists():
        exit_with_error(f"Error: File not found: {audio_file}")

    if not audio_file.is_file():
        exit_with_error(f"Error: Path is not a file: {audio_file}")

    progress_displayed = False
    progress_total_seconds: float | None = None

    def display_progress(progress: TranscriptionProgress) -> None:
        nonlocal progress_displayed, progress_total_seconds

        if progress.total_seconds <= 0:
            return

        percentage = int(progress.current_seconds / progress.total_seconds * 100)
        percentage = max(0, min(percentage, 100))
        if verbose:
            message = (
                f"Transcribing... {percentage}% | "
                f"{format_duration(progress.current_seconds)} / "
                f"{format_duration(progress.total_seconds)}"
            )
        else:
            message = f"Transcribing... {percentage}%"

        typer.echo(f"\r{message}", nl=False)
        progress_displayed = True
        progress_total_seconds = progress.total_seconds

    try:
        engine = FasterWhisperEngine()

        initial_backend = engine.backend

        typer.echo(f"Compute backend: {engine.backend}")

        pipeline_result = transcribe_audio(
            audio_file,
            engine,
            progress_callback=display_progress,
        )

        if engine.backend is not initial_backend:
            typer.echo(
                f"CUDA unavailable during transcription. "
                f"Falling back to {engine.backend}."
            )

    except UnsupportedAudioFormatError as exc:
        exit_with_error(str(exc))

    if progress_displayed:
        if verbose and progress_total_seconds is not None:
            typer.echo(
                "\rTranscribing... 100% | "
                f"{format_duration(progress_total_seconds)} / "
                f"{format_duration(progress_total_seconds)}"
            )
        else:
            typer.echo("\rTranscribing... 100%")

    metadata = pipeline_result["audio"]["metadata"]
    result = pipeline_result["transcription"]

    typer.echo(f"File      : {metadata['filename']}")
    typer.echo(f"Extension : {metadata['extension']}")
    typer.echo(f"Size      : {metadata['size_bytes']} bytes")
    typer.echo(f"Duration  : {format_duration(metadata['duration_seconds'])}")

    subtitle = generate_subtitle(result)

    srt = write_srt(subtitle)

    output_file = output or get_output_path(audio_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        output_file.write_text(
            srt,
            encoding="utf-8",
        )
    except OSError as exc:
        exit_with_error(
            f"Error: Could not write subtitle file: {output_file}\nReason: {exc}"
        )

    typer.echo()
    typer.echo(f"Engine    : {engine.__class__.__name__}")
    typer.echo(f"Backend   : {engine.backend}")
    typer.echo(f"Language  : {result.language}")
    typer.echo(f"Segments  : {len(result.segments)}")
    typer.echo(f"Output    : {output_file}")


if __name__ == "__main__":
    app()
