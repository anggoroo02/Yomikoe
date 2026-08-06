# Yomikoe

> **Offline Japanese Audio Subtitle Generator**

Generate synchronized subtitles from Japanese audio using a fully offline and open-source transcription pipeline.

<!-- Logo (Coming Soon) -->

---

## Introduction

Learning Japanese from podcasts, audiobooks, ASMR, radio programs, or recorded conversations can be difficult without synchronized subtitles.

**Yomikoe** is an offline-first application that generates subtitle files from Japanese audio using open-source speech recognition technology. It focuses on privacy, simplicity, and reproducibility by keeping the entire transcription process on your local machine without requiring cloud services.

Whether you're studying Japanese, creating subtitles for your own recordings, or building automated workflows, Yomikoe provides a modular foundation for generating accurate subtitle files from audio.

---

## Features

* ✅ Offline transcription
* ✅ Faster-Whisper backend
* ✅ Automatic subtitle generation
* ✅ Export to SRT
* ✅ Cross-platform
* ✅ Modular architecture
* ✅ Privacy-friendly

---

## Architecture

```text
CLI
 │
 ▼
Pipeline
 │
 ▼
Audio Loader
 │
 ▼
Transcription Engine
 │
 ▼
Transcription Result
 │
 ▼
Subtitle Generator
 │
 ▼
SRT Writer
```

The project is organized as a modular processing pipeline where each component has a single responsibility. This design makes the transcription engine, subtitle generation, and output formats easier to extend in the future.

---

## Installation

Clone the repository and install it in editable mode.

```bash
git clone https://github.com/anggoroo02/Yomikoe.git

cd yomikoe

python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -e .
```

---

## Quick Start

Transcribe a Japanese audio file:

```bash
yomikoe transcribe sample-JP.m4a
```

Output:

```text
sample-JP.srt
```

The generated SRT file can be opened with most video players or subtitle editors.

---

## Roadmap

### Current

* ✅ MVP

### Next

* ⬜ Progress reporting
* ⬜ Engine configuration
* ⬜ GPU auto detection

### Future

* ⬜ WebVTT export
* ⬜ ASS subtitle export
* ⬜ Graphical user interface (GUI)

---

## Project Status

**Current Status:** **MVP Complete**

The command-line application can:

* Load audio files
* Transcribe Japanese speech
* Generate subtitle models
* Export subtitles as SRT files

The architecture is designed for future expansion while keeping the current implementation lightweight and maintainable.

---

## Documentation

Additional documentation is available in the `docs/` directory, including architecture notes, design documents, and implementation details.

---

## Contributing

Contributions are welcome.

If you'd like to improve Yomikoe, please read **CONTRIBUTING.md** before submitting issues or pull requests.

---

## License

Licensed under the **MIT License**.
