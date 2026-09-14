import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api-client";
import type { AnalysisRun } from "./useStartAnalysis";

export function useAnalysisRun(runId: string | null) {
	return useQuery({ queryKey: ["analysis", runId], queryFn: () => api<AnalysisRun>(`/analysis/${runId}`), enabled: Boolean(runId), refetchInterval: (query) => ["COMPLETED", "PARTIAL_FAILURE", "FAILED"].includes(query.state.data?.status ?? "") ? false : 2500 });
}
