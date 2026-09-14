from app.infrastructure.agents.architecture_agent import ArchitectureAgent
from app.infrastructure.agents.code_quality_agent import CodeQualityAgent
from app.infrastructure.agents.dependency_agent import DependencyAgent
from app.infrastructure.agents.documentation_agent import DocumentationAgent
from app.infrastructure.agents.security_agent import SecurityAgent
from app.infrastructure.agents.testing_agent import TestingAgent

AGENT_REGISTRY = {
	"security-agent": SecurityAgent,
	"code-quality-agent": CodeQualityAgent,
	"testing-agent": TestingAgent,
	"architecture-agent": ArchitectureAgent,
	"dependency-agent": DependencyAgent,
	"documentation-agent": DocumentationAgent,
}

__all__ = ["AGENT_REGISTRY", "ArchitectureAgent", "CodeQualityAgent", "DependencyAgent", "DocumentationAgent", "SecurityAgent", "TestingAgent"]
