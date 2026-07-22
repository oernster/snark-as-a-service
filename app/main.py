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

PAGE_TITLE = "SnarkAPI: professional-grade condescension, on demand"
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# Serve files from ./static at /static
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(sarcasm.router, prefix="/api/v1/sarcasm")


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    """Browser-default favicon endpoint.

    We store the favicon as a PNG at ./static/favicon.png.
    """

    favicon_path = STATIC_DIR / "favicon.png"
    return FileResponse(
        path=str(favicon_path),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@app.get("/robots.txt", include_in_schema=False)
def robots_txt() -> FileResponse:
    """Crawler policy; must be served at the host root to be read."""

    return FileResponse(
        path=str(STATIC_DIR / "robots.txt"),
        media_type="text/plain",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml() -> FileResponse:
    """Sitemap for the snarkapi.com host, referenced from robots.txt."""

    return FileResponse(
        path=str(STATIC_DIR / "sitemap.xml"),
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@app.get("/", include_in_schema=False)
def root(request: Request):
    """Homepage: render the styled sarcasm page.

    (The plain-text API remains available at /api/v1/sarcasm/.)
    """

    quote = SarcasmService().get_quote()
    return templates.TemplateResponse(
        request=request,
        name="sarcasm.html",
        context={"title": PAGE_TITLE, "quote": quote},
    )


@app.get("/sarcasm", include_in_schema=False)
def sarcasm_page(request: Request):
    """Beautiful HTML page showing only the quote text."""

    quote = SarcasmService().get_quote()
    return templates.TemplateResponse(
        request=request,
        name="sarcasm.html",
        context={"title": PAGE_TITLE, "quote": quote},
    )

