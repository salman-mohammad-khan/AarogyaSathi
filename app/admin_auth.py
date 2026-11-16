"""Token protection for the admin and surveillance endpoints.

The public chat API stays open. The dashboard data and the routes that change surveillance data need the secret in
the ``ADMIN_TOKEN`` environment variable, sent as ``Authorization: Bearer <token>`` or ``X-Admin-Token: <token>``.
If ``ADMIN_TOKEN`` is not set, these endpoints are disabled (503) instead of being left open.
"""
import hmac

from fastapi import Header, HTTPException

from app import config


def _supplied_token(authorization, x_admin_token):
    if x_admin_token:
        return x_admin_token
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return ""


def require_admin(authorization: str | None = Header(default=None), x_admin_token: str | None = Header(default=None)):
    expected = config.ADMIN_TOKEN
    if not expected:
        raise HTTPException(status_code=503, detail="Admin access is disabled. Set ADMIN_TOKEN on the server.")
    supplied = _supplied_token(authorization, x_admin_token)
    if not hmac.compare_digest(supplied.encode("utf-8"), expected.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid or missing admin token.")
