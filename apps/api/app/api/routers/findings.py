from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.repositories.finding_repository import FindingRepository
from app.schemas.finding_schemas import FindingRead

router = APIRouter(prefix="/findings", tags=["findings"])


@router.get("/{finding_id}", response_model=dict)
async def get_finding(
	finding_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	finding = await FindingRepository(session).get_for_user(finding_id, user.id)
	if finding is None:
		raise HTTPException(status_code=404, detail="finding not found")
	return {"success": True, "data": FindingRead.model_validate(finding, from_attributes=True).model_dump(mode="json")}


@router.get("/{finding_id}/evidence", response_model=dict)
async def get_evidence(
	finding_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	finding = await FindingRepository(session).get_for_user(finding_id, user.id)
	if finding is None:
		raise HTTPException(status_code=404, detail="finding not found")
	return {"success": True, "data": [item.model_dump(mode="json") for item in finding.evidence]}
