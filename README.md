# Yomikoe

> **Offline Japanese Audio Subtitle Generator**

Yomikoe is an open-source command-line application that generates synchronized `.srt` subtitles from Japanese audio.

It is designed for learners, creators, and developers who want to process Japanese audio locally without relying on cloud transcription services.

Yomikoe follows an **offline-first, modular, and privacy-oriented** approach. Audio processing happens on your machine, allowing you to generate subtitles without uploading your audio to a cloud transcription service.

## ✨ Features

- 🎧 Process local audio files
- 🇯🇵 Japanese speech transcription
- 🕒 Timestamped transcription segments
- 📝 Automatic subtitle generation
- 📄 SRT subtitle export
- 📊 Transcription progress model
- 🧩 Replaceable transcription engine architecture
- 🔒 Offline-first and privacy-oriented
- 🧪 Automated tests for core processing components
- 🌱 Contributor-friendly repository structure

### Supported Audio Formats

Yomikoe currently supports:

- `.wav`
- `.mp3`
- `.m4a`
- `.flac`
- `.ogg`

### Current Transcription Backend

Yomikoe currently uses [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) as its transcription backend.

The transcription engine is isolated behind an application-level interface, allowing alternative engines to be introduced without redesigning the subtitle generation workflow.

## 🚀 Installation

> ⚠️ **Yomikoe is currently under development and has not yet reached a stable release.**

### Requirements

Before installing Yomikoe, make sure you have:

- Python 3.12 or later
- Windows, Linux, or macOS
- Sufficient local hardware for transcription

### Install

Open a terminal, Command Prompt, or PowerShell and run:

```bash
git clone https://github.com/anggoroo02/Yomikoe.git
cd Yomikoe
```

If you do not have Git installed, you can download the repository as a ZIP file from GitHub, extract it, and open a terminal inside the project folder.

Create a virtual environment.

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Yomikoe:

```bash
pip install -e .
```

Yomikoe is now ready to use.

## ▶️ Quick Start

Suppose you have an audio file:

```text
sample.m4a
```

Run:

```bash
yomikoe transcribe sample.m4a
```

Yomikoe will process the audio and generate:

```text
sample.srt
```

The subtitle file is created in the same location as the input audio file.

### Show Version

```bash
python -m yomikoe version
```

Or, after installation:

```bash
yomikoe version
```

### Transcribe Audio

```bash
python -m yomikoe transcribe sample.m4a
```

Or:

```bash
yomikoe transcribe sample.m4a
```

### Verbose Progress

Use `--verbose` to display additional transcription progress information:

```bash
yomikoe transcribe sample.m4a --verbose
```

Example output:

```text
Transcribing... 25% | 00:00:15 / 00:01:00
Transcribing... 50% | 00:00:30 / 00:01:00
Transcribing... 75% | 00:00:45 / 00:01:00
Transcribing... 100% | 00:01:00 / 00:01:00
```

Example file information:

```text
File      : sample.m4a
Extension : .m4a
Size      : 123456 bytes
Duration  : 00:01:00
```

Example transcription information:

```text
Engine    : FasterWhisperEngine
Language  : ja
Segments  : 42
Output    : sample.srt
```

> Transcription performance depends heavily on the selected model, hardware, and local environment.

## 🧱 Architecture

Yomikoe separates the main processing responsibilities into independent modules.

The current MVP follows this processing pipeline:

```text
                 ┌──────────────────┐
                 │       CLI        │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Pipeline     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Audio Loader   │
                 └────────┬─────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │  Transcription Engine    │
             │                          │
             │     Faster-Whisper       │
             │     Dummy Engine         │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │   TranscriptionResult    │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │   Subtitle Generator     │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │        SRT Writer        │
             └────────────┬─────────────┘
                          │
                          ▼
                     ┌─────────┐
                     │  .srt   │
                     └─────────┘
```

At a high level:

```text
Audio File
    ↓
Audio Metadata & Validation
    ↓
Transcription
    ↓
Timestamped Segments
    ↓
Subtitle Model
    ↓
SRT
```

The pipeline is intentionally kept small during the MVP stage.

### Design Principles

Yomikoe is built around several core principles:

* **Offline First** — Audio processing is performed locally.
* **Free & Open Source** — The project relies on free and open-source technologies while avoiding unnecessary vendor lock-in.
* **Modular** — Major processing responsibilities are separated into independent modules.
* **Testable** — Core processing behavior can be tested without requiring a real transcription model, GPU, CUDA, downloaded Whisper models, or long-running transcription jobs.
* **Maintainable** — Architecture, domain terminology, and important design decisions are documented in the repository.
* **Contributor Friendly** — The repository is structured to make the codebase and development workflow easier to understand.

