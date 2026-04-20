from google.cloud import storage
from google.auth.credentials import AnonymousCredentials

from .config import GCS_BUCKET_NAME, GCS_ENDPOINT_URL, GCS_PUBLIC_URL_BASE, GCS_PROJECT_ID


_client: storage.Client | None = None

def _get_client() -> storage.Client:
    global _client
    if _client is None:
        if GCS_ENDPOINT_URL:
            # Local emulator — anonymous credentials, custom endpoint
            _client = storage.Client(
                credentials=AnonymousCredentials(),
                project=GCS_PROJECT_ID,
                client_options={"api_endpoint": GCS_ENDPOINT_URL}
            )
        else:
            # Production — use workload identity / application default credentials
            _client = storage.Client(project=GCS_PROJECT_ID)
    return _client


def _ensure_bucket(bucket: storage.Bucket) -> None:
    if GCS_ENDPOINT_URL and not bucket.exists():
        bucket.create()

def upload_frames_to_gcs(frame_paths: list[str], job_id: str) -> list[str]:
    """Upload extracted frames to Google Cloud Storage and return their public URLs.

    Args:
        frame_paths: List of local file paths to the extracted frames.
        job_id: Used to organize frames in GCS under a common prefix.

    Returns:
        List of public URLs for the uploaded frames.
    """
    # Get bucket from the client
    bucket: storage.Bucket = _get_client().bucket(GCS_BUCKET_NAME)
    _ensure_bucket(bucket)
                         
    public_urls: list[str] = []
    for frame_path in frame_paths:
        frame_name = frame_path.split("/")[-1]
        blob : storage.Blob = bucket.blob(f"{job_id}/{frame_name}")
        blob.upload_from_filename(frame_path)
        if GCS_ENDPOINT_URL:
            public_urls.append(f"{GCS_ENDPOINT_URL}/download/storage/v1/b/{GCS_BUCKET_NAME}/o/{job_id}%2F{frame_name}?alt=media")
        else:
            public_urls.append(f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{job_id}/{frame_name}")
        
    
    return public_urls


def upload_video_to_gcs(video_path: str, job_id: str) -> str:
    """Upload the downloaded video to Google Cloud Storage and return its public URL.

    Args:
        video_path: Local file path to the downloaded video.
        job_id: Used to organize the video in GCS under a common prefix.
    Returns:
        Public URL for the uploaded video.
    """
    bucket: storage.Bucket = _get_client().bucket(GCS_BUCKET_NAME)
    _ensure_bucket(bucket)
                         
    video_name : str = "video.mp4"
    blob : storage.Blob = bucket.blob(f"{job_id}/{video_name}")
    blob.upload_from_filename(video_path)
    return f"gs://{GCS_BUCKET_NAME}/{job_id}/{video_name}"
        

def download_from_gcs(gcs_path: str, local_path: str)-> None:
    """Download a file from Google Cloud Storage to local temp storage.

    Args:
        gcs_path: GCS path in the format "gs://bucket_name/path/to/file".
        local_path: Local file path where the file will be downloaded.

    Returns:
        Local file path to the downloaded file.
    """
    bucket : storage.Bucket = _get_client().bucket(GCS_BUCKET_NAME)
    blob_name : str = "/".join(gcs_path.split("/")[3:])  # This gets the job id from the gcs path and strips the gs://bucket/
    bucket.blob(blob_name).download_to_filename(local_path)
        
    
if __name__ == "__main__":                                                                                                                    
    FRAME_PATHS = ["/tmp/example-job-id/frame_10.0.jpg", "/tmp/example-job-id/frame_30.0.jpg", "/tmp/example-job-id/frame_60.0.jpg"]          
    JOB_ID = "example-job-id"                                                                                                                 
                                                                                                                                            
    print("Uploading frames to GCS...")                                                                                                       
    public_urls = upload_frames_to_gcs(FRAME_PATHS, JOB_ID)
    for url in public_urls:                                                                                                                   
        print(url)
                                                                                                                                            
    print("Uploading video to GCS...")
    gcs_path = upload_video_to_gcs("/tmp/example-job-id.mp4", JOB_ID)
    print(f"GCS path: {gcs_path}")  
    
    
    print("Testing download from GCS...")
    download_from_gcs(gcs_path, "/tmp/example-job-id-downloaded.mp4")
    print("Download complete. Local path: /tmp/example-job-id-downloaded.mp4")
    
#EOF