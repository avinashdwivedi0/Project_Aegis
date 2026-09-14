from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProjectCreate(BaseModel):
	name: str
	git_url: str


class ProjectRead(BaseModel):
	id: UUID
	name: str
	source_type: str
	source_ref: str
	detected_stack: dict | None
	inventory: dict | None
	created_at: datetime

	model_config = {"from_attributes": True}
