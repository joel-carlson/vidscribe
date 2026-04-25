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

## Repository Structure

```
api/                  FastAPI app + worker
  main.py             REST API endpoints and web UI
  db.py               Database access layer
  pubsub.py           Pub/Sub publisher
  config.py           API config (env vars)
  migrations/         SQL schema
  templates/          Jinja2 HTML templates
  worker/             GKE worker process
    worker.py         Pub/Sub consumer + pipeline orchestrator
    ingest.py         Video download (yt-dlp + GCS)
    transcription.py  Whisper transcription
    structuring.py    LLM article structuring (Vertex AI)
    frames.py         ffmpeg frame extraction
    gcs.py            GCS upload/download
    assembly.py       Article assembly + DB write
    cache.py          Redis cache
    config.py         Worker config (env vars)
k8s/                  Kubernetes manifests
terraform/            GCP infrastructure (Terraform)
docker-compose.yml    Local development stack
```

---

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`)
- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.0
- [Docker](https://docs.docker.com/get-docker/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- A GCP project with billing enabled

---

## Deployment

### 1. Configure GCP

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

Enable required APIs:

```bash
gcloud services enable container.googleapis.com \
  sqladmin.googleapis.com \
  servicenetworking.googleapis.com \
  pubsub.googleapis.com \
  storage.googleapis.com \
  redis.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com
```

### 2. Provision Infrastructure

```bash
cd terraform
```

Create `terraform.tfvars` (never commit this file — it is gitignored):

```hcl
project_id   = "YOUR_PROJECT_ID"
region       = "us-central1"
sql_password = "YOUR_STRONG_PASSWORD"
```

Then apply:

```bash
terraform init
terraform apply
```

Note the outputs — you will need them in the next steps:

```bash
terraform output REDIS_HOST
terraform output CSQL_CONNECTION_NAME
```

### 3. Configure kubectl

```bash
gcloud container clusters get-credentials vidscribe-cluster --region us-central1
```

### 4. Create the Database Secret

The database password is never stored in any committed file. Create the Kubernetes Secret manually:

```bash
kubectl create secret generic vidscribe-secrets \
  --from-literal=DATABASE_URL="postgresql://vidscribe-user:YOUR_PASSWORD@/vidscribe?host=/cloudsql/YOUR_PROJECT_ID:us-central1:vidscribe-sql-instance"
```

Replace `YOUR_PASSWORD` and `YOUR_PROJECT_ID` with your values.

### 5. Update the ConfigMap

Edit `k8s/configmap.yaml` and set `REDIS_URL` to the Redis host from `terraform output REDIS_HOST`:

```yaml
REDIS_URL: "redis://REDIS_IP:6379"
```

### 6. Build and Push Docker Images

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev

# API image
docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/vidscribe/api:latest ./api
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/vidscribe/api:latest

# Worker image
docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/vidscribe/worker:latest ./api
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/vidscribe/worker:latest
```

### 7. Run Database Migrations

Connect to Cloud SQL via the proxy and run the schema:

```bash
cloud-sql-proxy YOUR_PROJECT_ID:us-central1:vidscribe-sql-instance &
psql "postgresql://vidscribe-user:YOUR_PASSWORD@localhost:5432/vidscribe" \
  -f api/migrations/001_initial_schema.sql
```

### 8. Deploy to Kubernetes

```bash
kubectl apply -f k8s/serviceaccount.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml
```

### 9. Get the External IP

```bash
kubectl get service vidscribe-api-service
```

Once `EXTERNAL-IP` is assigned (may take a minute), open it in a browser.

---

## Local Development

Start the local stack with Docker Compose:

```bash
docker compose up
```

This starts PostgreSQL, Redis, and a local GCS emulator. The API runs at `http://localhost:8000`.

Run the API separately (with hot reload):

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

Run the worker separately:

```bash
cd api
python -m worker.worker
```

---

## Known Issues & Solutions

A log of non-obvious problems encountered during development and deployment, kept here so they don't need to be solved twice.

---

