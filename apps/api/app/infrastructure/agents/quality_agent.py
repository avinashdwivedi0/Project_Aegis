from typing import Protocol

from pydantic import BaseModel, Field


class Finding(BaseModel):
	title: str
	description: str
	severity: str
	confidence: float
	component: str | None = None


class Evidence(BaseModel):
	file: str
	line_start: int | None = None
	line_end: int | None = None
	rule: str | None = None
	tool: str | None = None
	snippet: str | None = None


class AgentResult(BaseModel):
	findings: list[Finding] = Field(default_factory=list)
	evidence: list[Evidence] = Field(default_factory=list)
	metrics: dict[str, float] = Field(default_factory=dict)
	confidence: float = 0.0


class QualityAgent(Protocol):
	id: str
	name: str
	category: str

	def is_applicable(self, context: dict) -> bool: ...

	async def analyze(self, context: dict, tools: dict) -> AgentResult: ...


async def interpret(provider: object, category: str, context: dict, tools: dict) -> AgentResult:
	system = f"You are the {category} software quality agent. Use only supplied evidence."
	prompt = f"Project context: {context}\nDeterministic evidence: {tools}"
	return await provider.complete(system, prompt, response_model=AgentResult)  # type: ignore[attr-defined]