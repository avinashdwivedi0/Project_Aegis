import { ArrowUpRight } from "lucide-react";
import { SeverityBadge } from "../severity/SeverityBadge";
import type { Finding } from "../../features/findings/useFindings";

export function FindingCard({ finding, onSelect }: { finding: Finding; onSelect: () => void }) {
	return <button className="finding-card" onClick={onSelect}><div className="finding-card-top"><SeverityBadge severity={finding.severity} /><ArrowUpRight size={17} /></div><h3>{finding.title}</h3><p>{finding.description}</p><div className="finding-meta"><span>{finding.category.replace(/_/g, " ")}</span><span>{Math.round(finding.confidence * 100)}% confidence</span></div></button>;
}
