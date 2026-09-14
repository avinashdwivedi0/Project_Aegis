from typing import Protocol

from pydantic import BaseModel


class AIProvider(Protocol):
	async def complete(
		self,
		system: str,
		prompt: str,
		response_model: type[BaseModel] | None = None,
		temperature: float = 0.2,
	) -> str: ...
