import { Bell, LogOut, Search, User, X } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

const quickSearchItems = [
	{ label: "Projects overview", path: "/" },
	{ label: "Quality signal", path: "/projects/demo" },
	{ label: "Reports", path: "/reports/demo" },
];

const notificationItems = [
	{ title: "Analysis completed", detail: "Project quality review finished successfully." },
	{ title: "New recommendation", detail: "Two high-priority findings need review." },
	{ title: "Sync reminder", detail: "Your team digest is ready for export." },
];

export function TopNav() {
	const navigate = useNavigate();
	const [searchOpen, setSearchOpen] = useState(false);
	const [notificationsOpen, setNotificationsOpen] = useState(false);
	const [profileOpen, setProfileOpen] = useState(false);
	const [query, setQuery] = useState("");

	const email = localStorage.getItem("aegis_user_email") ?? "team@aegis.local";
	const initials = useMemo(() => email.split("@")[0].slice(0, 2).toUpperCase() || "AE", [email]);

	const searchResults = useMemo(() => {
		const normalized = query.trim().toLowerCase();
		if (!normalized) return quickSearchItems;
		return quickSearchItems.filter((item) => item.label.toLowerCase().includes(normalized));
	}, [query]);

	const handleSearch = (value: string) => {
		const normalized = value.trim();
		if (!normalized) return;
		setSearchOpen(false);
		setQuery("");
		if (normalized.toLowerCase().includes("report")) navigate("/reports/demo");
		else navigate("/");
	};

	const handleLogout = () => {
		localStorage.removeItem("aegis_access_token");
		localStorage.removeItem("aegis_refresh_token");
		localStorage.removeItem("aegis_user_email");
		setProfileOpen(false);
		navigate("/login", { replace: true });
	};

	return (
		<header className="top-nav">
			<div className="breadcrumb"><span>Workspace</span><strong>/</strong><span className="muted">Quality command center</span></div>
			<div className="top-actions">
				<button className="icon-button" aria-label="Search" onClick={() => setSearchOpen((current) => !current)}>
					<Search size={18} />
				</button>
				<button className="icon-button" aria-label="Notifications" onClick={() => setNotificationsOpen((current) => !current)}>
					<Bell size={18} />
				</button>
				<div className="profile-wrap">
					<button className="avatar-button" aria-label="Profile" onClick={() => setProfileOpen((current) => !current)}>
						<div className="avatar">{initials}</div>
					</button>
					{profileOpen && (
						<div className="floating-menu profile-menu">
							<div className="menu-header">
								<strong>{email}</strong>
								<span>Workspace admin</span>
							</div>
							<button type="button" className="menu-row" onClick={() => navigate("/")}>
								<User size={16} />
								<span>Profile</span>
							</button>
							<button type="button" className="menu-row danger" onClick={handleLogout}>
								<LogOut size={16} />
								<span>Sign out</span>
							</button>
						</div>
					)}
				</div>
			</div>
			{searchOpen && (
				<div className="floating-panel search-panel">
					<div className="panel-header">
						<strong>Quick search</strong>
						<button type="button" className="panel-close" aria-label="Close search" onClick={() => setSearchOpen(false)}>
							<X size={16} />
						</button>
					</div>
					<input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search projects or reports" onKeyDown={(event) => { if (event.key === "Enter") handleSearch(query); }} />
					<div className="panel-list">
						{searchResults.map((item) => (
							<button key={item.label} type="button" className="panel-item" onClick={() => handleSearch(item.label)}>
								<span>{item.label}</span>
							</button>
						))}
					</div>
				</div>
			)}
			{notificationsOpen && (
				<div className="floating-panel notification-panel">
					<div className="panel-header">
						<strong>Notifications</strong>
						<button type="button" className="panel-close" aria-label="Close notifications" onClick={() => setNotificationsOpen(false)}>
							<X size={16} />
						</button>
					</div>
					<div className="panel-list">
						{notificationItems.map((item) => (
							<div key={item.title} className="notification-item">
								<strong>{item.title}</strong>
								<span>{item.detail}</span>
							</div>
						))}
					</div>
				</div>
			)}
		</header>
	);
}
