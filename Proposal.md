# Video-to-Article as a Service

**Author:** Joel Carlson
**Collaborators:** [Add name here if applicable]

---

## Project Goals

This project builds a cloud-hosted service that accepts any video — a YouTube URL, a Zoom recording, or an uploaded file — and returns a structured, illustrated web article. The output resembles a WikiHow or Medium post: titled sections, paragraph or step-by-step text, and screenshots from the video placed contextually alongside the content.

The core problem being solved is that video is a poor reference format. You cannot skim it, search it, or quickly re-read a specific step. Existing tools (Otter.ai, YouTube captions, Notion AI) produce raw transcripts or bullet summaries — not coherent, illustrated articles. This service bridges that gap.

Target users:
- **Students** who want searchable notes from recorded lectures
- **Professionals** who want structured summaries from Zoom meetings
- **Learners** following tutorial videos who need a readable reference

---

## Software and Hardware Components

All infrastructure is deployed on **Google Cloud Platform (GCP)**.

| Component | Technology | Role |
|---|---|---|
| RPC / API Interface | FastAPI (REST) | Accepts submissions, serves Web UI and article results |
| Web UI | FastAPI + Jinja2 | Submit form, job status page, article display page |
| Message Queue | GCP Pub/Sub | Decouples job submission from async processing |
| Containers | Google Kubernetes Engine (GKE) | Runs all application and worker code |
| Storage Service | Google Cloud Storage (GCS) | Stores uploaded videos and extracted screenshot frames |
| Database | Cloud SQL (PostgreSQL) | Stores job records and generated article HTML |
| Key-Value Store | Redis (GCP Memorystore) | Caches transcripts, tracks in-flight job state |
| Video Download | yt-dlp | Downloads YouTube videos and extracts existing captions |
| Transcription | Whisper (OpenAI) | Transcribes audio when captions are unavailable |
| Frame Extraction | ffmpeg | Extracts frames from video at section timestamps |
| Article Structuring | LLM API (TBD) | Structures transcript into titled sections with timestamps |

**Hardware:** No dedicated hardware. All compute runs on GCP-managed virtual machines within GKE node pools.

---

## Architecture Diagram

![Architecture Diagram](Project-diagram.svg)

---

## Component Interactions

The service operates as an asynchronous processing pipeline:

**Submission flow:**
1. The user submits a YouTube URL or uploads a video file via the Web UI
2. The REST API validates the input, creates a job record in PostgreSQL (status: pending), and writes any uploaded file to GCS
3. A lightweight job message (job ID, source type, URL or GCS path) is published to GCP Pub/Sub
4. The API immediately returns a job ID to the user — processing is asynchronous

**Processing flow:**
5. A GKE worker pod consumes the job message from Pub/Sub
6. The worker checks Redis for a cached transcript; if found, skips to step 9
7. yt-dlp downloads the video and checks for existing YouTube captions (manual captions first, then auto-generated)
8. If no captions exist, Whisper transcribes the audio and produces a transcript with word-level timestamps
9. The transcript is sent to the LLM API, which returns section titles, body text, and section-start timestamps
10. ffmpeg extracts a frame at each section-start timestamp; frames are uploaded to GCS and public image URLs are returned
11. Article text and image URLs are assembled into final HTML, stored in PostgreSQL, and the job is marked complete
12. The worker caches the transcript in Redis for retry resilience

**Response flow:**
13. The user's status page polls the REST API for job completion
14. On completion, the user is redirected to the article page
15. The article HTML is served from PostgreSQL; images are fetched directly from GCS by the browser

**Storage TTL:** GCS objects and PostgreSQL article records are automatically expired after N days via a GCS lifecycle policy and an `expires_at` field, bounding storage costs.

---

## Debugging and Testing

**Local development:**
Each processing step (ingest, transcription, structuring, frame extraction, assembly) will be implemented as an independently runnable Python module. This allows each stage to be tested in isolation without running the full pipeline.

**Test cases:**
The following videos will be used to validate end-to-end correctness:

| # | Video | Source | Captions | Purpose |
|---|---|---|---|---|
| 1 | [Short tutorial, 2–5 min] | YouTube | Manual | Baseline happy path |
| 2 | [Lecture recording, 30–60 min] | YouTube | Auto-generated | Quality and processing time at scale |
| 3 | [Zoom meeting recording] | File upload | None | File upload path + Whisper fallback |
| 4 | [Poor audio quality video] | YouTube or upload | None | Whisper stress test |

> Fill in specific video titles and URLs before submitting.

**Definition of success:**
- *Technical:* 90% of submitted test videos produce a complete article without error
- *User-facing:* Average user rating of 4/5 or higher across a minimum of 10 user test sessions

**LLM evaluation:** Before finalizing LLM selection, candidate models (e.g. Claude, GPT-4o) will be compared on a sample of test videos using defined criteria: section coherence, factual accuracy relative to transcript, and appropriate screenshot placement. Results will be documented in the final report.

---

## Why This Project Meets the Requirements

This project uses 7 of the 9 required datacenter software components:

1. **RPC / API interfaces** — REST API built with FastAPI
2. **Message queues** — GCP Pub/Sub decouples submission from processing
3. **Storage services** — GCS stores videos and frames
4. **Databases** — PostgreSQL on Cloud SQL stores jobs and articles
5. **Key-value stores** — Redis on Memorystore caches transcripts and job state
6. **Containers / functions as a service** — GKE orchestrates all application and worker containers
7. **Message marshalling / encoding** — JSON serialization between all services

Each component is used because it solves a specific architectural problem — the queue handles async processing, the key-value store avoids redundant transcription, the storage service offloads image serving from the application layer — not simply to satisfy a checklist. The project is a real service with a working end-to-end pipeline and real users, which also satisfies the GenAI course requirements for the Project/Startup Track.

The scope is realistic: the core pipeline (transcription + LLM structuring + article output) can be built and deployed as an MVP without screenshots or a polished UI, with enhancements added incrementally.

