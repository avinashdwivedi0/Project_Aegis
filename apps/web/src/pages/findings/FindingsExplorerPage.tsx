import { useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { useFindings } from "../../features/findings/useFindings";
import { FindingCard } from "../../components/findings/FindingCard";
import { FindingDetailSheet } from "../../components/findings/FindingDetailSheet";
import type { Finding } from "../../features/findings/useFindings";

export function FindingsExplorerPage() {
	const { projectId } = useParams();
	const [searchParams] = useSearchParams();
	const [selected, setSelected] = useState<Finding | null>(null);
	const [severity, setSeverity] = useState("");
	const { data, isLoading, error } = useFindings(searchParams.get("run") ?? projectId, { severity });
	return <section className="page-section"><p className="eyebrow">Investigation</p><h1>Findings explorer</h1><p className="lede">Trace each issue from deterministic evidence to recommended action.</p><div className="finding-toolbar"><select value={severity} onChange={(event) => setSeverity(event.target.value)}><option value="">All severities</option><option>CRITICAL</option><option>HIGH</option><option>MEDIUM</option><option>LOW</option><option>INFO</option></select></div>{isLoading && <p className="muted">Loading findings...</p>}{error && <p className="error-text">{error.message}</p>}<div className="finding-list">{data?.map((finding) => <FindingCard key={finding.id} finding={finding} onSelect={() => setSelected(finding)} />)}</div><FindingDetailSheet finding={selected} onClose={() => setSelected(null)} /></section>;
}
