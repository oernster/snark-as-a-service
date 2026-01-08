import json
from pathlib import Path
from typing import List

from app.models.quote import Quote


class SarcasmService:
    def __init__(self, quotes_path: str | None = None) -> None:
        self._quotes = self._load_quotes(quotes_path or "app/data/quotes.json")

    def get_quote(self) -> Quote:
        return Quote(text=self._random_choice())

    def _load_quotes(self, path: str) -> List[str]:
        try:
            with open(Path(path), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load quotes. Falling back. Reason: {e}")
            return self._default_quotes()

    def _random_choice(self) -> str:
        import random

        return random.choice(self._quotes)

    @staticmethod
    def _default_quotes() -> List[str]:
        return [
            "Fallback activated. Sarcasm reserves at 1%.",
            "You’re trying. That’s the problem.",
        ]
