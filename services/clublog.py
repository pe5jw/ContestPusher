"""
Club Log upload handler voor ContestPusher.
Gebruikt de Club Log ADIF upload API.
"""
import httpx


CLUBLOG_UPLOAD_URL = "https://clublog.org/putlogs.php"


async def upload(adif_content: str, config: dict) -> dict:
    """
    Upload ADIF naar Club Log.
    Config verwacht: email, password, callsign, app_key (optioneel)
    """
    email = config.get("email", "")
    password = config.get("password", "")
    callsign = config.get("callsign", "")
    # ContestPusher app key voor Club Log API identificatie
    app_key = config.get("app_key", "contestpusher")

    if not email or not password or not callsign:
        return {"ok": False, "message": "Email, wachtwoord en callsign vereist voor Club Log"}

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                CLUBLOG_UPLOAD_URL,
                data={
                    "email": email,
                    "password": password,
                    "callsign": callsign,
                    "api": app_key,
                    "adif": adif_content,
                    "clear": "0",   # 0 = voeg toe, 1 = vervang alles
                }
            )

        body = response.text.strip()

        if response.status_code == 200:
            if "OK" in body or "success" in body.lower():
                return {"ok": True, "message": "Succesvol geüpload naar Club Log"}
            elif "error" in body.lower() or "invalid" in body.lower():
                return {"ok": False, "message": f"Club Log fout: {body[:200]}"}
            else:
                return {"ok": True, "message": f"Club Log: {body[:100]}"}
        elif response.status_code == 403:
            return {"ok": False, "message": "Club Log: toegang geweigerd — controleer credentials"}
        else:
            return {"ok": False, "message": f"Club Log HTTP {response.status_code}: {body[:100]}"}

    except httpx.TimeoutException:
        return {"ok": False, "message": "Timeout: Club Log reageert niet"}
    except httpx.RequestError as e:
        return {"ok": False, "message": f"Netwerkfout: {str(e)}"}
    except Exception as e:
        return {"ok": False, "message": str(e)}
