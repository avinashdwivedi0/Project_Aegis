const baseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export function setAccessToken(token: string | null) {
	if (token) localStorage.setItem("aegis_access_token", token);
	else localStorage.removeItem("aegis_access_token");
}

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
	const token = localStorage.getItem("aegis_access_token");
	const isForm = options.body instanceof FormData;
	const response = await fetch(`${baseUrl}${path}`, {
		...options,
		headers: {
			...(isForm ? {} : { "Content-Type": "application/json" }),
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...options.headers,
		},
	});

	if (response.status === 204 || response.headers.get("content-length") === "0") {
		return undefined as T;
	}

	const text = await response.text();
	const body = text ? JSON.parse(text) : null;
	if (!response.ok) {
		throw new Error(body?.error?.message ?? body?.detail ?? "Request failed");
	}
	return (body?.data ?? body) as T;
}