### Docker image platform mismatch on Apple Silicon

**Symptom:** Pods stuck in `ImagePullBackOff` with error `no match for platform in manifest: not found`.

**Cause:** Docker builds on Apple Silicon (M1/M2/M3) default to `linux/arm64`. GKE nodes run `linux/amd64`. The image lands in Artifact Registry but the node cannot use it.

**Fix:** Always build with `--platform linux/amd64` when targeting GKE:
```bash
docker build --platform linux/amd64 -t IMAGE_TAG ./api
```

---

### GKE nodes cannot pull from Artifact Registry

**Symptom:** Pods in `ImagePullBackOff`, event log shows `403 Forbidden` or permission denied when pulling from `us-central1-docker.pkg.dev`.

**Cause:** The GKE node pool's service account (the Compute Engine default SA) does not have permission to read from Artifact Registry by default.

**Fix:**
```bash
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)')
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

---

### GKE cluster stuck in PROVISIONING / GCE_STOCKOUT

**Symptom:** `terraform apply` completes but the node pool never becomes ready. GCP Console shows `GCE_STOCKOUT` — the requested machine type is unavailable in that zone.

**Cause:** GCP zones have limited capacity for specific machine types. Larger types (`e2-standard-2`, `e2-medium`) were unavailable in both `us-central1` and `us-east1` at time of deployment.

**Fix:** Use `e2-small` in `terraform/gke.tf`. Also remove any stuck cluster from state before retrying:
```bash
terraform state rm google_container_node_pool.primary_nodes
terraform state rm google_container_cluster.vidscribe_gke
```
Then delete the cluster from GCP Console and re-run `terraform apply`.

---

### Terraform subnet modification blocked

**Symptom:** `terraform apply` fails with `error modifying Subnetwork: subnetwork is already in use`.

**Cause:** GKE attaches to the subnet and GCP prevents changes to it while in use.

**Fix:** Add a lifecycle ignore block to the subnet in `terraform/vpc.tf`:
```hcl
lifecycle {
  ignore_changes = [secondary_ip_range]
}
```

---

### Worker startup hangs (Whisper / PyTorch import)

**Symptom:** Running `python -m worker.worker` appears to hang for several minutes with no output.

**Cause:** `import whisper` triggers PyTorch to load and JIT-compile kernels on first run. This takes 5–10 minutes on first execution and ~1 minute on subsequent runs once the cache is warm. It is not a deadlock.

**Fix:** Wait. On first run after a fresh environment, allow at least 10 minutes before concluding something is wrong.

---

### Worker crashes on startup (GCP clients at import time)

**Symptom:** `ImportError` or authentication error when the worker module is imported, before any job is processed.

**Cause:** Module-level instantiation of `google.cloud.storage.Client()` or `genai.Client(vertexai=True, ...)` makes network/auth calls at import time. If credentials are not available in the import environment, this fails immediately.

**Fix:** Use lazy initialization — only create the client on first use:
```python
_client: storage.Client | None = None

def _get_client() -> storage.Client:
    global _client
    if _client is None:
        _client = storage.Client(...)
    return _client
```

---

### ffmpeg frame extraction fails with "filename does not contain image sequence pattern"

**Symptom:** `subprocess.CalledProcessError` from ffmpeg when extracting a single frame to a `.jpg` path.

**Cause:** ffmpeg treats output filenames without a sequence pattern (e.g. `%04d.jpg`) as an image sequence by default and rejects single-file output.

**Fix:** Add the `-update 1` flag to tell ffmpeg the output is a single file:
```bash
ffmpeg -ss TIMESTAMP -i video.mp4 -frames:v 1 -update 1 -y output.jpg
```

---

### Database URL pointing to wrong host on startup

**Symptom:** `asyncpg.exceptions.InvalidPasswordError` or connection refused when starting the API or worker locally.

**Cause:** A stale `DATABASE_URL` environment variable set in the terminal session overrides the value in `config.py`.

**Fix:**
```bash
unset DATABASE_URL
```
Then restart the process.

---

## Author

Joel Carlson
