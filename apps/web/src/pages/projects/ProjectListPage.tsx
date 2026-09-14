import { ArrowUpRight, Plus } from "lucide-react";
import { Link, Navigate } from "react-router-dom";
import { useProjects } from "../../features/projects/useProjects";
import { NewProjectDialog } from "./NewProjectDialog";
import { useState } from "react";

export function ProjectListPage() {
	const { data: projects, isLoading, error } = useProjects();
	const [dialogOpen, setDialogOpen] = useState(false);

	if (!localStorage.getItem("aegis_access_token")) {
		return <Navigate to="/login" replace />;
	}

	return <section className="page-section"><div className="section-heading"><div><p className="eyebrow">Overview</p><h1>Projects</h1><p className="lede">A clear view of software quality across your codebases.</p></div><button className="primary-button" onClick={() => setDialogOpen(true)}><Plus size={17} />New project</button></div>{isLoading && <p className="muted">Loading projects...</p>}{error && <p className="error-text">{error.message}</p>}<div className="project-grid">{projects?.map((project) => <Link className="project-card project-link" to={`/projects/${project.id}`} key={project.id}><div className="card-top"><span className="project-icon">{project.name[0]}</span><ArrowUpRight size={18} className="muted" /></div><h2>{project.name}</h2><p className="muted">{Object.keys(project.detected_stack?.languages ?? {}).join(" · ") || "Stack pending"}</p><div className="card-foot"><span>Created {new Date(project.created_at).toLocaleDateString()}</span><span className="score-pill">Open dashboard</span></div></Link>)}</div>{dialogOpen && <NewProjectDialog onClose={() => setDialogOpen(false)} />}</section>;
}
