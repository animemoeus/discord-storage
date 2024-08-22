import requests
from fastapi import HTTPException

import config
from validators import validate_file_size_from_url


def get_file_from_url(url: str):
    validate_file_size_from_url(url)

    response = requests.get(url, stream=True, allow_redirects=True)

    if not response.ok:
        raise HTTPException(
            status_code=response.status_code, detail=f"Unable to get the file for {url}"
        )

    return response.raw


def upload_file_to_discord_server(file_data: bytes, file_name: str) -> dict:
    files = {file_name: file_data}

    response = requests.post(
        config.WEBHOOK_URL, files=files, data={"content": file_name}
    )

    if not response.ok:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Unable to upload the file to Discord Server",
        )

    response_json = response.json()
    return response_json
