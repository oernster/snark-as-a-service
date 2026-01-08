from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1 import sarcasm
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
)

# Serve files from ./static at /static
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(sarcasm.router, prefix="/api/v1/sarcasm")


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    """Browser-default favicon endpoint.

    We store the favicon as a PNG at ./static/favicon.png.
    """

    favicon_path = Path(__file__).resolve().parent.parent / "static" / "favicon.png"
    return FileResponse(
        path=str(favicon_path),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {
        "message": "Welcome. Expectations should be managed accordingly.",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "api": "/api/v1/sarcasm"
    }

