import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import config
from app.core import embeddings, generator, intent, kb, language, retriever
from app.core import session as session_store
from app.core.router import process_message
from app.factcheck import verifier
from app.surveillance import syndromic

app = FastAPI(title="AarogyaSathi - AI-Driven Public Health Chatbot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(config.WEB_DIR)), name="static")


class ChatRequest(BaseModel):
    message: str
    pincode: str | None = None
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    intent: str
    language: str
    latency_ms: int
    generator: str | None = None
    llm_backend: str | None = None
    flow: str | None = None
    factcheck: dict | None = None


_started = False


@app.on_event("startup")
def startup():
    global _started
    if _started:
        return
    _started = True
    kb.load()
    intent.load()
    language._load()
    retriever._ensure_index()
    verifier._ensure_index()
    embeddings.get_model()
    _warmup_llm()


def _warmup_llm():
    import threading
    import time

    def _run():
        import httpx
        for _ in range(12):
            try:
                r = httpx.post(
                    f"{config.OLLAMA_URL}/api/generate",
                    json={
                        "model": config.LLM_MODEL,
                        "prompt": "hi",
                        "stream": False,
                        "options": {"num_predict": 3, "num_ctx": 4096},
                    },
                    timeout=30,
                )
                if r.status_code == 200:
                    return
            except Exception:
                pass
            time.sleep(5)

    threading.Thread(target=_run, daemon=True).start()


def _update_summary(session):
    import threading

    def _run():
        try:
            summary = generator.summarize_conversation(session.get("history") or [])
            if summary:
                session.set("summary", summary)
        except Exception:
            pass

    threading.Thread(target=_run, daemon=True).start()


@app.get("/")
def index():
    return FileResponse(str(config.WEB_DIR / "index.html"))


@app.get("/api/health")
def health():
    generator.reset_availability()
    return {
        "status": "ok",
        "models": "loaded",
        "llm": {
            "backend": generator.backend(),
            "model": config.LLM_CLOUD_MODEL if generator.backend() == "cloud" else config.LLM_MODEL,
        },
        "languages": config.SUPPORTED_LANGUAGES,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    start = time.time()
    session = session_store.get_session(req.session_id)
    result = process_message(req.message, req.pincode, session)
    history = session.get("history") or []
    history.append({"role": "user", "text": req.message[:200]})
    history.append({"role": "bot", "text": result["text"][:300]})
    session.set("history", history[-12:])
    if len(history) >= 6 and (len(history) // 2) % 3 == 0:
        _update_summary(session)
    latency = int((time.time() - start) * 1000)
    meta = result.get("meta", {})
    factcheck = meta.get("factcheck")
    verdict = factcheck.get("verdict") if factcheck else None
    verdict_display = {
        "TRUE": "VERIFIED",
        "MYTH": "MYTH",
        "PARTLY_TRUE": "PARTLY TRUE",
        "UNVERIFIABLE": "UNVERIFIABLE",
    }.get(verdict, verdict)
    if factcheck is not None:
        factcheck = {
            "verdict": verdict_display,
            "confidence": factcheck.get("confidence"),
            "fear_mongering": factcheck.get("fear_mongering"),
            "tags": factcheck.get("tags", []),
            "sources": [s["name"] for s in factcheck.get("sources", [])],
        }
    if req.pincode:
        symptoms = meta.get("symptoms")
        if symptoms:
            syndromic.record_symptom_event(req.pincode, symptoms, meta.get("lang", "en"))
            syndromic.run_detection(req.pincode)
    syndromic.record_message(req.pincode, meta.get("intent", "unknown"), meta.get("lang", "en"), verdict)
    return ChatResponse(
        reply=result["text"],
        intent=meta.get("intent", "unknown"),
        language=meta.get("lang", "en"),
        latency_ms=latency,
        generator=meta.get("generator"),
        llm_backend=generator.last_backend(),
        flow=meta.get("flow"),
        factcheck=factcheck,
    )


@app.get("/api/intents")
def intents_debug():
    return {"available": True}


@app.get("/api/stats")
def stats():
    return syndromic.stats()


@app.get("/api/surveillance/alerts")
def surveillance_alerts():
    db_alerts = syndromic.active_alerts()
    kb_items = []
    for a in kb.alerts():
        kb_items.append(
            {
                "source": "advisory",
                "title": a["title"].get("en", ""),
                "body": a["body"].get("en", ""),
                "source_name": a["source"]["name"],
            }
        )
    return {"spike_alerts": db_alerts, "official_advisories": kb_items}


@app.post("/api/surveillance/run")
def surveillance_run():
    return {"new_alerts": syndromic.run_detection()}


@app.post("/api/surveillance/seed")
def surveillance_seed():
    return {"new_alerts": syndromic.seed_demo()}


@app.post("/api/surveillance/clear")
def surveillance_clear():
    syndromic.clear_all()
    return {"status": "cleared"}


@app.get("/admin")
def admin_page():
    return FileResponse(str(config.WEB_DIR / "admin.html"))


@app.exception_handler(Exception)
def unhandled(request, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})
