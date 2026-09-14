import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api-client";

export type Project = { id: string; name: string; detected_stack: { languages?: Record<string, number>; frameworks?: string[] } | null; created_at: string };

export function useProjects() {
	return useQuery({ queryKey: ["projects"], queryFn: () => api<Project[]>("/projects") });
}
