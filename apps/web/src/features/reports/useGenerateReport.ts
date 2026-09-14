import { useMutation } from "@tanstack/react-query";
import { api } from "../../lib/api-client";

export type Report = { id: string; content: { executive_summary: { finding_count: number; critical_count: number }; findings: { title: string; severity: string; category: string; description: string; recommendation: string | null }[] } };

export function useGenerateReport(projectId: string, runId: string) {
	return useMutation({ mutationFn: () => api<Report>(`/reports/projects/${projectId}?run_id=${runId}`, { method: "POST" }) });
}
