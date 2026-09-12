import traceback

from fastapi.testclient import TestClient

from app.main import app

with TestClient(app) as client:
    for msg in ["hi", "I have fever and headache", "fact check: garlic cures dengue"]:
        try:
            r = client.post("/api/chat", json={"message": msg})
            print(msg, "=>", r.status_code)
            print(r.json()["reply"][:120].replace("\n", " | "))
        except Exception:
            traceback.print_exc()
