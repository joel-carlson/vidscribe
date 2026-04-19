import os 

CACHE_EXPIRATION_SECONDS = 3600  # Cache expiration time in seconds (1 hour)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
#EOF