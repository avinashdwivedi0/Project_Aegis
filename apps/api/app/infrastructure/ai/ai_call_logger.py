import json
import logging

logger = logging.getLogger("aegis.ai")


def log_call(agent_id: str, latency_ms: float, tokens: int | None, success: bool) -> None:
	logger.info(json.dumps({"agent_id": agent_id, "latency_ms": round(latency_ms, 2), "tokens": tokens, "success": success}))
