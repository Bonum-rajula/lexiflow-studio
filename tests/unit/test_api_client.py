# tests/unit/test_api_client.py
import pytest
import requests
import requests_mock
from src.services.api_client import APIClient
from src.services.schemas import UploadResponse, AnswerResponse


@pytest.fixture
def api_client():
    """Returns an APIClient instance with a dummy base URL."""
    return APIClient(base_url="http://test-backend")


def test_upload_pdf_success(api_client):
    """Test successful PDF upload."""
    with requests_mock.Mocker() as m:
        m.post(
            "http://test-backend/upload/",
            json={
                "filename": "test.pdf",
                "num_chunks": 5,
                "status": "success",
                "message": "Ingestion complete."
            },
            status_code=200,
        )
        response = api_client.upload_pdf(b"dummy pdf content", "test.pdf")
        
        assert isinstance(response, UploadResponse)
        assert response.filename == "test.pdf"
        assert response.num_chunks == 5
        assert response.status == "success"


def test_ask_question_success(api_client):
    """Test successful question answering."""
    with requests_mock.Mocker() as m:
        m.post(
            "http://test-backend/ask/",
            json={
                "answer": "This is the final answer.",
                "chunks_used": 3,
                "critique": '{"relevance_score": 0.9}',
                "retry_count": 0,
                "error": None,
            },
            status_code=200,
        )
        response = api_client.ask_question("What is this about?")
        
        assert isinstance(response, AnswerResponse)
        assert response.answer == "This is the final answer."
        assert response.chunks_used == 3
        assert response.retry_count == 0


def test_upload_retry_on_failure(api_client):
    """
    Test that the client retries on connection errors and eventually succeeds.
    """
    with requests_mock.Mocker() as m:
        # Simulate failure for the first two attempts, success on the third.
        m.post(
            "http://test-backend/upload/",
            [
                {"exc": requests.exceptions.ConnectionError},
                {"exc": requests.exceptions.ConnectionError},
                {"json": {"filename": "test.pdf", "num_chunks": 1, "status": "success", "message": "OK"}},
            ]
        )
        response = api_client.upload_pdf(b"dummy", "test.pdf")
        assert response.status == "success"


def test_ask_question_timeout(api_client):
    """Test that the client retries on timeouts and raises after 3 attempts."""
    with requests_mock.Mocker() as m:
        m.post(
            "http://test-backend/ask/",
            [
                {"exc": requests.exceptions.Timeout},
                {"exc": requests.exceptions.Timeout},
                {"exc": requests.exceptions.Timeout},
            ]
        )
        with pytest.raises(requests.exceptions.Timeout):
            api_client.ask_question("What is this?")