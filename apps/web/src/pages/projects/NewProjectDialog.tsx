import { useState } from "react";
import { X } from "lucide-react";
import { useCreateProject, useUploadProject } from "../../features/projects/useCreateProject";

export function NewProjectDialog({ onClose }: { onClose: () => void }) {
	const [name, setName] = useState("");
	const [gitUrl, setGitUrl] = useState("");
	const [file, setFile] = useState<File | null>(null);
	const git = useCreateProject();
	const upload = useUploadProject();
	const submit = (event: React.FormEvent) => {
		event.preventDefault();
		if (file) upload.mutate({ name, file }, { onSuccess: onClose });
		else git.mutate({ name, gitUrl }, { onSuccess: onClose });
	};
	return <div className="dialog-backdrop"><form className="dialog" onSubmit={submit}><button className="dialog-close" type="button" aria-label="Close" onClick={onClose}><X size={18} /></button><p className="eyebrow">Ingest codebase</p><h2>New project</h2><label>Project name<input required value={name} onChange={(event) => setName(event.target.value)} /></label><label>Git URL<input value={gitUrl} onChange={(event) => setGitUrl(event.target.value)} placeholder="https://github.com/org/repo" disabled={Boolean(file)} /></label><label>Or upload ZIP<input type="file" accept=".zip" onChange={(event) => setFile(event.target.files?.[0] ?? null)} /></label><button className="primary-button" type="submit" disabled={git.isPending || upload.isPending}>{git.isPending || upload.isPending ? "Creating..." : "Create project"}</button></form></div>;
}
