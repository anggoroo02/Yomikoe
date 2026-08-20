# Benchmarking

Yomikoe includes a small local benchmark harness for measuring transcription performance.

The benchmark is intentionally separate from the test suite. Unit and integration tests verify deterministic behavior, while benchmarks measure behavior that depends on the local machine, model, backend, and audio input.

## Purpose

The baseline benchmark establishes a reference point for the current transcription pipeline before transcription post-processing is introduced.

The initial benchmark measures:

* audio duration
* model initialization time
* transcription runtime
* real-time factor (RTF)
* resolved compute backend
* transcription language
* number of transcription segments
* total transcription character count

These measurements will be used as a baseline when evaluating future changes to transcription processing and subtitle generation.

## Usage

Run the benchmark from the repository root:

```powershell
python -m benchmarks.benchmark_transcription <audio>
```

For example:

```powershell
python -m benchmarks.benchmark_transcription sample-JP.m4a
```

The benchmark uses the same Yomikoe transcription pipeline as the application rather than calling Faster-Whisper directly.

## Configuration

The benchmark follows the current Yomikoe engine configuration defaults:

| Option           | Default   |
| ---------------- | --------- |
| `--model`        | `small`   |
| `--language`     | `ja`      |
| `--device`       | `auto`    |
| `--compute-type` | `default` |

Options can be overridden from the command line:

```powershell
python -m benchmarks.benchmark_transcription sample-JP.m4a `
    --model small `
    --language ja `
    --device cpu `
    --compute-type default
```

The supported devices are:

* `auto`
* `cpu`
* `cuda`

Use `--help` to see all available options:

```powershell
python -m benchmarks.benchmark_transcription --help
```

## Real-Time Factor

The benchmark reports the real-time factor:

```text
RTF = transcription runtime / audio duration
```

For example, an RTF of `0.500` means that transcription took approximately half the duration of the input audio.

Lower RTF indicates faster transcription.

## Benchmark Audio

Benchmark audio files are kept locally and are not committed to the repository.

This keeps large media files and potentially private audio outside the source tree.

For reproducible comparisons, use the same audio sample and the same engine configuration across benchmark runs.

## Current Scope

The initial benchmark intentionally does not measure:

* CPU utilization
* RAM usage
* GPU utilization
* GPU memory usage
* transcription accuracy
* WER/CER
* subtitle quality
* post-processing performance

Those measurements can be added when there is a concrete need for them.

In particular, transcription accuracy is not currently reported because a benchmark score requires a trusted ground-truth transcript.

## Future Use

The raw transcription produced by this benchmark will later be useful as input for post-processing experiments.

The intended comparison is:

```text
Audio
  ↓
Transcription
  ↓
Raw transcription baseline
  ↓
Post-processing
  ↓
Subtitle cues
  ↓
SRT
```

Post-processing should be evaluated against the same raw transcription so that changes in cue segmentation can be studied without repeatedly running the Whisper model.
