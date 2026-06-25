# src/services/api_client.py
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from loguru import logger

from .schemas import UploadResponse, AnswerResponse


class APIClient:
    """
    Client for communicating with the LexiFlow backend API.
    
    DIP Compliance: This client is the only place that knows about HTTP.
    Components use this client, not `requests` directly.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    # ------------------------------------------------------------------
    # Upload Endpoint
    # ------------------------------------------------------------------
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.exceptions.ConnectionError,
                                       requests.exceptions.Timeout,
                                       requests.exceptions.RequestException)),
        reraise=True,
    )
    def upload_pdf(self, file_content: bytes, filename: str) -> UploadResponse:
        """
        Upload a PDF to the backend for ingestion.
        
        Args:
            file_content: Raw bytes of the PDF file.
            filename: Name of the file (for metadata).
            
        Returns:
            UploadResponse: Status of the ingestion.
            
        Raises:
            requests.exceptions.RequestException: If all retries fail.
        """
        logger.info(f"📤 Uploading PDF: {filename} (size: {len(file_content)} bytes)")

        url = f"{self.base_url}/upload/"
        files = {"file": (filename, file_content, "application/pdf")}

        response = requests.post(url, files=files, timeout=30.0)
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Upload successful: {data.get('message')}")
        return UploadResponse(**data)

    # ------------------------------------------------------------------
    # Ask Endpoint
    # ------------------------------------------------------------------
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.exceptions.ConnectionError,
                                       requests.exceptions.Timeout,
                                       requests.exceptions.RequestException)),
        reraise=True,
    )
    def ask_question(self, question: str) -> AnswerResponse:
        """
        Ask a question to the multi-agent RAG system.
        
        Args:
            question: The user's query.
            
        Returns:
            AnswerResponse: The final answer, chunks used, and critique.
            
        Raises:
            requests.exceptions.RequestException: If all retries fail.
        """
        logger.info(f"❓ Asking question: '{question[:50]}...'")

        url = f"{self.base_url}/ask/"
        payload = {"question": question}

        response = requests.post(url, json=payload, timeout=60.0)  # Allow longer for agents
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Answer generated using {data.get('chunks_used', 0)} chunks.")
        return AnswerResponse(**data)

    # Add to APIClient class in src/services/api_client.py

    def health(self) -> bool:
        """Check if the backend API is reachable."""
        try:
            url = f"{self.base_url}/health"
            response = requests.get(url, timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False