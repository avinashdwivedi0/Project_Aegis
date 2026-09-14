type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";

export function SeverityBadge({ severity }: { severity: Severity }) {
	return <span className={`severity severity-${severity.toLowerCase()}`}>{severity}</span>;
}
