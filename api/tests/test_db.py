import pytest
from uuid import uuid4
from http import HTTPStatus
from fastapi import HTTPException

from db import Database


async def test_create_job_returns_job_response(db: Database):
    """Happy path: create_job returns a JobResponse with expected fields."""
    response = await db.create_job("https://www.youtube.com/watch?v=test")
    assert response.job_id is not None
    assert response.status == "pending"
    assert response.video_url == "https://www.youtube.com/watch?v=test"


async def test_create_job_status_is_pending(db: Database):
    """Newly created jobs always start in pending status."""
    response = await db.create_job("https://www.youtube.com/watch?v=test2")
    assert response.status == "pending"


async def test_get_job_status_returns_pending(db: Database):
    """Roundtrip: create a job then read its status back."""
    created = await db.create_job("https://www.youtube.com/watch?v=test3")
    status = await db.get_job_status(created.job_id)
    assert status == "pending"


async def test_get_job_status_raises_404_for_unknown(db: Database):
    """get_job_status raises 404 for a job ID that does not exist."""
    with pytest.raises(HTTPException) as exc_info:
        await db.get_job_status(uuid4())
    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND


async def test_get_article_id_raises_404_when_no_article(db: Database):
    """get_article_id raises 404 when no article exists for a job."""
    created = await db.create_job("https://www.youtube.com/watch?v=test4")
    with pytest.raises(HTTPException) as exc_info:
        await db.get_article_id(created.job_id)
    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND


async def test_get_article_content_raises_410_when_expired(db: Database):
    """get_article_content raises 410 Gone when article expires_at is in the past."""
    created = await db.create_job("https://www.youtube.com/watch?v=test5")
    async with db._pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO articles (job_id, title, content, created_at, expires_at)
               VALUES ($1, 'Test', '{"sections": []}', NOW(), NOW() - INTERVAL '1 day')""",
            created.job_id
        )
        row = await conn.fetchrow("SELECT id FROM articles WHERE job_id = $1", created.job_id)
    with pytest.raises(HTTPException) as exc_info:
        await db.get_article_content(row["id"])
    assert exc_info.value.status_code == HTTPStatus.GONE
