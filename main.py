from fastapi import FastAPI
from pydantic import AnyUrl, BaseModel

from utils import get_file_from_url, upload_file_to_discord_server

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class UploadFromURLPayload(BaseModel):
    file_url: AnyUrl
    file_name: str


@app.post("/upload-from-url/")
async def upload_from_url(payload: UploadFromURLPayload):
    file_url = str(payload.file_url)
    file_name = payload.file_name

    raw_file = get_file_from_url(file_url)
    discord_response = upload_file_to_discord_server(raw_file, file_name)

    # Format Discord webhook response
    result = discord_response["attachments"][0]

    return result
