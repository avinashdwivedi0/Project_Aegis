from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	from app.models.project import Project


class Report(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	project_id: UUID = Field(foreign_key="project.id", index=True)
	analysis_run_id: UUID
	format: str
	content: dict = Field(sa_column=Column(JSON))
	created_at: datetime = Field(default_factory=datetime.utcnow)

	project: "Project" = Relationship(back_populates="reports")
