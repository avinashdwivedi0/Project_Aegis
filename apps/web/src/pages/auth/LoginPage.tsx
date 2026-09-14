import { useState } from "react";
import { Navigate, Link, useNavigate } from "react-router-dom";
import { useLogin } from "../../features/auth/useLogin";

export function LoginPage() {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const navigate = useNavigate();
	const login = useLogin();

	if (localStorage.getItem("aegis_access_token")) {
		return <Navigate to="/" replace />;
	}

	return (
		<form
			className="dialog"
			onSubmit={(event) => {
				event.preventDefault();
				login.mutate(
					{ email, password },
					{ onSuccess: () => navigate("/", { replace: true }) },
				);
			}}
		>
			<p className="eyebrow">Project Aegis</p>
			<h2>Sign in</h2>
			<label>
				Email
				<input type="email" required value={email} onChange={(event) => setEmail(event.target.value)} />
			</label>
			<label>
				Password
				<input type="password" required value={password} onChange={(event) => setPassword(event.target.value)} />
			</label>
			{login.isError && <p className="error-text">{login.error.message}</p>}
			<button className="primary-button" type="submit" disabled={login.isPending}>
				{login.isPending ? "Signing in..." : "Sign in"}
			</button>
			<p className="muted">
				Need an account? <Link to="/register">Create one</Link>
			</p>
		</form>
	);
}
