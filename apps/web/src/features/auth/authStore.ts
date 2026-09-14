import { setAccessToken } from "../../lib/api-client";

export function saveSession(accessToken: string, refreshToken: string) {
	setAccessToken(accessToken);
	localStorage.setItem("aegis_refresh_token", refreshToken);
}

export function clearSession() {
	setAccessToken(null);
	localStorage.removeItem("aegis_refresh_token");
}
