import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useRegister } from "../../features/auth/useLogin";

export function RegisterPage() {
	const [name, setName] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const navigate = useNavigate();
	const register = useRegister();

	if (localStorage.getItem("aegis_access_token")) {
		return <Navigate to="/" replace />;
	}

	return (
		<form
			className="dialog"
			onSubmit={(event) => {
				event.preventDefault();
				register.mutate(
					{ name, email, password },
					{ onSuccess: () => navigate("/", { replace: true }) },
				);
			}}
		>
			<p className="eyebrow">Project Aegis</p>
			<h2>Create your workspace</h2>
			<label>
				Name
				<input type="text" value={name} onChange={(event) => setName(event.target.value)} required />
			</label>
			<label>
				Email
				<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
			</label>
			<label>
				Password
				<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
			</label>
			{register.isError && <p className="error-text">{register.error.message}</p>}
			<button className="primary-button" type="submit" disabled={register.isPending}>
				{register.isPending ? "Creating account..." : "Create account"}
			</button>
			<p className="muted">
				Already have an account? <Link to="/login">Sign in</Link>
			</p>
		</form>
	);
}

