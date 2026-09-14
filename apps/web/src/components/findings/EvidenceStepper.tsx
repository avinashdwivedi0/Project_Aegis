import type { Finding } from "../../features/findings/useFindings";

export function EvidenceStepper({ finding }: { finding: Finding }) {
	return <div className="evidence-chain"><div><span className="step-number">1</span><div><strong>Finding</strong><p>{finding.description}</p></div></div>{finding.evidence.map((evidence, index) => <div key={`${evidence.file}-${index}`}><span className="step-number">{index + 2}</span><div><strong>Evidence · {evidence.file}:{evidence.line_start ?? "?"}</strong><p>{evidence.tool ?? "Deterministic scanner"} {evidence.rule ? `· ${evidence.rule}` : ""}</p>{evidence.snippet && <code>{evidence.snippet}</code>}</div></div>)}{finding.recommendation && <div><span className="step-number">{finding.evidence.length + 2}</span><div><strong>Recommendation</strong><p>{finding.recommendation.action}</p></div></div>}</div>;
}
