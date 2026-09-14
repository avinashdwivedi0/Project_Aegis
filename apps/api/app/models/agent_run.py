from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, Relationship, SQLModel

from app.models import AgentCategory, AgentRunStatus

if TYPE_CHECKING:
	from app.models.analysis_run import AnalysisRun


class AgentRun(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	analysis_run_id: UUID = Field(foreign_key="analysisrun.id", index=True)
	agent_id: str
	category: AgentCategory
	status: AgentRunStatus = Field(default=AgentRunStatus.PENDING)
	started_at: datetime | None = None
	completed_at: datetime | None = None
	confidence: float | None = None
	raw_output: dict | None = Field(default=None, sa_column=Column(JSON))
	error_message: str | None = None

	analysis_run: "AnalysisRun" = Relationship(back_populates="agent_runs")
