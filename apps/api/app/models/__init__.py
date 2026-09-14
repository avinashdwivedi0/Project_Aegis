from enum import Enum


class Severity(str, Enum):
	CRITICAL = "CRITICAL"
	HIGH = "HIGH"
	MEDIUM = "MEDIUM"
	LOW = "LOW"
	INFO = "INFO"


class AgentCategory(str, Enum):
	SECURITY = "SECURITY"
	CODE_QUALITY = "CODE_QUALITY"
	TESTING = "TESTING"
	ARCHITECTURE = "ARCHITECTURE"
	DEPENDENCY = "DEPENDENCY"
	DOCUMENTATION = "DOCUMENTATION"


class AnalysisStatus(str, Enum):
	PENDING = "PENDING"
	RUNNING = "RUNNING"
	PARTIAL_FAILURE = "PARTIAL_FAILURE"
	COMPLETED = "COMPLETED"
	FAILED = "FAILED"


class AgentRunStatus(str, Enum):
	PENDING = "PENDING"
	RUNNING = "RUNNING"
	SUCCEEDED = "SUCCEEDED"
	FAILED = "FAILED"
	SKIPPED = "SKIPPED"


from .agent_run import AgentRun
from .analysis_run import AnalysisRun
from .evidence import Evidence
from .finding import Finding
from .project import Project
from .recommendation import Recommendation
from .report import Report
from .user import User

__all__ = [
	"AgentCategory", "AgentRun", "AgentRunStatus", "AnalysisRun", "AnalysisStatus",
	"Evidence", "Finding", "Project", "Recommendation", "Report", "Severity", "User",
]
