import httpx
from pydantic import BaseModel

from app.core.config import settings


class OllamaProvider:
	async def complete(self, system: str, prompt: str, response_model: type[BaseModel] | None = None, temperature: float = 0.2) -> str:
		if response_model:
			system += f"\nReturn only JSON matching this schema: {response_model.model_json_schema()}"
		async with httpx.AsyncClient(timeout=300.0) as client:
			response = await client.post(f"{settings.ollama_base_url}/api/chat", json={"model": settings.ollama_model, "stream": False, "options": {"temperature": temperature}, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]})
			response.raise_for_status()
			content = response.json()["message"]["content"]
			if response_model:
				response_model.model_validate_json(content)
			return content