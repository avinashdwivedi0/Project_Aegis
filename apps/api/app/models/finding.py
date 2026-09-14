from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.models import AgentCategory, Severity

if TYPE_CHECKING:
	from app.models.analysis_run import AnalysisRun
	from app.models.evidence import Evidence
	from app.models.recommendation import Recommendation


class Finding(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	analysis_run_id: UUID = Field(foreign_key="analysisrun.id", index=True)
	agent_id: str
	category: AgentCategory
	title: str
	description: str
	severity: Severity
	confidence: float
	component: str | None = None
	correlation_id: str | None = Field(default=None, index=True)
	created_at: datetime = Field(default_factory=datetime.utcnow)

	analysis_run: "AnalysisRun" = Relationship(back_populates="findings")
	evidence: list["Evidence"] = Relationship(back_populates="finding")
	recommendation: Optional["Recommendation"] = Relationship(back_populates="finding")
