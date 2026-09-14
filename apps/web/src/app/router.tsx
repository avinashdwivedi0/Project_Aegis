import { createBrowserRouter } from "react-router-dom";
import { AppShell } from "../components/layout/AppShell";
import { LoginPage } from "../pages/auth/LoginPage";
import { RegisterPage } from "../pages/auth/RegisterPage";
import { FindingsExplorerPage } from "../pages/findings/FindingsExplorerPage";
import { ProjectDashboardPage } from "../pages/dashboard/ProjectDashboardPage";
import { ProjectListPage } from "../pages/projects/ProjectListPage";
import { ReportPage } from "../pages/reports/ReportPage";

export const router = createBrowserRouter([
	{
		path: "/login",
		element: <LoginPage />,
	},
	{
		path: "/register",
		element: <RegisterPage />,
	},
	{
		path: "/",
		element: <AppShell />,
		children: [
			{ index: true, element: <ProjectListPage /> },
			{ path: "projects/:projectId", element: <ProjectDashboardPage /> },
			{ path: "projects/:projectId/findings", element: <FindingsExplorerPage /> },
			{ path: "reports/:reportId", element: <ReportPage /> },
			{ path: "projects/:projectId/reports/:runId", element: <ReportPage /> },
		],
	},
]);
