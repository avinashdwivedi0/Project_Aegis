from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, Relationship, SQLModel

from app.models import AnalysisStatus

if TYPE_CHECKING:
	from app.models.agent_run import AgentRun
	from app.models.finding import Finding
	from app.models.project import Project


class AnalysisRun(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	project_id: UUID = Field(foreign_key="project.id", index=True)
	status: AnalysisStatus = Field(default=AnalysisStatus.PENDING)
	started_at: datetime = Field(default_factory=datetime.utcnow)
	completed_at: datetime | None = None
	overall_score: float | None = None
	dimension_scores: dict | None = Field(default=None, sa_column=Column(JSON))

	project: "Project" = Relationship(back_populates="analysis_runs")
	agent_runs: list["AgentRun"] = Relationship(back_populates="analysis_run")
	findings: list["Finding"] = Relationship(back_populates="analysis_run")
