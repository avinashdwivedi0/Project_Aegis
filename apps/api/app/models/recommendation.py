from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	from app.models.finding import Finding


class Recommendation(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	finding_id: UUID = Field(foreign_key="finding.id", unique=True)
	reasoning: str
	impact: str
	action: str
	reference: str | None = None

	finding: "Finding" = Relationship(back_populates="recommendation")
