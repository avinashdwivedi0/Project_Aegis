from app.core.config import settings
from app.infrastructure.ai.ai_provider import AIProvider
from app.infrastructure.ai.gemini_provider import GeminiProvider
from app.infrastructure.ai.ollama_provider import OllamaProvider
from app.infrastructure.ai.openrouter_provider import OpenRouterProvider


class FallbackProvider:
	def __init__(self, providers: list[AIProvider]) -> None:
		self.providers = providers

	async def complete(self, system, prompt, response_model=None, temperature=0.2) -> str:
		last_error = None
		for provider in self.providers:
			try:
				return await provider.complete(system, prompt, response_model, temperature)
			except Exception as error:  # noqa: BLE001
				last_error = error
		raise RuntimeError("all configured AI providers failed") from last_error


def get_ai_provider() -> AIProvider:
	providers: list[AIProvider] = []
	if settings.ai_provider == "ollama":
		providers.append(OllamaProvider())
	if settings.gemini_api_key:
		providers.append(GeminiProvider())
	if settings.openrouter_api_key:
		providers.append(OpenRouterProvider())
	if not providers:
		raise RuntimeError("configure Ollama, Gemini, or OpenRouter")
	return FallbackProvider(providers)