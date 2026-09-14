from time import perf_counter

import httpx
from pydantic import BaseModel

from app.core.config import settings
from app.infrastructure.ai.ai_call_logger import log_call


class OpenRouterProvider:
	async def complete(
		self,
		system: str,
		prompt: str,
		response_model: type[BaseModel] | None = None,
		temperature: float = 0.2,
	) -> str:
		instruction = system
		if response_model is not None:
			instruction += f"\nReturn only valid JSON matching this schema:\n{response_model.model_json_schema()}"

		for attempt in range(2):
			started = perf_counter()
			try:
				content, tokens = await self._request(instruction, prompt, temperature)
				log_call("unknown", (perf_counter() - started) * 1000, tokens, True)
			except Exception:
				log_call("unknown", (perf_counter() - started) * 1000, None, False)
				raise
			if response_model is None:
				return content
			try:
				response_model.model_validate_json(content)
				return content
			except ValueError as error:
				if attempt == 1:
					raise ValueError("OpenRouter returned invalid structured output") from error
				prompt = f"{prompt}\nReturn valid JSON only. Previous validation error: {error}"
		raise RuntimeError("unreachable")

	async def _request(self, system: str, prompt: str, temperature: float) -> tuple[str, int | None]:
		async with httpx.AsyncClient(
			headers={
				"Authorization": f"Bearer {settings.openrouter_api_key}",
				"HTTP-Referer": settings.openrouter_http_referer,
				"X-Title": settings.openrouter_app_title,
			}
		) as client:
			response = await client.post(
				f"{settings.openrouter_base_url}/chat/completions",
				json={
					"model": settings.openrouter_model,
					"temperature": temperature,
					"messages": [
						{"role": "system", "content": system},
						{"role": "user", "content": prompt},
					],
				},
			)
			response.raise_for_status()
			data = response.json()
			return data["choices"][0]["message"]["content"], data.get("usage", {}).get("total_tokens")
