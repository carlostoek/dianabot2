from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware


class NarrativeContextMiddleware(BaseMiddleware):
    """Attach a simple narrative context to handler data."""

    async def __call__(self, handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]], event: Any, data: Dict[str, Any]) -> Any:
        data.setdefault("narrative_context", {})
        return await handler(event, data)
