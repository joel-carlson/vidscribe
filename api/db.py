import asyncpg
import config
from models import JobResponse
from datetime import datetime


class Database:
    def __init__(self):
        self._pool = None 
    
    @classmethod 
    async def create(cls) -> "Database":
        instance : "Database" = cls()
        instance._pool = await asyncpg.create_pool(config.DATABASE_URL)
        return instance
        

    async def disconnect(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
            
            
    async def create_job(self, video_url: str) -> JobResponse:
        async with self._pool.acquire() as conn:
            row  = await conn.fetchrow(
                "INSERT INTO jobs ( video_url) VALUES ($1) RETURNING id, status, created_at",
                video_url
            )
            return JobResponse(
                job_id = row["id"],
                status = row["status"],
                created_at = row["created_at"],
                video_url = video_url
            ) 
        
    


    
        