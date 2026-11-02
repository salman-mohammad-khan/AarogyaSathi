import logging
import hashlib
import hmac
import json
import threading
from collections import OrderedDict
from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import httpx

from app import config
from app.core import router
from app.core import session as session_store

logger = logging.getLogger("uvicorn.error.aarogyasathi.whatsapp")

whatsapp_router = APIRouter()
_meta_message_lock = threading.Lock()
_completed_meta_messages = OrderedDict()


def send_whatsapp_message(to_number: str, message_text: str) -> dict:
    """
    Sends a text message back to the user via Meta's WhatsApp Cloud API.
    If credentials are not yet configured in .env, operates in simulation mode.
    """
    if not config.WHATSAPP_TOKEN or not config.WHATSAPP_PHONE_ID:
        logger.info("[WhatsApp] Outbound message simulated: credentials not configured")
        return {
            "status": "simulated",
            "to": to_number,
            "preview": message_text[:150],
            "note": "Configure WHATSAPP_TOKEN and WHATSAPP_PHONE_ID in .env for live transmission.",
        }

    url = f"https://graph.facebook.com/{config.WHATSAPP_API_VERSION}/{config.WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {config.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message_text,
        },
    }

    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code in (200, 201):
                logger.info("[WhatsApp] Outbound message accepted by Meta")
                return {"status": "sent", "response": resp.json()}
            else:
                logger.error(
                    "[WhatsApp] Outbound send failed: HTTP %s", resp.status_code
                )
                return {"status": "error", "code": resp.status_code, "detail": resp.text}
    except Exception as e:
        logger.exception(f"[WhatsApp] Network error dispatching message to {to_number}: {e}")
        return {"status": "exception", "error": str(e)}


def _handle_meta_inbound_payload(body: dict):
    # Serialize the prototype's in-memory conversation state and suppress Meta
    # redelivery while this process is running. This is not a durable job queue.
    with _meta_message_lock:
        _process_meta_inbound_payload(body)


def _process_meta_inbound_payload(body: dict):
    """
    Background worker that extracts incoming messages, maintains per-phone-number
    sessions, invokes the AarogyaSathi Fast-Path router, and dispatches responses.
    """
    try:
        entries = body.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                receiver_id = value.get("metadata", {}).get("phone_number_id")
                if receiver_id and config.WHATSAPP_PHONE_ID and receiver_id != config.WHATSAPP_PHONE_ID:
                    continue
                messages = value.get("messages", [])

                for msg in messages:
                    from_number = msg.get("from")  # e.g., '919876543210'
                    msg_type = msg.get("type")
                    message_id = msg.get("id")

                    if not from_number or not message_id or message_id in _completed_meta_messages:
                        continue

                    # Extract incoming user query
                    user_text = ""
                    if msg_type == "text":
                        user_text = msg.get("text", {}).get("body", "").strip()
                    elif msg_type == "interactive":
                        # Support interactive button clicks if used in future
                        interactive = msg.get("interactive", {})
                        user_text = (
                            interactive.get("button_reply", {}).get("title")
                            or interactive.get("list_reply", {}).get("title", "")
                        )
                    else:
                        # Non-text media (audio/image) notice
                        reply = (
                            "AarogyaSathi currently accepts text messages and forwarded health claims. "
                            "Please type your health question, symptoms, or claim."
                        )
                        sent = send_whatsapp_message(from_number, reply)
                        if sent.get("status") == "sent":
                            _remember_meta_message(message_id)
                        continue

                    if not user_text:
                        continue

                    logger.info("[WhatsApp] Processing incoming text message")

                    # Use the phone number as the persistent user session key
                    user_session = session_store.get_session(from_number)

                    # Execute AarogyaSathi clinical / factcheck / triage router
                    result = router.process_message(user_text, session=user_session)
                    bot_reply = result.get("text", "")

                    if bot_reply:
                        # Meta text messages have a 4096-character body limit.
                        parts = [bot_reply[i:i + 4000] for i in range(0, len(bot_reply), 4000)]
                        for part in parts:
                            sent = send_whatsapp_message(from_number, part)
                            if sent.get("status") != "sent":
                                logger.error("[WhatsApp] Reply delivery failed")
                                break
                        else:
                            _remember_meta_message(message_id)

    except Exception as e:
        logger.exception(f"[WhatsApp] Error processing inbound webhook payload: {e}")


def _remember_meta_message(message_id):
    _completed_meta_messages[message_id] = True
    while len(_completed_meta_messages) > 4096:
        _completed_meta_messages.popitem(last=False)


