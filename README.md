# Yomikoe

> **Offline Japanese Audio Subtitle Generator**

Yomikoe is an offline-first, open-source command-line application that
generates synchronized subtitle files from Japanese audio.

It is designed for learners, creators, and developers who want to process
Japanese audio locally without relying on cloud transcription services.

---

## ✨ Features

- 🎧 Process local audio files
- 🇯🇵 Japanese speech transcription
- 🕒 Timestamped transcription segments
- 📝 Automatic subtitle generation
- 📄 SRT subtitle export
- 📊 Transcription progress reporting
- 🧩 Replaceable transcription engine architecture
- 🔒 Offline-first and privacy-friendly
- 🧪 Automated tests for core processing components
- 🌱 Open-source and contributor-friendly architecture

### Current transcription backend

Yomikoe currently uses:

- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)

The transcription engine is isolated behind a stable interface so that
alternative engines can be introduced without redesigning the subtitle
generation pipeline.

---

## 🎯 Project Goals

Yomikoe is built around several core principles:

1. **Offline First**
   - Audio processing should not require a cloud service.
   - User audio remains on the local machine.

2. **Free & Open Source**
   - Avoid proprietary transcription services and vendor lock-in.

3. **Modular**
   - Major processing components have clear responsibilities.
   - Transcription engines are replaceable.

4. **Testable**
   - Core behavior should be verifiable without requiring a real
     transcription model or GPU.

5. **Maintainable**
   - Architecture, terminology, and important decisions are documented.

6. **Contributor Friendly**
   - Repository structure and engineering practices are designed to be
     understandable to new contributors.

---

## 🏗️ Architecture

The current MVP follows a small, explicit processing pipeline:

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
                    ┌─────────▼─────────┐
                    │   Audio Loader    │
                    └─────────┬─────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ Transcription Engine    │
                 │                         │
                 │  Faster-Whisper        │
                 │  Dummy Engine           │
                 └────────────┬────────────┘
                              │
                              ▼
                  ┌──────────────────────┐
                  │ TranscriptionResult │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Subtitle Generator  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     SRT Writer       │
                  └──────────┬───────────┘
                             │
                             ▼
                       ┌───────────┐
                       │ .srt file │
                       └───────────┘
