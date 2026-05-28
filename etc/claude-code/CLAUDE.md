# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is the planning and (eventually) implementation directory for a dual-class final project:

- **Datacenter class** (30% of grade): Must build a cloud-hosted *service* using 5+ datacenter software components. Deliverables: ideation (week 8), proposal (week 11), final report + git repo + video demo (last day of classes).
- **GenAI class** (30% of grade): Project/Startup Track — must solve a real-world problem using AI, with a working prototype, user testing, and deployment. Deliverables: writing PDF, demo video, slides.

## The Project: Video-to-Article as a Service

Accepts a video (YouTube URL, Zoom recording, file upload) and produces a structured, illustrated web article (WikiHow/Medium style) with extracted screenshots and LLM-structured text.

**Planned stack (Google Cloud):**
- REST API + Web UI (FastAPI + Jinja2) → Cloud Pub/Sub job queue → GKE containerized workers
- Workers: yt-dlp (download + captions), Whisper (transcription fallback), ffmpeg (frame extraction), LLM API (structuring)
- GCS (video + frame storage), Cloud SQL/PostgreSQL (jobs + articles), Redis/Memorystore (cache)

**Infrastructure provisioning:** Terraform — all GCP resources defined as code and version controlled alongside application code.

**Datacenter components satisfied:** RPC/API, message queues, storage (GCS), databases, key-value stores, containers (GKE), message marshalling (7 of 9 required).

## Key Planning Files

- `ideation.md` — full ideation document (detailed version)
- `ideation-pitch.md` — ~2000 char condensed pitch + open questions list
- `assignment-parameters-datacenter.md` — datacenter class requirements
- `assignment-paramters-GENAI.md` — GenAI class requirements

## Coding Style

Inferred from `/Users/joelcarlson/Library/Mobile Documents/com~apple~CloudDocs/Summer-2024/RMBL/RMBL_SnowView/models/Xception/`.

- **File-per-concern**: one responsibility per file (e.g. Model, Train, Processing, Utils, Evaluation)
- **Functions over classes**: encapsulation through module boundaries, not OOP
- **Google-style docstrings** with Args + Returns on public functions
- **ALL_CAPS constants** at the top of each module
- **Section comments** inside functions to label logical blocks
- **`if __name__ == "__main__":` in every file** so each module is independently runnable/testable
- **Imports**: stdlib → third-party, `from X import Y` preferred; grouped with blank lines
- **Type hints on all functions** — annotate all parameters and return types. Use `from __future__ import annotations` for forward references. Prefer specific types over `Any`.
- Explicit is preferred over clever — readable section-by-section code over compact one-liners
- User has a C++ background and prefers strongly typed code — lean into Python's type system fully

## When Code Exists

Update this file with build/run/test commands, service architecture, and deployment notes.
