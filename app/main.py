from fastapi import FastAPI

from app.api.v1 import sarcasm
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
)

app.include_router(sarcasm.router, prefix="/api/v1/sarcasm")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome. Expectations should be managed accordingly."}
