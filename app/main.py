from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.api.v1 import sarcasm
from app.core.config import settings
from app.services.sarcasm_service import SarcasmService


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
)

templates = Jinja2Templates(directory="app/templates")

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
def root(request: Request):
    """Homepage: render the styled sarcasm page.

    (The plain-text API remains available at /api/v1/sarcasm/.)
    """

    quote = SarcasmService().get_quote()
    return templates.TemplateResponse(
        "sarcasm.html",
        {"request": request, "title": "SnarkAPI", "quote": quote},
    )


@app.get("/sarcasm", include_in_schema=False)
def sarcasm_page(request: Request):
    """Beautiful HTML page showing only the quote text."""

    quote = SarcasmService().get_quote()
    return templates.TemplateResponse(
        "sarcasm.html",
        {"request": request, "title": "SnarkAPI", "quote": quote},
    )

