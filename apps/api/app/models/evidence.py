from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	from app.models.finding import Finding


class Evidence(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	finding_id: UUID = Field(foreign_key="finding.id", index=True)
	file: str
	line_start: int | None = None
	line_end: int | None = None
	rule: str | None = None
	tool: str | None = None
	snippet: str | None = None

	finding: "Finding" = Relationship(back_populates="evidence")
