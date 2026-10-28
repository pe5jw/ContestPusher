"""
QRZ Logbook upload handler voor ContestPusher.
Gebruikt de QRZ Logbook API (vereist betaald abonnement).
"""
import httpx
import re


QRZ_API_URL = "https://logbook.qrz.com/api"


async def upload(adif_content: str, config: dict) -> dict:
    """
    Upload ADIF naar QRZ Logbook.
    Config verwacht: api_key
    Vereist: QRZ XML Data betaald abonnement
    """
    api_key = config.get("api_key", "")

    if not api_key:
        return {"ok": False, "message": "QRZ API key niet geconfigureerd"}

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                QRZ_API_URL,
                data={
                    "KEY": api_key,
                    "ACTION": "INSERT",
                    "ADIF": adif_content,
                }
            )

        body = response.text
        # QRZ geeft KEY=value pairs terug
        params = dict(re.findall(r'(\w+)=([^\&\n]+)', body))

        result = params.get("RESULT", "").upper()
        count = params.get("COUNT", "?")
        message = params.get("MESSAGE", "")

        if result == "OK":
            return {"ok": True, "message": f"{count} QSO's toegevoegd aan QRZ Logbook"}
        elif result == "FAIL":
            return {"ok": False, "message": f"QRZ fout: {message or 'Onbekend'}"}
        elif result == "AUTH":
            return {"ok": False, "message": "QRZ authenticatie mislukt — controleer API key"}
        else:
            return {"ok": False, "message": f"Onverwachte QRZ response: {body[:100]}"}

    except httpx.TimeoutException:
        return {"ok": False, "message": "Timeout: QRZ reageert niet"}
    except httpx.RequestError as e:
        return {"ok": False, "message": f"Netwerkfout: {str(e)}"}
    except Exception as e:
        return {"ok": False, "message": str(e)}
