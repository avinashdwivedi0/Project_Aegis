from app.infrastructure.agents.quality_agent import AgentResult, interpret


class DocumentationAgent:
	id = "documentation-agent"
	name = "Documentation Agent"
	category = "DOCUMENTATION"

	def __init__(self, provider: object) -> None:
		self.provider = provider

	def is_applicable(self, context: dict) -> bool:
		return True

	async def analyze(self, context: dict, tools: dict) -> AgentResult:
		return await interpret(self.provider, self.category, context, tools)