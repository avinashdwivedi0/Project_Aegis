import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infrastructure.ai.ollama_provider import OllamaProvider


async def main() -> None:
    print(await OllamaProvider().complete("Reply with OK only.", "Reply with OK only."))


if __name__ == "__main__":
    asyncio.run(main())
