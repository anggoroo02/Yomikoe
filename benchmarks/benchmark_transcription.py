"""Benchmark Yomikoe transcription performance."""

import argparse
import time
from pathlib import Path

from yomikoe.engines import (
    ComputeBackend,
    FasterWhisperEngine,
    TranscriptionConfig,
)
from yomikoe.pipeline import transcribe_audio


def parse_args() -> argparse.Namespace:
    """Parse benchmark command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Benchmark Yomikoe transcription performance.",
    )

    parser.add_argument(
        "audio",
        type=Path,
        help="Path to the audio file to benchmark.",
    )

    parser.add_argument(
        "--model",
        default="small",
        help="Whisper model name. Default: small.",
    )

    parser.add_argument(
        "--language",
        default="ja",
        help="Transcription language code. Default: ja.",
    )

    parser.add_argument(
        "--device",
        type=ComputeBackend,
        choices=list(ComputeBackend),
        default=ComputeBackend.AUTO,
        help="Compute device: auto, cpu, or cuda. Default: auto.",
    )

    parser.add_argument(
        "--compute-type",
        default="default",
        help="Whisper compute type. Default: default.",
    )

    return parser.parse_args()


def format_duration(seconds: float | None) -> str:
    """Format a duration in seconds as HH:MM:SS."""
    if seconds is None:
        return "unknown"

    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def main() -> None:
    """Run the transcription benchmark."""
    args = parse_args()

    if not args.audio.is_file():
        raise SystemExit(f"Audio file not found: {args.audio}")

    config = TranscriptionConfig(
        model=args.model,
        language=args.language,
        backend=args.device,
        compute_type=args.compute_type,
    )

    engine_start = time.perf_counter()
    engine = FasterWhisperEngine(config=config)
    engine_init_time = time.perf_counter() - engine_start

    transcription_start = time.perf_counter()

    result = transcribe_audio(
        args.audio,
        engine,
    )

    transcription_time = time.perf_counter() - transcription_start

    audio_duration = result["audio"]["metadata"]["duration_seconds"]
    transcription = result["transcription"]

    rtf = None
    if audio_duration is not None and audio_duration > 0:
        rtf = transcription_time / audio_duration

    character_count = sum(
        len(segment.text.replace(" ", "").replace("\n", ""))
        for segment in transcription.segments
    )

    print("Yomikoe Transcription Benchmark")
    print("================================")
    print()
    print("Input")
    print(f"  File       : {args.audio}")
    print(f"  Duration   : {format_duration(audio_duration)}")
    print()
    print("Configuration")
    print(f"  Model      : {config.model}")
    print(f"  Language   : {config.language}")
    print(f"  Device     : {config.backend.value}")
    print(f"  Compute    : {config.compute_type}")
    print()
    print("Performance")
    print(f"  Backend    : {engine.backend.value}")
    print(f"  Engine init: {engine_init_time:.2f} s")
    print(f"  Runtime    : {transcription_time:.2f} s")

    if rtf is not None:
        print(f"  RTF        : {rtf:.3f}")
    else:
        print("  RTF        : unknown")

    print()
    print("Transcription")
    print(f"  Language   : {transcription.language}")
    print(f"  Segments   : {len(transcription.segments)}")
    print(f"  Characters : {character_count}")


if __name__ == "__main__":
    main()
