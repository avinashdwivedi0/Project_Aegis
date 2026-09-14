from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	from app.models.project import Project


class User(SQLModel, table=True):
	id: UUID = Field(default_factory=uuid4, primary_key=True)
	email: str = Field(unique=True, index=True)
	password_hash: str
	name: str | None = None
	created_at: datetime = Field(default_factory=datetime.utcnow)

	projects: list["Project"] = Relationship(back_populates="user")
