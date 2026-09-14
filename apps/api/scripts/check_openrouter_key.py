import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infrastructure.ai.openrouter_provider import OpenRouterProvider


async def main() -> None:
	result = await OpenRouterProvider().complete(
		"You are a connectivity check.",
		"Reply with the single word OK.",
	)
	print(result)


if __name__ == "__main__":
	asyncio.run(main())
