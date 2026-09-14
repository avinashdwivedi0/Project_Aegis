import pytest

from app.infrastructure.ai.orchestrator import AgentResult, execute_agents


async def failing_agent(context: dict) -> AgentResult:
    raise RuntimeError("agent failed")


async def passing_agent(context: dict) -> AgentResult:
    return AgentResult()


@pytest.mark.asyncio
async def test_agent_failure_does_not_stop_other_agents() -> None:
    results = await execute_agents(
        {},
        {"failed": failing_agent, "passed": passing_agent},
    )
    assert isinstance(results["failed"], RuntimeError)
    assert results["passed"] == AgentResult()