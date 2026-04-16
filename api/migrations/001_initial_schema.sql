CREATE TYPE status_enum AS ENUM (
    'pending',
    'in_progress',
    'completed',
    'failed'
 );
CREATE TABLE jobs(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
    status status_enum DEFAULT 'pending' NOT NULL, --shows the curent state of the job process
    video_url VARCHAR(2048) NOT NULL, --URL for the video such as yotuube or other services, future zoom
    created_at  TIMESTAMP DEFAULT NOW(), 
    updated_at  TIMESTAMP,
    expires_at  TIMESTAMP
);

CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()NOT NULL,
    job_id UUID references jobs(id) NOT NULL,
    title VARCHAR(2048), --Generated title for the article,
    content JSONB,
    created_at  TIMESTAMP DEFAULT NOW(), 
    updated_at  TIMESTAMP,
    expires_at  TIMESTAMP
);