### Source Structure

```text
src/yomikoe/
├── audio/       # Audio inspection and loading
├── engines/     # Transcription engine abstractions and implementations
├── pipeline/    # Processing orchestration
└── subtitle/    # Subtitle generation and serialization
```

The most important architectural boundary is the transcription engine.

The pipeline does not need to know whether transcription is performed by Faster-Whisper, a dummy implementation, or a future transcription engine.

This keeps the transcription backend replaceable while allowing the rest of the processing flow to remain stable.

## 📚 Documentation

The `docs/` directory contains the project's architectural and development documentation.

The architecture documentation is organized into four areas:

### `01-foundation`

* Project vision
* Requirements
* Repository structure
* Architectural rules

### `02-domain`

* Domain model
* Processing pipeline
* Data transformations
* Error model
* Processing job lifecycle

### `03-core`

* High-level architecture
* Module specification
* Ports & contracts
* Extension architecture

### `04-governance`

* Architecture decisions
* Development governance

### Architecture Decisions

Important architectural decisions are recorded as ADRs.

Current decisions include:

* ADR-001 — MVP Architecture Baseline
* ADR-002 — Canonical Domain Terminology

See `docs/decisions/adr/` for the current ADR index.

### Repository Structure

```text
Yomikoe/
├── .github/
├── assets/
├── docs/
│   ├── architecture/
│   │   ├── 01-foundation/
│   │   ├── 02-domain/
│   │   ├── 03-core/
│   │   └── 04-governance/
│   ├── decisions/
│   │   └── adr/
│   └── ...
├── src/
│   ├── scripts/
│   └── yomikoe/
│       ├── audio/
│       ├── engines/
│       ├── pipeline/
│       └── subtitle/
├── tests/
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── CHANGELOG.md
├── pyproject.toml
└── README.md
```

## 🤝 Contributing

Contributions are welcome.

Before making changes, please read:

* `CONTRIBUTING.md`
* `CODE_OF_CONDUCT.md`
* `SECURITY.md`

For architectural changes, please review the architecture documentation and existing ADRs before introducing new abstractions or changing module boundaries.

The project intentionally favors:

* Simple implementations
* Small public interfaces
* Explicit data flow
* Replaceable components
* Testable code
* Minimal coupling

Avoid introducing abstractions solely for hypothetical future requirements.

### Development

Yomikoe uses a `src/` layout and keeps development dependencies lightweight.

Install the project in editable mode:

```bash
pip install -e .
```

Run the test suite:

```bash
pytest -v
```

Run Ruff to check the source code:

```bash
ruff check src tests
```

Check formatting:

```bash
ruff format --check src tests
```

Apply formatting when necessary:

```bash
ruff format src tests
```

## 🧪 Project Status

Yomikoe is currently in **early MVP development**.

### Implemented

* CLI foundation
* Audio metadata inspection
* Audio loading and format validation
* Transcription engine abstraction
* Dummy transcription engine
* Processing pipeline
* Faster-Whisper integration
* Transcription result model
* Transcription progress model
* Subtitle model
* Subtitle generation
* SRT serialization
* CLI SRT export
* Core pipeline tests
* Contributor-oriented repository documentation

### Planned

The following areas are planned but are not currently part of the implemented MVP:

* Better CLI error handling
* More transcription engine configuration
* Improved device / compute configuration
* Additional subtitle formats
* Additional CLI output options
* GUI

### Current Limitations

At the current stage:

* The primary interface is the CLI
* SRT is the currently implemented subtitle output format
* Faster-Whisper is the current real transcription backend
* GPU/CUDA configuration is still under development
* Transcription can be computationally expensive, especially on CPU
* The project does not currently provide a GUI
* Translation is not part of the current MVP
* Cloud transcription is not supported or required

> Do not treat the current development version as a stable release.

### Roadmap

The long-term direction of Yomikoe is to evolve from a small CLI utility into a maintainable local Japanese audio processing tool.

Possible future capabilities include:

* Additional transcription engines
* Additional subtitle formats
* Improved subtitle processing
* Subtitle quality enhancement
* Translation
* Speaker diarization
* GUI

These are future possibilities, not promises for the current MVP.

## 📄 License

Yomikoe is released under the MIT License.

See `LICENSE` for the full license text.

---

> **Build the smallest useful system. Keep the boundaries clean. Let the architecture grow with the project.**

miaw~