@whatsapp_router.get("")
@whatsapp_router.get("/")
def meta_webhook_verification(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """
    Meta Developer Dashboard Handshake:
    Meta sends a GET request to verify ownership of the webhook URL using WHATSAPP_VERIFY_TOKEN.
    """
    if (hub_mode == "subscribe" and hub_challenge is not None
            and config.WHATSAPP_VERIFY_TOKEN and hub_verify_token
            and hmac.compare_digest(hub_verify_token, config.WHATSAPP_VERIFY_TOKEN)):
        logger.info("[WhatsApp] Webhook handshake successfully verified with Meta!")
        return PlainTextResponse(content=hub_challenge, status_code=200)

    logger.warning("[WhatsApp] Webhook verification rejected")
    return JSONResponse(status_code=403, content={"error": "Verification token mismatch"})


@whatsapp_router.post("")
@whatsapp_router.post("/")
async def meta_webhook_message(request: Request, background_tasks: BackgroundTasks):
    """
    Meta Inbound Webhook:
    Receives incoming WhatsApp messages from Meta Graph API.
    Acknowledge with 200 OK immediately and process asynchronously in background.
    """
    if not config.WHATSAPP_APP_SECRET:
        raise HTTPException(status_code=503, detail="WhatsApp webhook authentication not configured")
    raw_body = await request.body()
    if len(raw_body) > 1024 * 1024:
        raise HTTPException(status_code=413, detail="Webhook payload too large")
    expected = "sha256=" + hmac.new(
        config.WHATSAPP_APP_SECRET.encode(), raw_body, hashlib.sha256
    ).hexdigest()
    supplied = request.headers.get("x-hub-signature-256", "")
    if not hmac.compare_digest(expected, supplied):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")
    try:
        body = json.loads(raw_body)
    except (ValueError, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Invalid JSON")
    if not isinstance(body, dict) or body.get("object") != "whatsapp_business_account":
        raise HTTPException(status_code=400, detail="Invalid WhatsApp payload")

    # Offload processing to background task to strictly respect Meta's fast acknowledgement SLA
    background_tasks.add_task(_handle_meta_inbound_payload, body)
    return {"status": "ok"}


@whatsapp_router.post("/simulate")
def simulate_whatsapp_chat(req: dict):
    """
    Sandbox / Viva Demo Endpoint:
    Allows professors or testers to simulate an inbound WhatsApp message from a phone number
    without needing live Meta credentials.
    """
    from_number = req.get("from", "919999999999")
    message = req.get("message", "What are dengue symptoms?")

    user_session = session_store.get_session(from_number)
    result = router.process_message(message, session=user_session)
    reply = result.get("text", "")
    meta = result.get("meta", {})

    return {
        "channel": "whatsapp",
        "sender": from_number,
        "input_message": message,
        "bot_reply": reply,
        "meta": meta,
        "meta_graph_api_payload": {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": reply},
        },
    }


import html
import time
from urllib.parse import parse_qs
from fastapi import Response


@whatsapp_router.post("/twilio")
@whatsapp_router.get("/twilio")
async def twilio_webhook_inbound(request: Request):
    """
    Twilio WhatsApp Sandbox Webhook:
    Receives incoming messages from Twilio (POST form-data or GET query params).
    Processes through AarogyaSathi Fast-Path router and replies with standard TwiML XML.
    """
    t_start = time.time()
    if request.method == "POST":
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8", errors="ignore")
        parsed = parse_qs(body_str)
        from_user = parsed.get("From", [""])[0]
        user_text = parsed.get("Body", [""])[0].strip()
    else:
        from_user = request.query_params.get("From", "")
        user_text = request.query_params.get("Body", "").strip()

    phone_clean = from_user.replace("whatsapp:", "").replace("+", "").strip()
    session_id = phone_clean or "twilio_guest"

    print(f"[Twilio Inbound] From: {from_user} | Msg: {user_text}", flush=True)

    if not user_text:
        twiml = '<?xml version="1.0" encoding="UTF-8"?>\n<Response></Response>'
        return Response(
            content=twiml,
            media_type="text/xml",
            headers={"Content-Type": "text/xml; charset=utf-8", "Cache-Control": "no-transform"},
        )

    # Instant response for Twilio sandbox pairing command (sub-10ms)
    if user_text.lower().startswith("join"):
        reply_text = (
            "Namaste! 🙏 Welcome to AarogyaSathi (आरोग्यसाथी).\n\n"
            "I am your AI-powered public health companion verified against WHO and MoHFW guidelines.\n\n"
            "You can ask me questions like:\n"
            "• What are dengue symptoms?\n"
            "• मलेरिया से कैसे बचें?\n"
            "• Baby vaccination schedule at 6 weeks\n"
            "• Or check any viral rumor (e.g. 'fact check: garlic cures dengue')\n\n"
            "How can I help you today?"
        )
    else:
        user_session = session_store.get_session(session_id)
        result = router.process_message(user_text, session=user_session)
        reply_text = result.get("text", "")

    # Twilio WhatsApp strictly expects <Body> inside <Message> with CDATA to preserve formatting and unicode
    clean_reply = reply_text.replace("]]>", "]]&gt;")
    twiml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Response>\n'
        '    <Message>\n'
        f'        <Body><![CDATA[{clean_reply}]]></Body>\n'
        '    </Message>\n'
        '</Response>'
    )

    elapsed = round(time.time() - t_start, 3)
    print(f"[Twilio Outbound] Handled in {elapsed}s | Sent to {from_user}", flush=True)

    return Response(
        content=twiml,
        media_type="text/xml",
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "Cache-Control": "no-transform",
        },
    )
