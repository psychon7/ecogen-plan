"""Audit logging middleware — append-only logging of every significant action."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("audit")


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Logs every mutating request to the audit logger.

    In production, this writes to the append-only `audit_log` table.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.monotonic()
        response = await call_next(request)
        elapsed_ms = int((time.monotonic() - start) * 1000)

        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            logger.info(
                "AUDIT method=%s path=%s status=%d elapsed_ms=%d user=%s",
                request.method,
                request.url.path,
                response.status_code,
                elapsed_ms,
                request.headers.get("x-user-id", "anonymous"),
            )

        return response
