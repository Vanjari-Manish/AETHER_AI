import uuid
from typing import Any, Optional, Dict
from fastapi import Request
from fastapi.responses import JSONResponse

def generate_request_id() -> str:
    return str(uuid.uuid4())

def send_success(data: Any, meta: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None) -> Dict[str, Any]:
    """Wraps positive response data into the standard GPO JSON envelope."""
    return {
        "requestId": request_id or generate_request_id(),
        "success": True,
        "data": data,
        "meta": meta
    }

def send_error(code: str, message: str, details: Optional[Any] = None, request_id: Optional[str] = None) -> Dict[str, Any]:
    """Wraps error conditions into the standard GPO JSON error envelope."""
    return {
        "requestId": request_id or generate_request_id(),
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details
        }
    }

class GPOJSONResponse(JSONResponse):
    """Custom JSONResponse that automatically ensures the output matches GPO envelopes."""
    def render(self, content: Any) -> bytes:
        if isinstance(content, dict) and ("success" in content) and ("requestId" in content):
            # Already formatted
            return super().render(content)
        # Wrap raw data
        formatted = send_success(content)
        return super().render(formatted)
