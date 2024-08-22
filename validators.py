import requests
from fastapi import HTTPException

from config import MAX_FILE_SIZE


def validate_file_size_from_url(url: str):
    response = requests.head(url, timeout=5, allow_redirects=True)
    if not response.ok:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Unable to get the information from {url}",
        )

    content_length = response.headers.get("Content-Length")
    if not content_length:
        raise HTTPException(
            status_code=411,
            detail="Content-Length header is missing; unable to determine file size",
        )

    file_size = int(content_length) / 1024  # File size in KB
    if file_size > MAX_FILE_SIZE * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large: {file_size:.2f} KB exceeds the maximum allowed size of {MAX_FILE_SIZE * 1024:.2f} KB.",
        )
