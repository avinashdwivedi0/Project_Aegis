from uuid import UUID

from app.models import Finding
from app.repositories.finding_repository import FindingRepository


class FindingService:
	def __init__(self, repository: FindingRepository) -> None:
		self.repository = repository

	async def get(self, finding_id: UUID, user_id: UUID) -> Finding | None:
		return await self.repository.get_for_user(finding_id, user_id)
