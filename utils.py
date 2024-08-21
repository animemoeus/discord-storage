import requests
from fastapi import HTTPException

import config

MAX_FILE_SIZE = 24  # MB


def validate_file_size_from_url(url: str):
    response = requests.head(str(url), timeout=5, allow_redirects=True)

    if not response.headers.get("Content-Length"):
        raise HTTPException(status_code=411, detail="Unable to get file size")

    file_size = int(response.headers.get("Content-Length")) / 1024

    if file_size > MAX_FILE_SIZE * 1024:
        raise HTTPException(status_code=413, detail="File too large")


def get_file_from_url(url: str):
    validate_file_size_from_url(url)

    response = requests.get(url, stream=True, allow_redirects=True)
    return response.raw


def upload_file_to_discord_server(file_data: bytes, file_name: str) -> dict:
    files = {file_name: file_data}
    response = requests.post(
        config.WEBHOOK_URL, files=files, data={"content": file_name}
    )

    response_json = response.json()
    return response_json
