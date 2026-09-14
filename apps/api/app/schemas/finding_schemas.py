from uuid import UUID

from pydantic import BaseModel


class EvidenceRead(BaseModel):
	id: UUID
	file: str
	line_start: int | None
	line_end: int | None
	rule: str | None
	tool: str | None
	snippet: str | None

	model_config = {"from_attributes": True}


class FindingRead(BaseModel):
	id: UUID
	agent_id: str
	category: str
	title: str
	description: str
	severity: str
	confidence: float
	component: str | None
	correlation_id: str | None
	evidence: list[EvidenceRead]

	model_config = {"from_attributes": True}
"""Finding schemas will be implemented in Phase 9."""
