from app.infrastructure.agents.quality_agent import AgentResult, interpret


class DependencyAgent:
	id = "dependency-agent"
	name = "Dependency Agent"
	category = "DEPENDENCY"

	def __init__(self, provider: object) -> None:
		self.provider = provider

	def is_applicable(self, context: dict) -> bool:
		return bool(context.get("dependencies"))

	async def analyze(self, context: dict, tools: dict) -> AgentResult:
		return await interpret(self.provider, self.category, context, tools)