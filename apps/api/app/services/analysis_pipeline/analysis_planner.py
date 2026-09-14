from app.infrastructure.agents import AGENT_REGISTRY


def applicable_agents(context: dict) -> list[str]:
	return [
		agent_id
		for agent_id, agent_class in AGENT_REGISTRY.items()
		if agent_class(None).is_applicable(context)
	]
