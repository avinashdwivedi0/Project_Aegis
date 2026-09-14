import { useParams } from "react-router-dom";
import { useGenerateReport } from "../../features/reports/useGenerateReport";
import { ReportDocument } from "../../components/reports/ReportDocument";

export function ReportPage() {
	const { projectId = "", runId = "" } = useParams();
	const report = useGenerateReport(projectId, runId);
	return <section className="page-section"><p className="eyebrow">Deliverable</p><h1>Reports</h1><p className="lede">Generate an exportable assessment from the latest analysis.</p><button className="primary-button" onClick={() => report.mutate()} disabled={report.isPending}>{report.isPending ? "Generating..." : "Generate report"}</button>{report.data && <ReportDocument report={report.data} />}</section>;
}
