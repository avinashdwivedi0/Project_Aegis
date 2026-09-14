import { NavLink, Outlet } from "react-router-dom";
import { Activity, FileText, FolderKanban, ShieldCheck } from "lucide-react";
import { TopNav } from "./TopNav";

const navigation = [
	{ label: "Projects", to: "/", icon: FolderKanban },
	{ label: "Quality signal", to: "/projects/demo", icon: Activity },
	{ label: "Reports", to: "/reports/demo", icon: FileText },
];

export function AppShell() {
	return (
		<div className="shell">
			<aside className="sidebar">
				<div className="brand"><span className="brand-mark"><ShieldCheck size={18} /></span><span>Aegis</span></div>
				<nav className="nav-list" aria-label="Primary navigation">
					{navigation.map(({ label, to, icon: Icon }) => (
						<NavLink key={label} to={to} className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
							<Icon size={17} />{label}
						</NavLink>
					))}
				</nav>
				<div className="sidebar-foot"><span className="status-dot" />System ready</div>
			</aside>
			<div className="main-column"><TopNav /><main className="page-content"><Outlet /></main></div>
		</div>
	);
}
