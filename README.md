# Sarcasm API

A minimal FastAPI service that returns a sarcastic quote.

## Run
uvicorn app.main:app --reload

## Endpoint
GET /api/v1/sarcasm/

## Example Response
{
  "text": "You have unlimited potential. Unfortunately, it’s mostly theoretical."
}

## Tests
pytest
