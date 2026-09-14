import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api-client";

export type Finding = { id: string; title: string; description: string; severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO"; category: string; confidence: number; component: string | null; evidence: { file: string; line_start: number | null; line_end: number | null; tool: string | null; rule: string | null; snippet: string | null }[]; recommendation?: { reasoning: string; impact: string; action: string } | null };

export function useFindings(runId: string | undefined, filters: { severity?: string; category?: string; component?: string }) {
	const params = new URLSearchParams(Object.entries(filters).filter(([, value]) => Boolean(value)) as string[][]);
	return useQuery({ queryKey: ["findings", runId, filters], queryFn: () => api<Finding[]>(`/analysis/${runId}/findings?${params}`), enabled: Boolean(runId) });
}
