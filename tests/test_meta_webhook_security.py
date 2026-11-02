"""Synthetic channel checks: no model calls, patient data or live sends."""
import hashlib
import hmac
import json
import asyncio
from unittest.mock import Mock

import pytest
from fastapi import BackgroundTasks, HTTPException

from app import config
from app.channels import whatsapp as channel


def client_and_payload(monkeypatch):
    monkeypatch.setattr(config, "WHATSAPP_APP_SECRET", "synthetic-test-secret")
    raw = json.dumps({"object": "whatsapp_business_account", "entry": []}).encode()
    signature = "sha256=" + hmac.new(b"synthetic-test-secret", raw, hashlib.sha256).hexdigest()
    return raw, signature


def invoke(raw, signature=""):
    class Request:
        headers = {"x-hub-signature-256": signature}

        async def body(self):
            return raw
    tasks = BackgroundTasks()
    result = asyncio.run(channel.meta_webhook_message(Request(), tasks))
    asyncio.run(tasks())
    return result


def test_valid_signature_dispatches_exact_payload(monkeypatch):
    raw, signature = client_and_payload(monkeypatch)
    worker = Mock()
    monkeypatch.setattr(channel, "_handle_meta_inbound_payload", worker)
    assert invoke(raw, signature) == {"status": "ok"}
    worker.assert_called_once_with(json.loads(raw))


def test_tampered_or_unsigned_payload_never_dispatches(monkeypatch):
    raw, signature = client_and_payload(monkeypatch)
    worker = Mock()
    monkeypatch.setattr(channel, "_handle_meta_inbound_payload", worker)
    for body, supplied in [(raw, ""), (raw + b" ", signature)]:
        with pytest.raises(HTTPException) as error:
            invoke(body, supplied)
        assert error.value.status_code == 403
    worker.assert_not_called()


def test_missing_app_secret_fails_closed(monkeypatch):
    raw, signature = client_and_payload(monkeypatch)
    monkeypatch.setattr(config, "WHATSAPP_APP_SECRET", "")
    with pytest.raises(HTTPException) as error:
        invoke(raw, signature)
    assert error.value.status_code == 503


def test_duplicate_message_is_only_answered_once(monkeypatch):
    monkeypatch.setattr(config, "WHATSAPP_PHONE_ID", "test-phone-id")
    process = Mock(return_value={"text": "Synthetic reply"})
    send = Mock(return_value={"status": "sent"})
    monkeypatch.setattr(channel.router, "process_message", process)
    monkeypatch.setattr(channel, "send_whatsapp_message", send)
    channel._completed_meta_messages.clear()
    body = {"entry": [{"changes": [{"value": {
        "metadata": {"phone_number_id": "test-phone-id"},
        "messages": [{"id": "synthetic-message-id", "from": "synthetic-recipient",
                      "type": "text", "text": {"body": "hello"}}]
    }}]}]}
    channel._handle_meta_inbound_payload(body)
    channel._handle_meta_inbound_payload(body)
    process.assert_called_once()
    send.assert_called_once_with("synthetic-recipient", "Synthetic reply")
    channel._completed_meta_messages.clear()


def test_wrong_receiver_and_status_updates_do_not_answer(monkeypatch):
    monkeypatch.setattr(config, "WHATSAPP_PHONE_ID", "correct-phone-id")
    process = Mock()
    monkeypatch.setattr(channel.router, "process_message", process)
    channel._handle_meta_inbound_payload({"entry": [{"changes": [{"value": {
        "metadata": {"phone_number_id": "different-phone-id"},
        "messages": [{"id": "m", "from": "synthetic", "type": "text", "text": {"body": "hi"}}]
    }}, {"value": {"statuses": [{"status": "delivered"}]}}]}]})
    process.assert_not_called()
