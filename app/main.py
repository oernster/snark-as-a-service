from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.v1 import sarcasm
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
)

app.include_router(sarcasm.router, prefix="/api/v1/sarcasm")


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {
        "message": "Welcome. Expectations should be managed accordingly.",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "api": "/api/v1/sarcasm"
    }

