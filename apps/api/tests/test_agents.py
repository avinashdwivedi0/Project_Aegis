import pytest

from app.infrastructure.agents import AGENT_REGISTRY
from app.infrastructure.ai.orchestrator import execute_agents


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0

    async def complete(self, system: str, prompt: str, response_model=None, temperature: float = 0.2) -> str:
        self.calls += 1
        return '{"findings": [], "evidence": [], "metrics": {}, "confidence": 0.8}'


@pytest.mark.asyncio
async def test_registry_runs_all_applicable_agents() -> None:
    provider = FakeProvider()
    context = {"languages": {"Python": 1}, "dependencies": {"requirements.txt": ["fastapi"]}}
    results = await execute_agents(context, provider=provider)
    assert set(results) == set(AGENT_REGISTRY)
    assert provider.calls == 6
    assert all(not isinstance(result, Exception) for result in results.values())
