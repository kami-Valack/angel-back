# Utility functions for API responses

def success_response(message: str, data: dict = None, status_code: int = 200):
    return {
        "success": True,
        "message": message,
        "data": data or {}
    }

def error_response(code: str, message: str, status_code: int = 400, details: list = None):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            **({"details": details} if details else {})
        }
    }
