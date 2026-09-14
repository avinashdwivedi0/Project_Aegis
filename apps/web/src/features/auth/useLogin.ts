import { useMutation } from "@tanstack/react-query";
import { api, setAccessToken } from "../../lib/api-client";

export function useLogin() {
	return useMutation({
		mutationFn: (input: { email: string; password: string }) =>
			api<{ access_token: string; refresh_token: string }>("/auth/login", {
				method: "POST",
				body: JSON.stringify(input),
			}),
		onSuccess: (data, variables) => {
			setAccessToken(data.access_token);
			localStorage.setItem("aegis_user_email", variables.email);
		},
	});
}

export function useRegister() {
	return useMutation({
		mutationFn: (input: { email: string; password: string; name?: string }) =>
			api<{ access_token: string; refresh_token: string }>("/auth/register", {
				method: "POST",
				body: JSON.stringify(input),
			}),
		onSuccess: (data, variables) => {
			setAccessToken(data.access_token);
			localStorage.setItem("aegis_user_email", variables.email);
		},
	});
}
