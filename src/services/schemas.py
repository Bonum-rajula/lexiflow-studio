# src/services/schemas.py
from typing import Optional
from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response model for the /upload endpoint."""
    filename: str
    num_chunks: int
    status: str
    message: str


class AnswerResponse(BaseModel):
    """Response model for the /ask endpoint."""
    answer: str
    chunks_used: int
    critique: Optional[str] = None
    retry_count: int = 0
    error: Optional[str] = None


# We don't strictly need a request model on the client,
# but defining one improves type safety.
class AskRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str