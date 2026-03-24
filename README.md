# VidScribe

> Submit a video. Get back a readable, illustrated article.

VidScribe is a cloud-hosted service that accepts a YouTube URL, Zoom recording, or uploaded video file and returns a structured web article — titled sections, step-by-step text, and screenshots from the video placed contextually alongside the content. Think WikiHow or Medium, but generated automatically from any video.

---

## The Problem

Video is a poor reference format. You cannot skim it, search it, or quickly re-read a specific step. Existing tools produce raw transcripts or bullet-point summaries — not coherent, illustrated articles.

**VidScribe bridges that gap.**

---

## How It Works

```
Submit URL or file
        ↓
  REST API + Web UI
        ↓
   GCP Pub/Sub
        ↓
   GKE Worker
   ├── yt-dlp      → download video + extract captions
   ├── Whisper     → transcribe audio (fallback)
   ├── LLM API     → structure transcript into article sections
   └── ffmpeg      → extract frames at section timestamps
        ↓
  Assemble article (text + screenshots)
        ↓
  Shareable URL
```

---

## Stack

| Layer | Technology |
|---|---|
| Web UI | FastAPI + Jinja2 |
| REST API | FastAPI |
| Message Queue | GCP Pub/Sub |
| Container Orchestration | Google Kubernetes Engine (GKE) |
| Object Storage | Google Cloud Storage (GCS) |
| Database | Cloud SQL (PostgreSQL) |
| Cache | Redis (GCP Memorystore) |
| Video Download | yt-dlp |
| Transcription | Whisper (fallback when captions unavailable) |
| Frame Extraction | ffmpeg |
| Article Structuring | LLM API |
| Infrastructure | Terraform |

All infrastructure runs on **Google Cloud Platform**.

---

## Architecture

![Architecture Diagram](Project-diagram.svg)

---

## Project Status

> This project is under active development as a dual-class final project (Datacenter Applications + Generative AI).

- [ ] Infrastructure provisioning (Terraform)
- [ ] REST API + Web UI (FastAPI)
- [ ] GKE worker pipeline
- [ ] Video ingest (yt-dlp + caption extraction)
- [ ] Transcription fallback (Whisper)
- [ ] Article structuring (LLM)
- [ ] Frame extraction (ffmpeg)
- [ ] Article assembly + storage
- [ ] User testing

---

## Getting Started

> Build and run instructions will be added as implementation progresses.

---

## Repository Structure

> Directory structure will be added as implementation progresses.

---

## Author

Joel Carlson
