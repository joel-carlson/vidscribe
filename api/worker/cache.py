import json
import redis

from . import config
from .models import CaptionSegment

_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

def cache_transcript(job_id: str, captions: list[CaptionSegment]) -> None:
    """Cache the transcript for a given job ID in Redis.
    
    Args:
        job_id: The UUID of the job as a string.
        captions: List of caption segments to cache.
    """
    encoded_captions = json.dumps(captions)
    try: 
        _client.set(job_id, encoded_captions, ex=config.CACHE_EXPIRATION_SECONDS)
    except redis.RedisError as e:
        print(f"Error occurred while caching transcript for job {job_id}: {e}")  # Log the error


def get_cached_transcript(job_id: str) -> list[CaptionSegment] | None:
    """Retrieve the cached transcript for a given job ID from Redis.
    
    Args:
        job_id: The UUID of the job as a string.
        
    Returns:
        List of caption segments if found in cache, otherwise None.
    """
    try:
        encoded_captions = _client.get(job_id)
    except redis.RedisError as e:
        print(f"Error occurred while retrieving cached transcript for job {job_id}: {e}")  # Log the error
        return None
    if encoded_captions is not None:
        return json.loads(encoded_captions)
    return None


        
        
if __name__ == "__main__":
    # Example usage
    test_job_id : str = "test-job-id"
    test_captions : list[dict] = [
        {"start": 0.0, "end": 5.0, "text": "Hello world!"},
        {"start": 5.0, "end": 10.0, "text": "This is a test."}
    ]
    print("Caching transcript...")
    cache_transcript(test_job_id, test_captions)
    print("Retrieving cached transcript...")
    cached : list[CaptionSegment] | None = get_cached_transcript(test_job_id)
    print("Cached captions:", cached)