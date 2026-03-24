# Ideation: Video-to-Article as a Service

**Author:** Joel Carlson

---

## Concept

A cloud-hosted service that accepts any video — a YouTube link, a Zoom recording, a lecture, a cooking tutorial, a coding walkthrough — and returns a structured, mobile-friendly web article summarizing the content. Think WikiHow or a Medium post, but generated automatically from video.

Users submit a URL or upload a file. The service processes it asynchronously and delivers a readable, shareable article with extracted screenshots placed contextually alongside the text.

---

## Problem

Video is a poor format for reference material. You cannot skim a video, search its contents, or quickly re-read a specific step. This is a real friction point for:

- **Students** who want searchable notes from lectures or recorded classes
- **Professionals** who want a summary and action items from Zoom meetings
- **Learners** following tutorial videos who need to pause, reference, and re-read steps

Existing tools (YouTube auto-captions, Otter.ai, Notion AI meeting summaries) produce raw transcripts or sparse bullet points — not a coherent, illustrated article.

---

## Solution

This product accepts a video and produces a structured web article with:

- Titled sections and subsections derived from the video's structure
- Step-by-step or paragraph-format text (adapted to content type: how-to vs. lecture vs. meeting)
- Screenshots extracted from the video placed at relevant points in the article
- A shareable, mobile-responsive URL

### Example Use Cases

| Input | Output |
|---|---|
| YouTube cooking tutorial | WikiHow-style recipe article with step images |
| Zoom team standup | Meeting summary with decisions and action items |
| Recorded lecture on thermodynamics | Study guide with diagrams and key concepts |
| Coding walkthrough on YouTube | Step-by-step tutorial with code screenshots |

---

## Why This Is Interesting

- **General-purpose**: The same pipeline handles any instructional or informational video
- **Genuinely useful**: Solves a real daily friction point for students, programmers, remote workers, and lifelong learners
- **Novel output format**: Existing tools don't produce illustrated, structured articles — they produce transcripts
- **Monetization path**: API access for platforms (e.g., e-learning sites), per-article credits, or SaaS subscription

---

## High-Level Technical Approach

The service is a distributed processing pipeline deployed on Google Cloud:

1. **Web UI**: Server-side rendered frontend (FastAPI + Jinja2) — submit form, status/progress page, article display page
2. **API layer**: REST API (same FastAPI service) accepts submissions, creates jobs, serves article data
3. **Job queue**: Submission is placed on a message queue; processing is handled asynchronously by worker nodes
4. **Processing workers** (containerized on GKE):
   - Video download via yt-dlp
   - Transcription: use existing YouTube captions if available, fall back to Whisper if not
   - Frame extraction at key moments via ffmpeg
   - LLM call to structure transcript into article with screenshot placement
5. **Storage**: Video files and generated screenshots stored in GCS (Google Cloud Storage)
6. **Database**: Job status, article metadata, and user history stored in PostgreSQL (Cloud SQL)
7. **Key-value store**: Cache transcription results and processing state for fast retries (Redis / Memorystore)
8. **Output**: Rendered HTML article served at a shareable, mobile-responsive URL

**LLM selection**: To be determined after an offline comparison of candidate models (e.g. Claude, GPT-4o) on a sample of test videos. The comparison will be documented in the final report as an evaluation finding rather than exposed as a runtime feature.

This architecture naturally incorporates the following datacenter components:
- RPC / API interfaces
- Message queues (GCP Pub/Sub)
- Storage services (GCS)
- Databases (PostgreSQL on Cloud SQL)
- Key-Value Stores (Redis on Memorystore)
- Containers (GKE)
- Message marshalling (JSON between services)

---

## Feasibility

- **AI components** are well-supported: Whisper (transcription fallback), ffmpeg (frame extraction), yt-dlp (download + caption extraction)
- **Infrastructure** maps directly onto Google Cloud: GKE for workers, Pub/Sub for queuing, GCS for storage, Cloud SQL (PostgreSQL) for metadata, Redis (Memorystore) for caching
- **Scope is controllable**: A working MVP supports URL input and text-only output; screenshots and full styling are enhancements
- **User testing is easy**: Share a link with classmates and colleagues, ask them to submit a video and rate the output

---

## Future Extensions

These are explicitly out of scope for the initial build but represent natural next steps:

- **Contextual Q&A**: A chat interface embedded on the article page, backed by a vector database over the transcript, letting users ask questions about the video content directly
- **Browser extension**: Convert any video you're currently watching with one click
- **Batch / playlist processing**: Submit an entire YouTube channel or course playlist
- **LMS integrations**: API connectors for Canvas, Coursera, or similar platforms so instructors can auto-generate notes for their recorded lectures
- **Multi-language support**: Whisper supports multilingual transcription; extending the LLM structuring step to non-English output is a natural follow-on

---

## Open Questions (for Proposal Phase)

- Screenshot selection strategy: fixed-interval extraction vs. AI-driven frame relevance scoring
- Article format adaptation: should the output format differ for meetings vs. tutorials vs. lectures?
- Authentication and rate limiting for the public API
- Whether to support real-time (streaming) progress updates to the user while the job runs
- Privacy handling for Zoom recordings containing sensitive business or personal information

