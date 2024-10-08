import sentry_sdk
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from pydantic import AnyUrl, BaseModel

from config import SENTRY_DSN
from utils import get_file_from_url, upload_file_to_discord_server, refresh_expired_url

sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{path:path}")
async def index(path: str, width: int | None = None, height: int | None = None):
    try:
        refreshed_url = refresh_expired_url(path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    extra_params = ""
    if width and height:
        extra_params = f"width={width}&height={height}&"

    redirect_url = f"{refreshed_url}{extra_params}"
    return RedirectResponse(url=redirect_url, status_code=307)


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
