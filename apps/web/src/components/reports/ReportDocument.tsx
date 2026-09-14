import type { Report } from "../../features/reports/useGenerateReport";

export function ReportDocument({ report }: { report: Report }) {
	return <article className="report-document"><p className="eyebrow">Assessment report</p><h2>Project quality review</h2><div className="report-summary"><strong>{report.content.executive_summary.finding_count}</strong><span>findings identified</span><strong>{report.content.executive_summary.critical_count}</strong><span>critical findings</span></div><h3>Prioritized findings</h3>{report.content.findings.map((finding, index) => <section className="report-finding" key={`${finding.title}-${index}`}><div><strong>{finding.title}</strong><span>{finding.category} · {finding.severity}</span></div><p>{finding.description}</p>{finding.recommendation && <blockquote>{finding.recommendation}</blockquote>}</section>)}</article>;
}
