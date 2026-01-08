from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from app.services.sarcasm_service import SarcasmService

router = APIRouter()


def get_sarcasm_service() -> SarcasmService:
    return SarcasmService()


@router.get("/", response_class=PlainTextResponse)
def get_sarcastic_quote(
    service: SarcasmService = Depends(get_sarcasm_service),
) -> str:
    # Plain text response (no JSON wrapper)
    return service.get_quote()
