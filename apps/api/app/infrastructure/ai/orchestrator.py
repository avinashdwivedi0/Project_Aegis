import asyncio
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.infrastructure.agents import AGENT_REGISTRY
from app.infrastructure.agents.quality_agent import AgentResult
from app.infrastructure.ai.provider_factory import get_ai_provider
from app.infrastructure.analyzers.architecture_scan import architecture_scan
from app.infrastructure.analyzers.complexity_scan import complexity_scan
from app.infrastructure.analyzers.dependency_scan import dependency_scan
from app.infrastructure.analyzers.doc_scan import doc_scan
from app.infrastructure.analyzers.lint_scan import lint_scan
from app.infrastructure.analyzers.security_scan import security_scan
from app.infrastructure.analyzers.test_scan import test_scan


class AnalysisState(TypedDict):
	context: dict
	results: dict[str, AgentResult | Exception]


async def empty_agent(context: dict) -> AgentResult:
	return AgentResult()


async def execute_agents(
	context: dict,
	agents: dict[str, object] | None = None,
	provider: object | None = None,
) -> dict[str, AgentResult | Exception]:
	if agents is None:
		provider = provider or get_ai_provider()
		instances = {agent_id: agent(provider) for agent_id, agent in AGENT_REGISTRY.items()}
		selected = {agent_id: agent for agent_id, agent in instances.items() if agent.is_applicable(context)}
		tools = collect_tools(context)
		calls = (agent.analyze(context, tools.get(agent.category, {})) for agent in selected.values())
	else:
		selected = agents
		calls = (agent(context) for agent in selected.values())
	values = await asyncio.gather(
		*calls, return_exceptions=True
	)
	return dict(zip(selected, values, strict=True))


def collect_tools(context: dict) -> dict[str, dict]:
	root_value = context.get("source_root")
	if not root_value:
		return {}
	root = Path(root_value)
	tool_context = type("ToolContext", (), context)()
	return {
		"SECURITY": security_scan(root, tool_context),
		"CODE_QUALITY": {"lint": lint_scan(root, tool_context), "complexity": complexity_scan(root, tool_context)},
		"TESTING": test_scan(root, tool_context),
		"ARCHITECTURE": architecture_scan(root, tool_context),
		"DEPENDENCY": dependency_scan(root, tool_context),
		"DOCUMENTATION": doc_scan(root, tool_context),
	}


class AIOrchestrator:
	def build_graph(self, context: dict) -> StateGraph:
		graph = StateGraph(AnalysisState)

		async def run_agents(state: AnalysisState) -> dict:
			return {"results": await execute_agents(state["context"])}

		graph.add_node("agents", run_agents)
		graph.set_entry_point("agents")
		graph.add_edge("agents", END)
		return graph.compile()

	async def execute(self, context: dict) -> dict[str, AgentResult | Exception]:
		state = await self.build_graph(context).ainvoke({"context": context, "results": {}})
		return state["results"]
