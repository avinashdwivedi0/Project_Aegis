from uuid import UUID

from pydantic import BaseModel


class ReportRead(BaseModel):
	id: UUID
	project_id: UUID
	analysis_run_id: UUID
	format: str
	content: dict

	model_config = {"from_attributes": True}
