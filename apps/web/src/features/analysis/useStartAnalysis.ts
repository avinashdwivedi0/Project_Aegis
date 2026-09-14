import { useMutation } from "@tanstack/react-query";
import { api } from "../../lib/api-client";

export type AnalysisRun = { id: string; status: string; overall_score: number | null; dimension_scores: Record<string, number> | null };

export function useStartAnalysis() {
	return useMutation({ mutationFn: (projectId: string) => api<AnalysisRun>(`/projects/${projectId}/analysis`, { method: "POST" }) });
}
