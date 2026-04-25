import pytest
from uuid import uuid4
from starlette.testclient import TestClient


def test_root_returns_html(client: TestClient):
    """GET / returns 200 with HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_status_page_returns_html(client: TestClient):
    """GET /status/{job_id} renders the status HTML page."""
    response = client.get(f"/status/{uuid4()}", follow_redirects=False)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_post_jobs_redirects_303(client: TestClient):
    """POST /jobs creates a job and redirects to /status/{job_id} with 303."""
    response = client.post("/jobs", data={"video_url": "https://www.youtube.com/watch?v=test"}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/status/")


def test_get_job_status_200(client: TestClient):
    """GET /jobs/{job_id} returns pending for a newly created job."""
    post = client.post("/jobs", data={"video_url": "https://www.youtube.com/watch?v=test"}, follow_redirects=False)
    job_id = post.headers["location"].split("/status/")[1]
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert "pending" in response.text


def test_get_job_status_404(client: TestClient):
    """GET /jobs/{unknown_id} returns 404."""
    response = client.get(f"/jobs/{uuid4()}")
    assert response.status_code == 404


def test_get_article_by_job_404(client: TestClient):
    """GET /articles/by-job/{job_id} returns 404 before worker runs."""
    post = client.post("/jobs", data={"video_url": "https://www.youtube.com/watch?v=test"}, follow_redirects=False)
    job_id = post.headers["location"].split("/status/")[1]
    response = client.get(f"/articles/by-job/{job_id}")
    assert response.status_code == 404


def test_get_article_content_404(client: TestClient):
    """GET /articles/{unknown_id} returns 404."""
    response = client.get(f"/articles/{uuid4()}")
    assert response.status_code == 404
