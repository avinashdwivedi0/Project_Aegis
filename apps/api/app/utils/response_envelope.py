def success(data: object) -> dict[str, object]:
	return {"success": True, "data": data}


def error(message: str) -> dict[str, object]:
	return {"success": False, "error": {"message": message}}
