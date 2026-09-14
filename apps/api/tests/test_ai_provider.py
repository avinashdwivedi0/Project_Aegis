from typing import Self

import pytest
from pydantic import BaseModel

from app.infrastructure.ai.openrouter_provider import OpenRouterProvider


class Answer(BaseModel):
    value: int


class FakeResponse:
    def __init__(self, content: str) -> None:
        self.content = content

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {"choices": [{"message": {"content": self.content}}]}


class FakeClient:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = responses

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def post(self, *args: object, **kwargs: object) -> FakeResponse:
        return self.responses.pop(0)


@pytest.mark.asyncio
async def test_complete_retries_invalid_structured_output(monkeypatch) -> None:
    responses = [FakeResponse('{"value":"bad"}'), FakeResponse('{"value":7}')]
    monkeypatch.setattr(
        "app.infrastructure.ai.openrouter_provider.httpx.AsyncClient",
        lambda **kwargs: FakeClient(responses),
    )
    result = await OpenRouterProvider().complete("system", "prompt", Answer)
    assert Answer.model_validate_json(result).value == 7


@pytest.mark.asyncio
async def test_complete_returns_plain_text(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.infrastructure.ai.openrouter_provider.httpx.AsyncClient",
        lambda **kwargs: FakeClient([FakeResponse("OK")]),
    )
    assert await OpenRouterProvider().complete("system", "prompt") == "OK"