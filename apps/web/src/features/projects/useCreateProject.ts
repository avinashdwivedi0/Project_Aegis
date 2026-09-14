import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../lib/api-client";

export function useCreateProject() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: ({ name, gitUrl }: { name: string; gitUrl: string }) => api("/projects", { method: "POST", body: JSON.stringify({ name, git_url: gitUrl }) }),
		onSuccess: () => queryClient.invalidateQueries({ queryKey: ["projects"] }),
	});
}

export function useUploadProject() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: ({ name, file }: { name: string; file: File }) => {
			const form = new FormData();
			form.append("name", name);
			form.append("upload", file);
			return api("/projects", { method: "POST", body: form });
		},
		onSuccess: () => queryClient.invalidateQueries({ queryKey: ["projects"] }),
	});
}
