"""
HRDLog.net upload handler voor ContestPusher.
Gebruikt de HRDLog REST API.
"""
import httpx


HRDLOG_UPLOAD_URL = "https://www.hrdlog.net/api/qso/"


async def upload(adif_content: str, config: dict) -> dict:
    """
    Upload ADIF naar HRDLog.net.
    Config verwacht: callsign, api_key
    """
    callsign = config.get("callsign", "")
    api_key = config.get("api_key", "")

    if not callsign or not api_key:
        return {"ok": False, "message": "Callsign en API key vereist voor HRDLog"}

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                HRDLOG_UPLOAD_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "CALLSIGN": callsign,
                    "ADIF": adif_content,
                }
            )

        if response.status_code in (200, 201):
            try:
                data = response.json()
                count = data.get("imported", data.get("count", "?"))
                return {"ok": True, "message": f"{count} QSO's geïmporteerd in HRDLog"}
            except Exception:
                return {"ok": True, "message": "Upload succesvol naar HRDLog"}
        elif response.status_code == 401:
            return {"ok": False, "message": "HRDLog: ongeautoriseerd — controleer API key"}
        else:
            return {"ok": False, "message": f"HRDLog HTTP {response.status_code}: {response.text[:100]}"}

    except httpx.TimeoutException:
        return {"ok": False, "message": "Timeout: HRDLog reageert niet"}
    except httpx.RequestError as e:
        return {"ok": False, "message": f"Netwerkfout: {str(e)}"}
    except Exception as e:
        return {"ok": False, "message": str(e)}
