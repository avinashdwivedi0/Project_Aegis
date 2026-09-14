import httpx
from pydantic import BaseModel

from app.core.config import settings


class GeminiProvider:
	async def complete(self, system: str, prompt: str, response_model: type[BaseModel] | None = None, temperature: float = 0.2) -> str:
		if response_model:
			system += f"\nReturn only JSON matching this schema: {response_model.model_json_schema()}"
		async with httpx.AsyncClient() as client:
			response = await client.post(f"{settings.gemini_base_url}/models/{settings.gemini_model}:generateContent", params={"key": settings.gemini_api_key}, json={"systemInstruction": {"parts": [{"text": system}]}, "contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": {"temperature": temperature}})
			response.raise_for_status()
			content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
			if response_model:
				response_model.model_validate_json(content)
			return content