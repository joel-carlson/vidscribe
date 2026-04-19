import os 

CACHE_EXPIRATION_SECONDS = 3600  # Cache expiration time in seconds (1 hour)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
GCS_PUBLIC_URL_BASE = os.getenv("GCS_PUBLIC_URL_BASE", "http://localhost:4443/") #Changing in production
GCS_PROJECT_ID = os.getenv("GCS_PROJECT_ID", "local") #Change this when deploying
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "vidscribe-frames")
GCS_ENDPOINT_URL = os.getenv("GCS_ENDPOINT_URL", "http://localhost:4443")
#EOF