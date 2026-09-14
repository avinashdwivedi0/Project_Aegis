import pytest

from app.infrastructure.ai.provider_factory import FallbackProvider


class FailingProvider:
    async def complete(self, *args, **kwargs):
        raise RuntimeError("offline")


class WorkingProvider:
    async def complete(self, *args, **kwargs):
        return "OK"


@pytest.mark.asyncio
async def test_fallback_provider_uses_next_provider() -> None:
    provider = FallbackProvider([FailingProvider(), WorkingProvider()])
    assert await provider.complete("system", "prompt") == "OK"
