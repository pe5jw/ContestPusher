"""
ContestPusher — self-hosted contest log sync tool
Versie: 0.1.0
Auteur: Joeri — joeri@noppus.nl
Licentie: MIT
"""
import asyncio
import json
import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from database import (
    get_decrypted_config, get_service, get_services, get_uploads,
    init_db, save_service, save_upload,
)
from services.adif_parser import parse_adif
from services import lotw, eqsl, qrz, clublog, hrdlog

# ── App setup ──────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
VERSION = "0.1.0"

app = FastAPI(title="ContestPusher", version=VERSION, docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Service registry: id → module
SERVICE_MODULES = {
    "lotw":    lotw,
    "eqsl":    eqsl,
    "qrz":     qrz,
    "clublog": clublog,
    "hrdlog":  hrdlog,
}

SERVICE_META = {
    "lotw":    {"name": "Logbook of the World", "color": "#1a56db", "icon": "🏛️"},
    "eqsl":    {"name": "eQSL.cc",              "color": "#16a34a", "icon": "📧"},
    "qrz":     {"name": "QRZ Logbook",          "color": "#dc2626", "icon": "📻"},
    "clublog": {"name": "Club Log",             "color": "#9333ea", "icon": "📋"},
    "hrdlog":  {"name": "HRDLog.net",           "color": "#ea580c", "icon": "🌐"},
}


# ── HTML pagina (single-file frontend) ────────────────────────────────────────

def load_html() -> str:
    return (BASE_DIR / "templates" / "index.html").read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def root():
    return load_html()


# ── API endpoints ──────────────────────────────────────────────────────────────

@app.get("/api/services")
async def api_services():
    """Geeft alle services terug met hun status en veilige config."""
    services = get_services()
    result = []
    for s in services:
        meta = SERVICE_META.get(s["id"], {})
        result.append({
            "id": s["id"],
            "name": s["name"],
            "enabled": bool(s["enabled"]),
            "color": meta.get("color", "#666"),
            "icon": meta.get("icon", "🔌"),
            "config": s["safe_config"],  # Wachtwoorden leeg
        })
    return result


@app.post("/api/services/{service_id}")
async def api_save_service(service_id: str, request: Request):
    """Sla service configuratie op."""
    if service_id not in SERVICE_MODULES:
        raise HTTPException(404, "Service niet gevonden")
    body = await request.json()
    enabled = body.get("enabled", False)
    config = body.get("config", {})
    save_service(service_id, enabled, config)
    return {"ok": True}


@app.get("/api/service-fields")
async def api_service_fields():
    """Geeft de vereiste configuratievelden per service terug."""
    return {
        "lotw": [
            {"key": "callsign",   "label": "Callsign",          "type": "text",     "required": True},
            {"key": "tqsl_path",  "label": "Pad naar TQSL",     "type": "text",     "required": False,
             "placeholder": "tqsl  (of bijv. C:\\Program Files\\TQSL\\tqsl.exe)"},
            {"key": "location",   "label": "Station locatie",    "type": "text",     "required": False,
             "placeholder": "Optioneel — LoTW station location naam"},
        ],
        "eqsl": [
            {"key": "username",  "label": "Gebruikersnaam", "type": "text",     "required": True},
            {"key": "password",  "label": "Wachtwoord",     "type": "password", "required": True},
        ],
        "qrz": [
            {"key": "api_key",   "label": "QRZ API Key",    "type": "password", "required": True,
             "hint": "Vereist betaald QRZ abonnement. Te vinden op logbook.qrz.com"},
        ],
        "clublog": [
            {"key": "callsign",  "label": "Callsign",   "type": "text",     "required": True},
            {"key": "email",     "label": "Email",       "type": "email",    "required": True},
            {"key": "password",  "label": "Wachtwoord", "type": "password", "required": True},
        ],
        "hrdlog": [
            {"key": "callsign",  "label": "Callsign",   "type": "text",     "required": True},
            {"key": "api_key",   "label": "API Key",    "type": "password", "required": True,
             "hint": "Te vinden in je HRDLog account instellingen"},
        ],
    }


@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...)):
    """
    Upload een ADIF bestand en stuur het naar alle ingeschakelde services.
    Geeft realtime SSE stream terug via /api/upload-stream.
    """
    content = (await file.read()).decode("utf-8", errors="replace")
    qsos, count = parse_adif(content)

    if count == 0:
        return JSONResponse({"ok": False, "message": "Geen geldige QSO's gevonden in het bestand"}, status_code=400)

    # Haal alle ingeschakelde services op
    services = [s for s in get_services() if s["enabled"]]
    if not services:
        return JSONResponse({"ok": False, "message": "Geen services ingeschakeld — configureer eerst een service"}, status_code=400)

    # Upload parallel naar alle services
    async def upload_to_service(service_id: str) -> dict:
        config = get_decrypted_config(service_id)
        module = SERVICE_MODULES[service_id]
        try:
            result = await module.upload(content, config)
        except Exception as e:
            result = {"ok": False, "message": str(e)}
        return {"service_id": service_id, **result}

    tasks = [upload_to_service(s["id"]) for s in services]
    results_list = await asyncio.gather(*tasks)
    results = {r["service_id"]: r for r in results_list}

    # Sla upload op in history
    save_upload(file.filename or "upload.adi", count, results)

    return {
        "ok": True,
        "filename": file.filename,
        "qso_count": count,
        "results": results,
    }


@app.get("/api/history")
async def api_history():
    """Geeft upload history terug."""
    return get_uploads(50)


@app.get("/api/version")
async def api_version():
    return {"version": VERSION, "name": "ContestPusher"}


# ── Startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    init_db()
    print(f"\n{'='*50}")
    print(f"  ContestPusher v{VERSION} gestart!")
    print(f"  Open in je browser: http://localhost:8090")
    print(f"{'='*50}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("CONTESTPUSHER_PORT", 8090))
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=port,
        reload=False,
        log_level="warning",
    )
