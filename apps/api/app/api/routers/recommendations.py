from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.recommendation_schemas import RecommendationRead

router = APIRouter(prefix="/projects", tags=["recommendations"])


@router.get("/{project_id}/recommendations", response_model=dict)
async def list_recommendations(
	project_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	recommendations = await RecommendationRepository(session).list_for_project(project_id, user.id)
	data = [RecommendationRead.model_validate(item, from_attributes=True).model_dump(mode="json") for item in recommendations]
	return {"success": True, "data": data}
