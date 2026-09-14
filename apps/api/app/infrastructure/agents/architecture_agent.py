from app.infrastructure.agents.quality_agent import AgentResult, interpret


class ArchitectureAgent:
	id = "architecture-agent"
	name = "Architecture Agent"
	category = "ARCHITECTURE"

	def __init__(self, provider: object) -> None:
		self.provider = provider

	def is_applicable(self, context: dict) -> bool:
		return bool(context.get("languages"))

	async def analyze(self, context: dict, tools: dict) -> AgentResult:
		return await interpret(self.provider, self.category, context, tools)