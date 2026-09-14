from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	from app.models.analysis_run import AnalysisRun
	from app.models.report import Report
	from app.models.user import User


class Project(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	user_id: UUID = Field(foreign_key="user.id", index=True)
	name: str
	source_type: str
	source_ref: str
	detected_stack: dict | None = Field(default=None, sa_column=Column(JSON))
	inventory: dict | None = Field(default=None, sa_column=Column(JSON))
	created_at: datetime = Field(default_factory=datetime.utcnow)

	user: "User" = Relationship(back_populates="projects")
	analysis_runs: list["AnalysisRun"] = Relationship(back_populates="project")
	reports: list["Report"] = Relationship(back_populates="project")
