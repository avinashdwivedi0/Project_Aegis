from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models import AgentRunStatus, AnalysisStatus


class AnalysisRunRead(BaseModel):
	id: UUID
	project_id: UUID
	status: AnalysisStatus
	started_at: datetime
	completed_at: datetime | None
	overall_score: float | None
	dimension_scores: dict | None
	agent_runs: list["AgentRunRead"] = Field(default_factory=list)

	model_config = {"from_attributes": True}


class AgentRunRead(BaseModel):
	id: UUID
	agent_id: str
	category: str
	status: AgentRunStatus
	confidence: float | None
	error_message: str | None

	model_config = {"from_attributes": True}
