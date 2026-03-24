# System Architecture Diagram

```mermaid
flowchart TD
    classDef user     fill:#4A90D9,stroke:#2C5F8A,color:#fff
    classDef api      fill:#27AE60,stroke:#1E8449,color:#fff
    classDef queue    fill:#E67E22,stroke:#CA6F1E,color:#fff
    classDef worker   fill:#8E44AD,stroke:#6C3483,color:#fff
    classDef db       fill:#C0392B,stroke:#922B21,color:#fff
    classDef external fill:#7F8C8D,stroke:#566573,color:#fff
    classDef decision fill:#F39C12,stroke:#D68910,color:#fff

    User(["👤 User\nBrowser"]):::user

    subgraph api ["  🌐  API Layer  "]
        REST["⚡ REST API"]:::api
    end

    subgraph queue ["  📨  Message Queue  "]
        PubSub["📨 GCP Pub/Sub"]:::queue
    end

    subgraph workers ["  ⚙️  GKE Processing Workers  "]
        Ingest["📥 Video Ingest\nyt-dlp · file upload"]:::worker
        CaptionCheck{"📝 Captions\nAvailable?"}:::decision
        Whisper["🎙️ Whisper\nASR Transcription"]:::worker
        LLM["🧠 LLM\nArticle Structuring"]:::worker
        Frames["🎞️ ffmpeg\nFrame Extraction"]:::worker
        Assemble["📄 Article\nAssembly"]:::worker
    end

    subgraph storage ["  🗄️  Storage Layer  "]
        GCS[("☁️ GCS\nVideos · Frames")]:::db
        DB[("🗄️ PostgreSQL\nJobs · Articles")]:::db
        Redis[("⚡ Redis\nJob State · Cache")]:::db
    end

    ExtLLM(["🤖 LLM API\nClaude / GPT-4o"]):::external

    User -->|"1 - Submit URL or file"| REST
    REST -->|"2 - Create job record"| DB
    REST -->|"3 - Publish job"| PubSub
    REST -->|"4 - Return job ID"| User
    User -->|"5 - Poll status"| REST

    PubSub -->|"6 - Consume job"| Ingest
    Ingest --> CaptionCheck
    CaptionCheck -->|"Yes - use captions"| LLM
    CaptionCheck -->|"No - transcribe audio"| Whisper
    Whisper -->|"Transcript and timestamps"| LLM

    LLM -->|"Structure request"| ExtLLM
    ExtLLM -->|"Structured article"| LLM
    LLM -->|"Section timestamps"| Frames
    Frames -->|"Upload frames"| GCS
    GCS -->|"Public image URLs"| Assemble
    LLM -->|"Article text and structure"| Assemble

    Assemble -->|"Store article HTML"| DB
    Assemble -->|"Mark job complete"| DB
    workers -->|"Write cache"| Redis
    Redis -->|"Read cache"| workers

    DB -->|"7 - Return shareable URL"| REST
    REST -->|"7 - Shareable URL"| User
```

## Notes

- **GCS TTL**: Objects deleted automatically via GCS lifecycle policy after N days (set low during testing). PostgreSQL `expires_at` field mirrors this.
- **Caption fallback**: yt-dlp checks for manual captions first, then auto-generated, then falls back to Whisper.
- **Frame extraction timing**: ffmpeg extracts frames at section-start timestamps returned by the LLM structuring step — ensures screenshots align with article content.
- **LLM selection**: TBD after offline comparison of candidate models on sample videos.
