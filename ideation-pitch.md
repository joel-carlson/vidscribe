# Video-to-Article as a Service

Submit a video link or file and receive a structured, illustrated web article — like WikiHow or Medium, but generated automatically from any video.

### **The Problem**
Video is a poor reference format. You cannot skim it, search it, or re-read a specific step. Existing tools (Otter.ai, YouTube captions, Notion AI) produce raw transcripts or bullet-point summaries — not coherent, illustrated articles.

### **What It Does**
Accepts YouTube links, Zoom recordings, lectures, tutorials, or any uploaded video file. Transcribes the audio, extracts contextual screenshots, and uses an LLM to structure the content into a titled, section-based article. Output is a mobile-friendly, shareable URL.

**Why It's Interesting**
- General-purpose: one pipeline handles how-tos, meetings, and lectures
- Genuinely novel output: no existing tool produces illustrated, structured articles from video
- Clear user groups: students wanting lecture notes, professionals wanting meeting summaries, learners following tutorials
- Monetization path: API for e-learning platforms, per-article credits, or SaaS

### **Technical Approach (Google Cloud)**
REST API + Web UI (FastAPI + Jinja2) accepts submissions → Pub/Sub job queue → containerized workers on GKE handle transcription (Whisper), frame extraction (ffmpeg), and LLM structuring. GCS stores video and images; Cloud SQL (PostgreSQL) stores metadata; Redis (Memorystore) handles caching. Infrastructure provisioned via Terraform. Satisfies 7 of 9 required datacenter software components.

### **Feasibility**
AI tools are now mature. GCP maps cleanly to the required architecture. An MVP producing text-only articles is achievable early; screenshots and styling are additive enhancements. User testing is straightforward: share a link, have users submit a video, collect ratings.

## Questions I need to answer for my proposal:

- Screenshot selection strategy: fixed-interval extraction vs. AI-driven frame relevance scoring
- Article format adaptation: should the output format differ for meetings vs. tutorials vs. lectures?
- Authentication and rate limiting for the public API
- Whether to support real-time (streaming) progress updates to the user while the job runs
- Privacy handling for Zoom recordings containing sensitive business or personal information
- How to define "success" for user testing — article coherence score, user rating, time-to-article, or some combination
- Cost per job estimation: transcription + LLM calls on a 1-hour video add up; need to establish a per-job budget before opening to broader testing
- Copyright and ToS implications of processing YouTube videos via download; file upload sidesteps this but limits use cases
