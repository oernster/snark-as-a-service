from fastapi import APIRouter, Depends

from app.models.quote import Quote
from app.services.sarcasm_service import SarcasmService

router = APIRouter()


def get_sarcasm_service() -> SarcasmService:
    return SarcasmService()


@router.get("/", response_model=Quote)
def get_sarcastic_quote(
    service: SarcasmService = Depends(get_sarcasm_service),
) -> Quote:
    return service.get_quote()
