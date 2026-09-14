from app.infrastructure.agents.quality_agent import AgentResult, interpret


class SecurityAgent:
	id = "security-agent"
	name = "Security Agent"
	category = "SECURITY"

	def __init__(self, provider: object) -> None:
		self.provider = provider

	def is_applicable(self, context: dict) -> bool:
		return bool(context.get("languages"))

	async def analyze(self, context: dict, tools: dict) -> AgentResult:
		return await interpret(self.provider, self.category, context, tools)