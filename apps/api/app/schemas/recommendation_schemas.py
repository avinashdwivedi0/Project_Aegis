from uuid import UUID

from pydantic import BaseModel


class RecommendationRead(BaseModel):
	id: UUID
	finding_id: UUID
	reasoning: str
	impact: str
	action: str
	reference: str | None

	model_config = {"from_attributes": True}


class RecommendationOutput(BaseModel):
	reasoning: str
	impact: str
	action: str
	reference: str | None = None
"""Recommendation schemas will be implemented in Phase 9."""
