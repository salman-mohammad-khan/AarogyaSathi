"""The admin dashboard data and the surveillance write routes need ADMIN_TOKEN; the public chat API stays open."""
import pytest
from fastapi import HTTPException

from app import config
from app.admin_auth import require_admin
from app.main import app

PROTECTED = [
    ("/api/stats", "GET"),
    ("/api/surveillance/alerts", "GET"),
    ("/api/surveillance/run", "POST"),
    ("/api/surveillance/seed", "POST"),
    ("/api/surveillance/clear", "POST"),
]
PUBLIC = [("/api/chat", "POST"), ("/api/health", "GET"), ("/", "GET"), ("/admin", "GET")]


def _route(path, method):
    for route in app.routes:
        if getattr(route, "path", None) == path and method in getattr(route, "methods", set()):
            return route
    raise AssertionError(f"route {method} {path} not found")


def _guards(route):
    return [dep.call for dep in route.dependant.dependencies]


@pytest.mark.parametrize("path,method", PROTECTED)
def test_surveillance_and_stats_routes_require_the_admin_check(path, method):
    assert require_admin in _guards(_route(path, method))


@pytest.mark.parametrize("path,method", PUBLIC)
def test_public_routes_have_no_admin_check(path, method):
    assert require_admin not in _guards(_route(path, method))


def test_disabled_when_no_token_is_configured(monkeypatch):
    monkeypatch.setattr(config, "ADMIN_TOKEN", "")
    with pytest.raises(HTTPException) as err:
        require_admin(authorization="Bearer anything", x_admin_token=None)
    assert err.value.status_code == 503


def test_missing_token_is_rejected(monkeypatch):
    monkeypatch.setattr(config, "ADMIN_TOKEN", "s3cret-value")
    with pytest.raises(HTTPException) as err:
        require_admin(authorization=None, x_admin_token=None)
    assert err.value.status_code == 401


@pytest.mark.parametrize("authorization,x_token", [
    ("Bearer wrong", None),
    ("Basic s3cret-value", None),
    ("bearer ", None),
    (None, "wrong"),
    ("Bearer s3cret-valu", None),
    ("Bearer s3cret-value-and-more", None),
])
def test_wrong_tokens_are_rejected(monkeypatch, authorization, x_token):
    monkeypatch.setattr(config, "ADMIN_TOKEN", "s3cret-value")
    with pytest.raises(HTTPException) as err:
        require_admin(authorization=authorization, x_admin_token=x_token)
    assert err.value.status_code == 401


@pytest.mark.parametrize("authorization,x_token", [
    ("Bearer s3cret-value", None),
    ("bearer s3cret-value", None),
    (None, "s3cret-value"),
])
def test_correct_token_is_accepted(monkeypatch, authorization, x_token):
    monkeypatch.setattr(config, "ADMIN_TOKEN", "s3cret-value")
    assert require_admin(authorization=authorization, x_admin_token=x_token) is None
