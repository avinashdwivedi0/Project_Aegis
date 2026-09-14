import { Play } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { api } from "../../lib/api-client";
import { useQuery } from "@tanstack/react-query";
import { useStartAnalysis } from "../../features/analysis/useStartAnalysis";
import { useAnalysisRun } from "../../features/analysis/useAnalysisRun";

type Dashboard = { project: { name: string }; analysis: { id: string; status: string; overall_score: number | null; dimension_scores: Record<string, number> | null } | null; severity_counts: Record<string, number> };

export function ProjectDashboardPage() {
	const { projectId = "" } = useParams();
	const dashboard = useQuery({ queryKey: ["dashboard", projectId], queryFn: () => api<Dashboard>(`/projects/${projectId}/dashboard`) });
	const start = useStartAnalysis();
	const run = useAnalysisRun(start.data?.id ?? null);
	const analysis = run.data ?? dashboard.data?.analysis;
	return <section className="page-section"><div className="section-heading"><div><p className="eyebrow">Project dashboard</p><h1>{dashboard.data?.project.name ?? "Quality signal"}</h1><p className="lede">Evidence-backed quality metrics for this codebase.</p></div><button className="primary-button" onClick={() => start.mutate(projectId)} disabled={start.isPending}><Play size={16} />{start.isPending ? "Starting..." : "Run analysis"}</button></div>{dashboard.isLoading && <p className="muted">Loading dashboard...</p>}{analysis && <><div className="dashboard-actions"><Link to={`/projects/${projectId}/findings?run=${analysis.id}`}>Explore findings</Link><Link to={`/projects/${projectId}/reports/${analysis.id}`}>Generate report</Link></div><div className="dashboard-summary"><div className="score-panel"><span>Overall quality</span><strong>{analysis.overall_score ?? "--"}</strong><small>{analysis.status}</small></div><div className="dimension-list">{Object.entries(analysis.dimension_scores ?? {}).map(([name, score]) => <div className="dimension-row" key={name}><span>{name.replace(/_/g, " ")}</span><div className="bar"><i style={{ width: `${score}%` }} /></div><strong>{score}</strong></div>)}</div></div></>}</section>;
}
