from typing import Any

import asyncpg
import config
from models import JobResponse
from uuid import UUID
from fastapi import HTTPException
from http import HTTPStatus
from datetime import datetime, timedelta , timezone
class Database:
    def __init__(self):
        self._pool = None 
    
    @classmethod 
    async def create(cls) -> "Database":
        """
          Create a Database instance with an active asyncpg connection pool.
                                                                                                                                                                                                                                    
            Returns:                                                                                                                                                                                                                          
                Connected Database instance ready for queries.
        """  
        instance : "Database" = cls()
        instance._pool = await asyncpg.create_pool(config.DATABASE_URL)
        return instance
        

    async def disconnect(self) -> None:
        """Close the connection pool if one exists."""
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
            
            
    async def create_job(self, video_url: str) -> JobResponse:
        """
        Insert a new job record and return its initial state.
                                                                                                                                                                                                                                            
        Args:                                                                                                                                                                                                                             
            video_url: URL of the video to process.
                                                                                                                                                                                                                                            
        Returns:        
            JobResponse containing the new job's id, status, and created_at.
        """      
        
        
        async with self._pool.acquire() as conn:
            row  = await conn.fetchrow(
                "INSERT INTO jobs ( video_url) VALUES ($1) RETURNING id, status, created_at",
                video_url
            )
            return JobResponse(
                job_id = row["id"],
                status = row["status"],
                created_at = row["created_at"],
                expires_at= row["created_at"] + timedelta(hours =1), #epire 1 hour after, temporary
                video_url = video_url
            ) 
            
    # Give Job ID, return status. Status endpoint
    async def get_job_status(self, job_id : UUID) -> str:
        """ Fetch the current processing status for a job.                                                                                                                                                                             
                                                                                                                                                                                                                                            
            Args:
                job_id: UUID of the job to look up.                                                                                                                                                                                       
                        
            Returns:
                Status string from the jobs table.
                                                                                                                                                                                                                                            
            Raises:
                HTTPException: 404 if no job with the given ID exists.                                                                                                                                                                    
        """ 
        async with self._pool.acquire() as conn:
            row: asyncpg.Record = await conn.fetchrow(
                "SELECT status FROM jobs WHERE id = $1",
                job_id
            )
            if row is None:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND)        # 404 
            return row["status"]
    
    async def get_article_id(self, job_id : UUID) -> UUID:
        """ Fetch the article_id for a completed job.                                                                                                                                                                             
                                                                                                                                                                                                                                            
            Args:
                job_id: UUID of the job to look up.
                
            Returns:
                article_id UUID from the jobs table.
        """
        async with self._pool.acquire() as conn:
            row: asyncpg.Record = await conn.fetchrow(
                "SELECT id FROM articles WHERE job_id = $1",
                job_id
            )
            if row is None:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND)        # 404 
            return row["id"]


        
    async def get_article_content(self, article_id : UUID) -> dict[str, Any] :
        """ Fetch the article text for a completed job.                                                                                                                                                                             
                                                                                                                                                                                                                                            
            Args:
                article_id: UUID of the article to look up.
            Returns: 
                json object containing article text and metadata
                
        """
        async with self._pool.acquire() as conn:
           row : asyncpg.Record = await conn.fetchrow(
               "SELECT content, expires_at FROM articles WHERE id = $1",
               article_id
           )
           if row is None:
               raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
           if row["expires_at"] < datetime.now(timezone.utc):
                raise HTTPException(status_code=HTTPStatus.GONE, detail="Article has expired")
           return row["content"] 

    